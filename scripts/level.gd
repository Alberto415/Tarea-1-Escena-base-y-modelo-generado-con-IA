extends Node3D
@onready var player: CharacterBody3D = $Player
var cap: int = 144

func _ready() -> void:
	$HUD/Help.text = "WASD mover · Espacio saltar · R reiniciar\nRatón / flechas: cámara · Esc: liberar ratón\nF: 30 / 144 FPS · clic: capturar ratón"
	$HUD/Help.add_theme_constant_override("paragraph_spacing", 0)
	Engine.max_fps = cap
	if "--test" in OS.get_cmdline_user_args() or "--demo" in OS.get_cmdline_user_args():
		var runner = load("res://tests/acceptance.gd").new()
		add_child(runner)

func _process(_delta: float) -> void:
	$HUD/Status.text = "ESTADO  %s     |     %s\nVelocidad %.2f m/s  ·  FPS %d / %d" % [player.STATE_NAMES[player.state], "SUELO" if player.is_on_floor() else "AIRE", Vector2(player.velocity.x, player.velocity.z).length(), Engine.get_frames_per_second(), cap]
	if "--test" in OS.get_cmdline_user_args() or "--demo" in OS.get_cmdline_user_args():
		return
	if Input.is_action_just_pressed("reset"):
		player.reset_player()
	if Input.is_action_just_pressed("fps_toggle"):
		cap = 30 if cap == 144 else 144
		Engine.max_fps = cap
