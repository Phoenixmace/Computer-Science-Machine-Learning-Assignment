import asyncio
import websockets
import json
import random
async def debug_enemy_movement(args):
    return { "x": random.randint(-1, 1), "y": random.randint(-1, 1)}
async def move_player(args):
    print("Moving player to:", args)
    # Do your logic here
    return {"status": "ok"}

# Dispatcher: map function names to Python functions
FUNCTIONS = {
    "move_player": move_player,
    "debug_enemy_movement":debug_enemy_movement
}

async def handle_connection(ws):
    async for message in ws:
        data = json.loads(message)
        func_name = data.get("function")
        args = data.get("args", {})

        if func_name in FUNCTIONS:
            result = await FUNCTIONS[func_name](args)
        else:
            result = {"error": "Unknown function"}

        await ws.send(json.dumps(result))

async def main():
    async with websockets.serve(handle_connection, "127.0.0.1", 8765):
        print("Server running...")
        await asyncio.Future()

asyncio.run(main())