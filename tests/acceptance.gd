extends Node
## Integration tests: actual input, physics, imported model and camera.
var results: Array = []
var failures: int = 0
var demo: bool = false
@onready var level = get_parent()
@onready var player = level.get_node("Player")
@onready var rig = player.get_node("CameraRig")
@onready var arm = rig.get_node("Pitch/SpringArm3D")

func _ready() -> void:
	demo = "--demo" in OS.get_cmdline_user_args()
	call_deferred("run")

func ticks(count: int) -> void:
	for i in count:
		await get_tree().physics_frame
	await get_tree().process_frame

func check(label: String, passed: bool, detail: String = "") -> void:
	results.append({"test": label, "passed": passed, "detail": detail})
	if not passed:
		failures += 1
	print("TEST %s: %s %s" % ["PASS" if passed else "FAIL", label, detail])

func caption(value: String) -> void:
	level.get_node("HUD/Caption").text = value

func shot(name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("res://output/evidence/" + name + ".png")

func pause_demo(seconds: float) -> void:
	if demo:
		await ticks(int(seconds * 60))

func place(at: Vector3, yaw: float = 0.0) -> void:
	player.reset_player(at)
	rig.rotation.y = yaw
	await ticks(35)

func run() -> void:
	caption("01 / IDLE  ·  Controlador y modelo importado independientes")
	await ticks(60)
	check("Idle en suelo", player.state == player.State.IDLE and player.is_on_floor())
	await shot("01_idle")
	await pause_demo(7)
	var distances: Array = []
	for limit in [30, 144]:
		level.cap = limit
		Engine.max_fps = limit
		await place(Vector3(-10, 0.05, 10), -PI / 2)
		var start: Vector3 = player.position
		var start_usec: int = Time.get_ticks_usec()
		Input.action_press("move_forward")
		await ticks(120)
		Input.action_release("move_forward")
		var distance: float = Vector2(player.position.x-start.x, player.position.z-start.z).length()
		distances.append(distance)
		check("Caminar a %d FPS / 120 pasos" % limit, distance > 9.0 and distance < 10.2, "%.4f m; tiempo real=%.3f s" % [distance, (Time.get_ticks_usec()-start_usec)/1000000.0])
		check("Estado Walk", player.state == player.State.WALK)
		caption("02 / WALK  ·  %d FPS: %.3f m en 120 pasos de fisica" % [limit, distance])
		await pause_demo(4)
		await ticks(30)
		check("Walk vuelve a Idle", player.state == player.State.IDLE)
	check("Consistencia 30 vs 144 FPS", absf(distances[0]-distances[1]) < 0.18, "diferencia %.5f m" % absf(distances[0]-distances[1]))
	Engine.max_fps = 60
	level.cap = 60
	await place(Vector3(0, 0.05, 4))
	var jumps_before: int = player.jump_count
	Input.action_press("jump")
	await ticks(10)
	Input.action_release("jump")
	check("Jump en aire", player.state == player.State.JUMP and not player.is_on_floor())
	caption("03 / JUMP  ·  Espacio en el aire no crea un segundo salto")
	await shot("02_jump")
	Input.action_press("jump")
	await ticks(12)
	Input.action_release("jump")
	check("Sin doble salto", player.jump_count == jumps_before + 1)
	await ticks(70)
	check("Aterrizaje en Idle", player.state == player.State.IDLE and player.is_on_floor())
	await pause_demo(5)
	await place(Vector3(-3, 0.05, 3))
	Input.action_press("move_forward")
	await ticks(100)
	Input.action_release("move_forward")
	check("No atraviesa cubo", player.position.z > -0.61 and player.position.z < -0.4, str(player.position))
	Input.action_press("jump")
	Input.action_press("move_forward")
	await ticks(25)
	Input.action_release("jump")
	Input.action_release("move_forward")
	await ticks(60)
	check("Salto aterriza sobre obstaculo", player.is_on_floor() and player.position.y > 0.85, str(player.position))
	await pause_demo(5)
	await place(Vector3(0, 0.05, 8), PI / 2)
	Input.action_press("move_forward")
	await ticks(60)
	Input.action_release("move_forward")
	check("Movimiento relativo a camara", player.position.x < -4.0 and absf(player.position.z-8) < 0.1, str(player.position))
	await pause_demo(5)
	await place(Vector3(0, 0.05, 12.5))
	caption("04 / CAMARA  ·  SpringArm acorta su longitud junto a la pared")
	await ticks(10)
	check("SpringArm retraido", arm.get_hit_length() < 2.0, "longitud %.3f m" % arm.get_hit_length())
	await shot("03_camera")
	var clear: bool = true
	var min_length: float = 6.0
	for i in 120:
		rig.rotation.y = TAU * i / 120.0
		await ticks(1)
		min_length = minf(min_length, arm.get_hit_length())
		var camera_position: Vector3 = arm.get_node("Camera3D").global_position
		if camera_position.z > 13.7:
			clear = false
	check("Giro de camara 360 junto a pared", clear, "minimo %.3f m" % min_length)
	await pause_demo(5)
	rig.rotation.y = 0.0
	Input.action_press("move_back")
	await ticks(90)
	Input.action_release("move_back")
	check("No atraviesa pared", player.position.z <= 13.34)
	await place(Vector3(8, 0.05, 0), PI/4)
	Input.action_press("move_forward")
	await ticks(120)
	Input.action_release("move_forward")
	check("Colision en esquina", player.position.x > 6.69 and player.position.x < 6.8 and player.position.z > -1.31 and player.position.z < -1.2, str(player.position))
	await pause_demo(5)
	await place(Vector3(0, 0.05, 6))
	caption("05 / RESULTADOS  ·  %d pruebas, %d fallos  |  Alberto" % [results.size(), failures])
	await pause_demo(14)
	var report := {"engine": Engine.get_version_info().string, "physics_hz": Engine.physics_ticks_per_second, "render_backend": DisplayServer.get_name(), "results": results, "failures": failures, "distance_30": distances[0], "distance_144": distances[1]}
	var report_path: String = "res://output/evidence/demo_results.json" if demo else "res://output/evidence/results.json"
	var file := FileAccess.open(report_path, FileAccess.WRITE)
	file.store_string(JSON.stringify(report, "\t"))
	file.close()
	get_tree().quit(1 if failures else 0)

