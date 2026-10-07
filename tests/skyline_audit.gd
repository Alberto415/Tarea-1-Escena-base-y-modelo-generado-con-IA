extends SceneTree
## Documentation measurements: current courier, current 6 m/s controller.
var parts: int = 0
var triangles: int = 0
var vertices: int = 0
var normals_ok: bool = true
var uv_parts: int = 0
var degenerate: int = 0
var materials: Dictionary = {}
var bounds := AABB()
var has_bounds: bool = false
var results: Array = []
var body: CharacterBody3D
var rig: Node3D

func _initialize() -> void:
	call_deferred("run")

func traverse(node: Node, transform: Transform3D = Transform3D.IDENTITY) -> void:
	if node is Node3D:
		transform *= node.transform
	if node is MeshInstance3D:
		parts += 1
		var box: AABB = transform * node.mesh.get_aabb()
		bounds = bounds.merge(box) if has_bounds else box
		has_bounds = true
		for surface in node.mesh.get_surface_count():
			var arrays: Array = node.mesh.surface_get_arrays(surface)
			var points: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]
			var ns: PackedVector3Array = arrays[Mesh.ARRAY_NORMAL]
			var indices: PackedInt32Array = arrays[Mesh.ARRAY_INDEX]
			vertices += points.size()
			triangles += indices.size() / 3 if not indices.is_empty() else points.size() / 3
			if arrays[Mesh.ARRAY_TEX_UV] != null and arrays[Mesh.ARRAY_TEX_UV].size() > 0:
				uv_parts += 1
			for normal in ns:
				if not normal.is_finite() or absf(normal.length() - 1.0) > 0.01:
					normals_ok = false
			var faces: PackedVector3Array = node.mesh.get_faces()
			for i in range(0, faces.size(), 3):
				if (faces[i+1]-faces[i]).cross(faces[i+2]-faces[i]).length_squared() < 0.000000000001:
					degenerate += 1
			var material: Material = node.mesh.surface_get_material(surface)
			materials[str(material.get_instance_id())] = true
	for child in node.get_children():
		traverse(child, transform)

func ticks(n: int) -> void:
	for i in n:
		await physics_frame
	await process_frame

func check(name: String, ok: bool, detail: Variant = "") -> void:
	results.append({"name": name, "passed": ok, "detail": detail})
	print("AUDIT %s: %s %s" % ["PASS" if ok else "FAIL", name, str(detail)])

func run() -> void:
	var model: Node3D = load("res://scenes/courier_visual.tscn").instantiate()
	traverse(model)
	var model_report := {"parts": parts, "triangles": triangles, "vertices": vertices, "materials": materials.size(), "uv_surfaces": uv_parts, "textures": 0, "bones": 0, "normal_vectors_finite_unit": normals_ok, "degenerate_triangles": degenerate, "aabb_size_m": [bounds.size.x, bounds.size.y, bounds.size.z], "aabb_min_m": [bounds.position.x,bounds.position.y,bounds.position.z]}
	model.free()
	var world := Node3D.new()
	root.add_child(world)
	var floor := StaticBody3D.new()
	var shape := CollisionShape3D.new()
	var box := BoxShape3D.new()
	box.size = Vector3(60,1,60)
	shape.shape = box
	floor.add_child(shape)
	floor.position.y = -0.5
	world.add_child(floor)
	body = load("res://scenes/courier_player.tscn").instantiate()
	body.speed = 6.0
	body.jump_speed = 9.0
	world.add_child(body)
	rig = body.get_node("CameraRig")
	var distances: Array = []
	for cap in [30,144]:
		Engine.max_fps = cap
		body.reset_player(Vector3.ZERO)
		rig.rotation.y = 0
		await ticks(30)
		var start: Vector3 = body.position
		var begin: int = Time.get_ticks_usec()
		Input.action_press("move_forward")
		await ticks(120)
		Input.action_release("move_forward")
		var distance: float = (body.position-start).length()
		distances.append(distance)
		check("120 pasos a %d FPS" % cap, distance > 11.0 and distance < 12.1, {"meters": distance,"wall_seconds": (Time.get_ticks_usec()-begin)/1000000.0,"render_fps": Engine.get_frames_per_second()})
		await ticks(30)
		check("Walk vuelve a Idle", body.state == body.State.IDLE)
	check("Consistencia 30/144", absf(distances[0]-distances[1]) < 0.18, absf(distances[0]-distances[1]))
	body.reset_player(Vector3.ZERO)
	await ticks(30)
	var before: int = body.jump_count
	Input.action_press("jump")
	await ticks(10)
	Input.action_release("jump")
	check("Jump sin apoyo", body.state == body.State.JUMP and not body.is_on_floor())
	Input.action_press("jump")
	await ticks(12)
	Input.action_release("jump")
	check("No hay doble salto", body.jump_count == before+1)
	await ticks(70)
	check("Aterriza en Idle", body.is_on_floor() and body.state == body.State.IDLE)
	rig.rotation.y = PI/2
	Input.action_press("move_forward")
	await ticks(60)
	Input.action_release("move_forward")
	check("W sigue yaw de camara", body.position.x < -5.0 and absf(body.position.z)<0.1)
	await ticks(30)
	# A real wall for the same 6 m SpringArm used in SKYLINE.
	var wall := StaticBody3D.new()
	var wall_collision := CollisionShape3D.new()
	var wall_shape := BoxShape3D.new()
	wall_shape.size = Vector3(50,6,0.5)
	wall_collision.shape = wall_shape
	wall.add_child(wall_collision)
	wall.position = Vector3(0,3,4)
	world.add_child(wall)
	body.reset_player(Vector3(0,0.05,2.5))
	rig.rotation.y = 0
	await ticks(30)
	var arm: SpringArm3D = rig.get_node("Pitch/SpringArm3D")
	check("Brazo retraido", arm.get_hit_length() < 2.0, arm.get_hit_length())
	var clear: bool = true
	for i in 120:
		rig.rotation.y = TAU*i/120.0
		await ticks(1)
		if arm.get_node("Camera3D").global_position.z > 3.7:
			clear = false
	check("Giro 360 junto a pared", clear)
	var report := {"engine": Engine.get_version_info().string, "backend": DisplayServer.get_name(), "physics_hz": Engine.physics_ticks_per_second,"model":model_report,"checks":results,"distance_30":distances[0],"distance_144":distances[1]}
	var f := FileAccess.open("res://output/evidence/skyline_audit.json", FileAccess.WRITE)
	f.store_string(JSON.stringify(report,"\t"))
	var all_ok: bool = true
	for result in results:
		all_ok = all_ok and result.passed
	quit(0 if all_ok else 1)
