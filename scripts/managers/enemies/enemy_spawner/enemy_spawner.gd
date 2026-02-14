extends Node2D

@export var enemy_scene: PackedScene       # Assign your enemy scene here
@export var spawn_points: Array[Node2D]    # Optional: array of Position2D nodes
@export var spawn_interval := 100.0          # seconds between spawns
@export var max_enemies := 10

var current_enemies: Array = []
var spawn_timer := 100.0

func _ready() -> void:
	pass
func _process(delta):
	spawn_timer += delta

	# Check if we can spawn
	if spawn_timer >= spawn_interval and current_enemies.size() < max_enemies:
		spawn_enemy()
		
		spawn_timer = 0.0

	# Clean up dead enemies
	current_enemies = current_enemies.filter(func(e):
		return is_instance_valid(e)
	)

func spawn_enemy():
	if spawn_points.size() == 0:
		return

	# Pick a random spawn point
	var point = spawn_points[randi() % spawn_points.size()]
	
	# Instance the enemy
	var enemy = enemy_scene.instantiate()
	enemy.global_position = point.global_position
	get_parent().add_child(enemy)

	current_enemies.append(enemy)
