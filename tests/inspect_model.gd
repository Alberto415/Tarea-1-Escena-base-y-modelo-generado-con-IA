extends SceneTree

func _initialize() -> void:
	call_deferred("inspect")

func inspect() -> void:
	assert(InputMap.action_get_events("camera_left")[0].physical_keycode == KEY_LEFT)
	assert(InputMap.action_get_events("camera_right")[0].physical_keycode == KEY_RIGHT)
	assert(InputMap.action_get_events("camera_up")[0].physical_keycode == KEY_UP)
	assert(InputMap.action_get_events("camera_down")[0].physical_keycode == KEY_DOWN)
	var scene = load("res://scenes/model_comparison.tscn").instantiate()
	root.add_child(scene)
	for i in 10:
		await process_frame
	await RenderingServer.frame_post_draw
	root.get_texture().get_image().save_png("res://output/evidence/04_model_comparison.png")
	var meshes: Array = scene.get_node("FinalMenta").find_children("*", "MeshInstance3D", true, false)
	var triangles: int = 0
	var materials: Dictionary = {}
	for instance in meshes:
		var mesh: Mesh = instance.mesh
		for surface in mesh.get_surface_count():
			var arrays: Array = mesh.surface_get_arrays(surface)
			triangles += arrays[Mesh.ARRAY_INDEX].size() / 3
			var material = mesh.surface_get_material(surface)
			materials[material.resource_name] = true
	print("IMPORTED MODEL: %d nodes, %d triangles, %d materials" % [meshes.size(), triangles, materials.size()])
	quit(0 if meshes.size() == 11 and triangles == 132 and materials.size() == 3 else 1)
