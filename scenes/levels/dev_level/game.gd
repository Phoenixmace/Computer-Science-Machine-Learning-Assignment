extends Node2D


@export var python_controller:Node2D
func end_game():
	python_controller.close_game()
	get_tree().quit()
