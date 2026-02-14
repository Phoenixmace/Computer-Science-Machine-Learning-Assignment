extends Camera2D

const start_coords := Vector2(1024, 1024)
const start_zoom := Vector2(0.6, 0.6)
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	position = start_coords
	zoom = start_zoom
	pass # Replace with function body.


# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass
