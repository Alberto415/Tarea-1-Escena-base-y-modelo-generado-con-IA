extends Area3D
@export var index: int = 0
var age: float = 0.0
var collected: bool = false

func _ready() -> void:
	body_entered.connect(_collect)

func _process(delta: float) -> void:
	age += delta
	$Gem.rotation.y += delta * 1.8
	$Gem.position.y = sin(age * 2.6) * 0.12

func _collect(body: Node3D) -> void:
	if collected or not body is CharacterBody3D:
		return
	collected = true
	$Gem.hide()
	get_tree().current_scene.collect_crystal(index)
