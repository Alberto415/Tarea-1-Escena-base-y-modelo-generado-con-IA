extends Node
var failures: Array[String] = []
var checks: Array = []
var video: bool = false
@onready var level = get_parent()
@onready var player = level.get_node("Player")

func _ready() -> void:
	video = "--skyline-video" in OS.get_cmdline_user_args()
	call_deferred("run")

func ticks(n: int) -> void:
	for i in n:
		await get_tree().physics_frame
	await get_tree().process_frame

func check(name: String, ok: bool) -> void:
	checks.append({"name": name, "passed": ok})
	print("PARKOUR %s: %s" % ["PASS" if ok else "FAIL", name])
	if not ok:
		failures.append(name)

func steer(direction: Vector3) -> void:
	for action in ["move_forward", "move_back", "move_left", "move_right"]:
		Input.action_release(action)
	if absf(direction.x) > 0.01:
		Input.action_press("move_right" if direction.x > 0 else "move_left", absf(direction.x))
	if absf(direction.z) > 0.01:
		Input.action_press("move_back" if direction.z > 0 else "move_forward", absf(direction.z))

func screenshot(name: String) -> void:
	if DisplayServer.get_name() == "headless":
		return
	await RenderingServer.frame_post_draw
	get_viewport().get_texture().get_image().save_png("res://output/evidence/" + name + ".png")

func run() -> void:
	await ticks(50)
	check("inicio apoyado", player.is_on_floor())
	await screenshot("skyline_gameplay")
	if video:
		await ticks(360)
	# Front portrait using the existing orbit rig, then return to forward yaw.
	player.get_node("CameraRig").rotation.y = PI - 0.45
	await ticks(5)
	await screenshot("skyline_character")
	if video:
		await ticks(360)
	player.get_node("CameraRig").rotation.y = 0
	for i in range(1, level.route.size()):
		var previous: Array = level.route[i-1]
		var current: Array = level.route[i]
		var target := Vector3(current[0], current[1], current[2])
		var start := Vector3(previous[0], previous[1], previous[2])
		var direction: Vector3 = (target - start)
		direction.y = 0
		direction = direction.normalized()
		var edge: Vector3 = start + direction * (float(previous[3]) - 0.8)
		for step in 100:
			var offset: Vector3 = edge - player.position
			offset.y = 0
			if offset.dot(direction) < 0.12:
				break
			steer(offset.normalized())
			await ticks(1)
		Input.action_press("jump")
		steer(direction)
		await ticks(2)
		Input.action_release("jump")
		var arrived: bool = false
		for step in 120:
			var offset: Vector3 = target - player.position
			offset.y = 0
			steer(offset.normalized() if offset.length() > 0.7 else Vector3.ZERO)
			await ticks(1)
			if i == 1 and step == 8:
				await screenshot("skyline_jump")
			if level.reached >= i and player.is_on_floor():
				arrived = true
				break
			if player.position.y < current[1] - 3:
				break
		steer(Vector3.ZERO)
		await ticks(20)
		check("salto real azotea %d -> %d" % [i, i+1], arrived)
		if not arrived:
			print("position ", player.position, " target ", target)
			break
		if video and i in [4, 8, 12]:
			level.notice = "Checkpoint: progreso guardado al aterrizar"
			level.notice_time = 6.0
			await ticks(360)
		if i == 8:
			await screenshot("skyline_checkpoint")
			player.reset_player(Vector3(30, -11, 0))
			await ticks(90)
			check("checkpoint intermedio recupera la caida", level.checkpoint == 8 and player.is_on_floor() and player.position.distance_to(player.respawn_position) < 0.2)
	check("meta y progreso", level.finished and level.reached == 15)
	check("quince cristales recogidos", level.crystals.size() == 15)
	await screenshot("skyline_finish")
	if video:
		await ticks(900)
	# Check respawn by physically falling and waiting for the real fall threshold.
	level.finished = false
	player.reset_player(Vector3(30, -11, 0))
	await ticks(90)
	check("caida vuelve al checkpoint", player.is_on_floor() and player.position.distance_to(player.respawn_position) < 0.2 and level.falls == 2)
	var path: String = "res://output/evidence/skyline_video_results.json" if video else "res://output/evidence/parkour_results.json"
	var output := FileAccess.open(path, FileAccess.WRITE)
	output.store_string(JSON.stringify({"failures": failures, "checks": checks, "reached": level.reached, "crystals": level.crystals.size(), "falls": level.falls}, "\t"))
	get_tree().quit(0 if failures.is_empty() else 1)
