extends CharacterBody3D
## Physics owns position/velocity. Imported appearance never controls collisions.
signal state_changed(previous: String, current: String)
signal fell
signal physics_stepped
enum State { IDLE, WALK, JUMP }
const STATE_NAMES := ["Idle", "Walk", "Jump"]
@export var speed: float = 5.0
@export var acceleration: float = 22.0
@export var gravity: float = 22.0
@export var jump_speed: float = 8.0
var state: State = State.IDLE
var jump_count: int = 0
var desired_direction := Vector3.ZERO
var visual_time: float = 0.0
var respawn_position := Vector3(0, 0.05, 6)
@onready var visual: Node3D = $Visual
@onready var rig: Node3D = $CameraRig

func _physics_process(delta: float) -> void:
	var input := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
	# Yaw-only camera basis: looking up/down never changes ground speed.
	desired_direction = rig.global_basis * Vector3(input.x, 0.0, input.y)
	desired_direction.y = 0.0
	desired_direction = desired_direction.limit_length(1.0)
	# Acceleration (m/s²) becomes a change in velocity (m/s) once.
	velocity.x = move_toward(velocity.x, desired_direction.x * speed, acceleration * delta)
	velocity.z = move_toward(velocity.z, desired_direction.z * speed, acceleration * delta)
	if not is_on_floor():
		velocity.y -= gravity * delta
	elif Input.is_action_just_pressed("jump"):
		velocity.y = jump_speed # Impulse in m/s, never multiplied by delta.
		jump_count += 1
	move_and_slide() # Internally integrates velocity using the physics timestep.
	_update_state()
	physics_stepped.emit()
	if position.y < -12.0:
		fell.emit()
		reset_player()

func _update_state() -> void:
	var next: State = State.JUMP if not is_on_floor() else (State.WALK if Vector2(velocity.x, velocity.z).length() > 0.1 else State.IDLE)
	if next == state:
		return
	# Explicit legal transitions; Jump includes jumping and falling.
	var allowed := {State.IDLE: [State.WALK, State.JUMP], State.WALK: [State.IDLE, State.JUMP], State.JUMP: [State.IDLE, State.WALK]}
	assert(next in allowed[state])
	var previous: String = STATE_NAMES[state]
	state = next
	state_changed.emit(previous, STATE_NAMES[state])
	print("FSM: %s -> %s" % [previous, STATE_NAMES[state]])

func _process(delta: float) -> void:
	# Render-only orientation and modest whole-model bob; no skeletal clips claimed.
	visual_time += delta
	if desired_direction.length_squared() > 0.01:
		visual.rotation.y = lerp_angle(visual.rotation.y, atan2(-desired_direction.x, -desired_direction.z), 1.0 - exp(-14.0 * delta))
	visual.position.y = sin(visual_time * 12.0) * 0.025 if state == State.WALK else 0.0

func reset_player(at: Vector3 = Vector3.INF) -> void:
	position = respawn_position if at == Vector3.INF else at
	velocity = Vector3.ZERO
	reset_physics_interpolation()
