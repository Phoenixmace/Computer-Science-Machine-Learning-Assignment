extends CharacterBody2D


@export var speed := 150
@export var max_health := 3
@export var hit_cooldown := 0.2

var health := max_health
@export var ACCELERATION := 3
@export var DECELERATION_FACTOR := 0.3
var DECELERATION := ACCELERATION * DECELERATION_FACTOR
@export var MAX_SPEED := 30
@export var DAMAGE := 10

var python_request_interval = 0.1
var current_request_cooldown = 0.0
var current_hit_cooldown = 0.0


@onready var movement_vector := Vector2.ZERO
@onready var controller = get_node("../PythonController")
@onready var game = get_node("../Game")
var previous_distance = 0.0



func _physics_process(delta: float) -> void:
	current_request_cooldown -= delta
	if current_hit_cooldown > 0:
		current_hit_cooldown -= delta
	if current_request_cooldown <=0:
		current_request_cooldown = python_request_interval
		var data = get_current_game_state_for_python(movement_vector) # data is a String
		var recieved_vector = controller.send_request("enemy_movement", data)
		print(recieved_vector)
		#recieved_vector = Vector2(int(Input.is_action_pressed("D"))-int(Input.is_action_pressed("A")), int(Input.is_action_pressed("W")) - int(Input.is_action_pressed("S")))
		if recieved_vector:
			var dict = str_to_var(recieved_vector)     # dict is a Dictionary
			recieved_vector = str_to_var(recieved_vector)
			movement_vector = get_new_movement_vector(movement_vector,delta, Vector2(int(recieved_vector["x"]), int(recieved_vector["y"])))
	else:
		move_and_slide()
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
	for i in range(get_slide_collision_count()):
		var collision = get_slide_collision(i)
		var collider = collision.get_collider()
		if collider.name == "Player" and current_hit_cooldown < 0.01:
			_hit_player(collider)
			current_hit_cooldown = hit_cooldown
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
# Notes: Borders, player pos, player vector, enemy, position, enemy movement vector
func get_current_game_state_for_python(movement_vector):
#region Observations
	var level_name = get_tree().current_scene.name
	var global = global_position
	var player = get_node("../Player")
	var player_coords =  player.global_position - global 
	var player_movement_vector = player.movement_vector
#endregion
	
	
	var reward = previous_distance - player_coords.length()
	previous_distance = player_coords.length()
	var data = {"observation":{"player_relative":player_coords,
	"player_vector":player_movement_vector,
	"global_position":global_position, 
	"enemy_vector":movement_vector}, 
	"previous_reward":reward,
	"level_name":level_name,
	"type":"melee",
	"number":"0"}
	
	return data


func _hit_player(player) -> void:
	player.recieve_damage(DAMAGE) # Replace with function body.
