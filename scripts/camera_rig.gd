extends Node3D
@export var sensitivity: float = 0.003
@onready var pitch: Node3D = $Pitch
@onready var arm: SpringArm3D = $Pitch/SpringArm3D

func _ready() -> void:
	arm.add_excluded_object(get_parent().get_rid())
	if not "--test" in OS.get_cmdline_user_args() and not "--demo" in OS.get_cmdline_user_args() and not "--parkour-test" in OS.get_cmdline_user_args():
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _unhandled_input(event: InputEvent) -> void:
	if "--test" in OS.get_cmdline_user_args() or "--demo" in OS.get_cmdline_user_args() or "--parkour-test" in OS.get_cmdline_user_args():
		return
	if event is InputEventMouseMotion and Input.mouse_mode == Input.MOUSE_MODE_CAPTURED:
		# Mouse event already represents accumulated displacement: no delta here.
		rotation.y -= event.relative.x * sensitivity
		pitch.rotation.x = clampf(pitch.rotation.x - event.relative.y * sensitivity, -1.1, 0.25)
	if event is InputEventKey and event.pressed and event.keycode == KEY_ESCAPE:
		Input.mouse_mode = Input.MOUSE_MODE_VISIBLE
	if event is InputEventMouseButton and event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
		Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _process(delta: float) -> void:
	if "--test" in OS.get_cmdline_user_args() or "--demo" in OS.get_cmdline_user_args() or "--parkour-test" in OS.get_cmdline_user_args():
		return
	rotation.y += Input.get_axis("camera_right", "camera_left") * 1.8 * delta
	pitch.rotation.x = clampf(pitch.rotation.x + Input.get_axis("camera_down", "camera_up") * delta, -1.1, 0.25)

