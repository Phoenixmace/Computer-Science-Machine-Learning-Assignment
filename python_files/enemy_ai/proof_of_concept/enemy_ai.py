import random
def poc_enemy_movement(args):
    print(args)
    return {"x": random.randint(-1, 1), "y": random.randint(-1, 1)}