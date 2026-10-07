extends Node3D
## Cosmetic rigid-part animation. Never changes the capsule or movement.
var phase: float = 0.0
@onready var body: Node3D = $Body
@onready var actor: CharacterBody3D = get_parent()

func _process(delta: float) -> void:
	var moving: float = Vector2(actor.velocity.x, actor.velocity.z).length() / 6.0
	phase += delta * (3.0 + moving * 10.0)
	var airborne: bool = not actor.is_on_floor()
	var stride: float = sin(phase) * 0.65 * moving
	var blend: float = 1.0 - exp(-16.0 * delta)
	$Body/LeftLeg.rotation.x = lerpf($Body/LeftLeg.rotation.x, -0.48 if airborne else stride, blend)
	$Body/RightLeg.rotation.x = lerpf($Body/RightLeg.rotation.x, 0.45 if airborne else -stride, blend)
	$Body/LeftArm.rotation.x = lerpf($Body/LeftArm.rotation.x, -1.0 if airborne else -stride, blend)
	$Body/RightArm.rotation.x = lerpf($Body/RightArm.rotation.x, -1.0 if airborne else stride, blend)
	body.rotation.x = lerpf(body.rotation.x, -0.10 * moving if not airborne else 0.05, blend)
	$Body/Scarf.rotation.x = sin(phase * 0.8) * 0.1 + moving * 0.3
