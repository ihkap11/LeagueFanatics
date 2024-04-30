from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
import random
from queue import PriorityQueue
import time
from typing import Dict

app = FastAPI()
STATUS = ["main menu", "teaming up", "matchmaking", "playing"]


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, player_id: str):
        await websocket.accept()
        self.active_connections[player_id] = websocket
        print(f"[CONNECTED] Player {player_id}")
        print(len(self.active_connections.keys()))

    def disconnect(self, player_id: str):
        if player_id in self.active_connections:
            del self.active_connections[player_id]
            print(f"[DISCONNECTED] Player {player_id}")

    async def send_personal_message(self, message: str, player_id: str):
        print(self.active_connections)
        if player_id in self.active_connections:
            try:
                await self.active_connections[player_id].send_text(message)
                print(f"[MESSAGE SENT] To {player_id}: {message}")
            except Exception as e:
                print(f"Error sending message to {player_id}: {str(e)}")


manager = ConnectionManager()


@app.websocket("/ws/{player_id}")
async def websocket_endpoint(websocket: WebSocket, player_id: str):
    await manager.connect(websocket, player_id)
    message = await websocket.receive_text()
    try:
        while True:
            message = await websocket.receive_text()
            print(f"[RECEIVED] From {player_id}: {message}")
            queue_player(player_id)
    except WebSocketDisconnect:
        manager.disconnect(player_id)


@app.get("/")
def health_check():
    return {"status": "Server running"}


class Player(BaseModel):
    player_id: str


pq = PriorityQueue()


@app.post("/queue_player")
async def queue_player(player: Player):
    pq.put((time.time(), player.player_id))
    print(f"[QUEUED] Player {player.player_id}")
    await manager.send_personal_message(
        f"Player {player.player_id} queued. Running queue count {pq}", player.player_id
    )
    return {"status": "Player queued"}


@app.get("/create_teams")
async def attempt_create_teams():
    team_size = 5
    if pq.qsize() >= team_size:
        team = []
        while len(team) < team_size:
            _, player_id = pq.get()
            team.append(player_id)
        print(f"[TEAM CREATED] {team}")
        for player_id in team:
            print("[SENDING...]", manager.active_connections.keys())
            await manager.send_personal_message(f"Your team: {team}", player_id)


@app.get("/player_status/{player_id}")
async def player_status(player_id: str):
    status = random.choice(STATUS)
    await manager.send_personal_message(f"Your status: {status}", player_id)
    return {"status": status}
