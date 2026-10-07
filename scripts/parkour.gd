extends Node3D
## Progress is based on landed platforms, not touching a floating pickup in mid-air.
const CHECKPOINTS: Array[int] = [0, 4, 8, 12, 15]
var checkpoint: int = 0
var reached: int = 0
var crystals: Dictionary = {}
var elapsed: float = 0.0
var falls: int = 0
var finished: bool = false
var started: bool = false
var notice: String = "Llega al portal de la azotea 16"
var notice_time: float = 5.0
var best: float = 0.0
var route: Array = []
var cap: int = 144
@onready var player: CharacterBody3D = $Player

func _ready() -> void:
	route = preload("res://assets/parkour/route.gd").POINTS
	player.respawn_position = Vector3(0, 0.08, 4)
	player.fell.connect(_on_fall)
	player.physics_stepped.connect(_inspect_landing)
	Engine.max_fps = cap
	var save := ConfigFile.new()
	if save.load("user://skyline.cfg") == OK:
		best = save.get_value("run", "best_seconds", 0.0)
	if "--parkour-test" in OS.get_cmdline_user_args():
		add_child(load("res://tests/parkour_test.gd").new())

func _physics_process(delta: float) -> void:
	if Vector2(player.velocity.x, player.velocity.z).length() > 0.1:
		started = true
	if started and not finished:
		elapsed += delta

func _inspect_landing() -> void:
	if not player.is_on_floor():
		return
	for n in player.get_slide_collision_count():
		var collision: KinematicCollision3D = player.get_slide_collision(n)
		var collider: Object = collision.get_collider()
		if collision.get_normal().y > 0.7 and collider is StaticBody3D and str(collider.name).begins_with("Roof"):
			land_on(str(collider.name).trim_prefix("Roof").to_int())

func land_on(index: int) -> void:
	reached = maxi(reached, index)
	if index in CHECKPOINTS and index > checkpoint:
		checkpoint = index
		var point: Array = route[index]
		player.respawn_position = Vector3(point[0], point[1] + 0.08, point[2])
		notice = "Punto de control guardado"
		notice_time = 3.0
	if index == 15 and not finished:
		finished = true
		notice = "¡CIRCUITO COMPLETADO!"
		if best == 0.0 or elapsed < best:
			best = elapsed
			if not "--parkour-test" in OS.get_cmdline_user_args():
				var save := ConfigFile.new()
				save.set_value("run", "best_seconds", best)
				save.save("user://skyline.cfg")

func _process(delta: float) -> void:
	notice_time = maxf(0.0, notice_time - delta)
	if "--parkour-test" in OS.get_cmdline_user_args():
		return
	if Input.is_action_just_pressed("reset"):
		if finished:
			get_tree().reload_current_scene()
		else:
			player.reset_player()
	if Input.is_action_just_pressed("fps_toggle"):
		cap = 30 if cap == 144 else 144
		Engine.max_fps = cap

func collect_crystal(index: int) -> void:
	crystals[index] = true

func _on_fall() -> void:
	if not finished:
		falls += 1
	notice = "De vuelta al punto de control"
	notice_time = 2.5
