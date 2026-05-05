extends MarginContainer

@export var game:Node2D
@export var hp_bar:TextureProgressBar
func _on_exit_game_pressed() -> void:
	game.end_game()
	pass # Replace with function body.
func update_player_life(current, total) -> void:
	hp_bar.max_value = total
	hp_bar.value = current
