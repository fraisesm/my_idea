import asyncio
import websockets
import json
import random
from datetime import datetime
import uuid

URI = "ws://localhost:8000/ws/{team_id}"

async def emulate_team(team_id: str):
    async with websockets.connect(URI.format(team_id=team_id)) as websocket:
        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)
                
                if data["type"] == "task":
                    await asyncio.sleep(random.uniform(1, 5))
                    
                    solution = {
                        "type": "solution",
                        "task_id": data["task_id"],
                        "solution": {
                            "selections": [
                                {
                                    "type": "ЛОГИЧЕСКАЯ ОШИБКА",
                                    "startSelection": random.randint(0, 100),
                                    "endSelection": random.randint(100, 500)
                                }
                            ]
                        }
                    }
                    
                    await websocket.send(json.dumps(solution))
                    
            except websockets.exceptions.ConnectionClosed:
                print(f"Team {team_id} disconnected, reconnecting...")
                await asyncio.sleep(5)
                continue

if __name__ == "__main__":
    team_id = str(uuid.uuid4())
    print(f"Starting emulator for team {team_id}")
    asyncio.get_event_loop().run_until_complete(emulate_team(team_id))