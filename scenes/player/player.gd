extends CharacterBody2D


const ACCELERATION := 20
const DECELERATION := ACCELERATION *0.75
const MAX_SPEED := 40

@onready var movement_vector := Vector2.ZERO

func _physics_process(delta: float) -> void:
	movement_vector = get_new_movement_vector(movement_vector,delta)
	global_position = global_position + movement_vector
	pass


################### movement
func get_new_movement_vector(current_vector: Vector2, delta: float) -> Vector2:
	
#region Horizontal Movement
	var horizontal_movement = (int(Input.is_action_pressed("D")) - int(Input.is_action_pressed("A"))) # direction
	# no input
	if horizontal_movement == 0:
		if current_vector.x > 0:
			current_vector.x = max(current_vector.x - DECELERATION, 0)
		elif current_vector.x < 0:
			current_vector.x = min(current_vector.x + DECELERATION, 0)
	else: # input
		var new_horizontal_movement = (horizontal_movement * ACCELERATION) + current_vector.x
		if abs(new_horizontal_movement) > MAX_SPEED:
			current_vector.x = horizontal_movement * MAX_SPEED
		else:
			current_vector.x = new_horizontal_movement
#endregion
#region Vertical Movement
	var vertical_movement = (int(Input.is_action_pressed("S")) - int(Input.is_action_pressed("W"))) # direction
	# no input
	if vertical_movement == 0:
		if current_vector.y > 0:
			current_vector.y = max(current_vector.y - DECELERATION, 0)
		elif current_vector.y < 0:
			current_vector.y = min(current_vector.y + DECELERATION, 0)
	else: # input
		var new_horizontal_movement = (vertical_movement * ACCELERATION) + current_vector.y
		if abs(new_horizontal_movement) > MAX_SPEED:
			current_vector.y = vertical_movement * MAX_SPEED
		else:
			current_vector.y = new_horizontal_movement
#endregion
	print(current_vector.length())
	return current_vector
