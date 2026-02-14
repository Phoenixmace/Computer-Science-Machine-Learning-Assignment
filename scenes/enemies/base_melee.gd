extends CharacterBody2D

@export var speed := 150
@export var max_health := 3

var health := max_health
@export var ACCELERATION := 2
@export var DECELERATION_FACTOR := 0.3
var DECELERATION := ACCELERATION * DECELERATION_FACTOR
@export var MAX_SPEED := 20

@onready var movement_vector := Vector2.ZERO
@onready var controller = get_node("../PythonController")

func _physics_process(delta: float) -> void:
	var data = '{ "a": 1, "b": 2 }' # data is a String
	var recieved_vector = controller.send_request("debug_enemy_movement", {})
	
	if recieved_vector:
		var dict = str_to_var(recieved_vector)     # dict is a Dictionary
		recieved_vector = str_to_var(recieved_vector)
		movement_vector = get_new_movement_vector(movement_vector,delta, Vector2(int(recieved_vector["x"]), int(recieved_vector["y"])))
		global_position = global_position + movement_vector

	pass


################### movement
#region Movement
func get_new_movement_vector(current_vector: Vector2, delta: float, recieved_vector:Vector2) -> Vector2:
	
#region Horizontal Movement
	var horizontal_movement = recieved_vector.x # direction
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
	var vertical_movement = recieved_vector.y # direction
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

	move_and_slide()
	for i in get_slide_collision_count():
		var collision = get_slide_collision(i)
		var collision_vector =   Vector2(-0.8, -0.8)
		if collision.get_normal().x == 0:
			collision_vector.x = 1
		if collision.get_normal().y == 0:
			collision_vector.y = 1
		current_vector *= collision_vector
		
#region cap speed
	# snap vector to max length
	if current_vector.length() > MAX_SPEED:
		current_vector = (current_vector.normalized() * Vector2(MAX_SPEED, MAX_SPEED)).round()
#endregion
	
	return current_vector
#endregion

################### python
func get_current_game_state_for_python():
	var data = {}
	return 0
