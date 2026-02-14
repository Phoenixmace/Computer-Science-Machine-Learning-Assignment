import asyncio
import websockets
import json

async def test():
    async with websockets.connect("ws://127.0.0.1:8765") as ws:
        await ws.send(json.dumps({"player_x": 0, "player_y": 0}))
        response = await ws.recv()
        print("Action received:", response)

asyncio.run(test())
