extends Node2D


# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	start_dev_scene()
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass


################################################### -Dev
func start_dev_scene():
	get_tree().call_deferred("change_scene_to_file", "res://scenes/levels/dev_level/dev_level.tscn")
