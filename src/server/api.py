from fastapi import FastAPI, WebSocket, HTTPException, WebSocketDisconnect
from websocketconnector import WebSocketConnectionManager
from queue import PriorityQueue
from loguru import logger
from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4, UUID
import time


# Models
class Player(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    mmr: float


class Team(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    players: List[Player]


class Match(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    teams: List[UUID]
    state: str


class QueueManager:
    def __init__(self, player_queue: PriorityQueue = PriorityQueue()) -> None:
        self.player_queue = player_queue

    def queue_size(self):
        return self.player_queue.qsize()

    def enqueue_player(self, player_name: str) -> None:
        """Creates a ticket for the player and adds the player to the queue for matchmaking.
            - create player object
            - create player ticket
            - enqueue player for matchmaking

        Args:
            player_name (str): Player name as (unique) identifier for the player
        """
        # TODO: add database to fetch mmr
        player = Player(name=player_name, mmr=10)
        self.player_queue.put((int(time.time()), player))

    def dequeue_player(self) -> None:
        """Priority player from player queue for matchmaking.

        Args:
            player_name (str): Unique identifier representing player.
        """
        return self.player_queue.get()[1]

    def drop_player(self) -> None:
        """Drop player from the queue."""
        pass


class MatchManager:
    """
    - maintains player queue
    - creates teams (team_id)
    - assigns team a match (match_id)
    """

    def __init__(self) -> None:
        self.MIN_PLAYERS_FOR_MATCH = 4
        self.MIN_PLAYERS_FOR_TEAM = 2

    def ready_for_match(self):
        return queue_manager.queue_size() >= self.MIN_PLAYERS_FOR_MATCH

    async def create_teams(self):
        team_mates = [
            queue_manager.dequeue_player() for _ in range(self.MIN_PLAYERS_FOR_TEAM)
        ]
        new_team = Team(players=team_mates)
        return new_team


player_match_queue = PriorityQueue()
conn_manager = WebSocketConnectionManager()
queue_manager = QueueManager()
match_manager = MatchManager()

# simulated DB
players = {}
teams = {}
matches = {}

MMR_RANGE = [10, 20]

app = FastAPI()


@app.get("/")
def health():
    return "[HEALTH CHECK] Up and running!"


# API routers
@app.put("/players/{player_name}")
def register_player(player_name: str):
    player = Player(name=player_name, mmr=50.0)
    if player.name in players:
        raise HTTPException(
            status_code=400, detail="Player with this ID already exists."
        )
    players[player.name] = player
    return {
        "message": "Player registered successfully",
        "player_name": player.name,
        "player_name": player.id,
        "player_data": player.model_dump_json(),
    }


@app.get("/players/{player_name}")
def get_player(player_name: str):
    player = players.get(player_name)
    if not player:
        raise HTTPException(status_code=404, detail="Player not found")
    return player


@app.websocket("/players/{player_name}/ws")
async def play(websocket: WebSocket, player_name: str):
    client_host = websocket.client.host
    client_port = websocket.client.port
    print("INSIDE")
    logger.info(
        f"[Connecting ...] Player {player_name} from IP {client_host}:{client_port}"
    )

    logger.info(f"[ACTIVE CONNECTIONS]: {conn_manager.active_connections}")
    try:
        player = players.get(player_name)
        if not player:
            logger.warn(f"Player {player_name} doesn't exist. Closing websocket.")
            await websocket.close(code=4000)
            return
        await conn_manager.connect(websocket, player_name)
        await websocket.send_text(f"Connected to server as player: {player_name}")
        logger.info(
            f"[Team Assignment] Player {player_name} from IP {client_host}:{client_port}"
        )

        queue_manager.enqueue_player(player_name)

        if match_manager.ready_for_match():
            team = await match_manager.create_teams()
            logger.info(f"[Team Assigned] {team}")
            for player in team.players:
                player_name = player.name
                logger.info(f"[ACTIVE CONNECTIONS]: {conn_manager.active_connections}")
                logger.info(f"{player_name}")
                await websocket.send_text(str(team.id))
                await conn_manager.send_message(
                    {
                        "message": f"You {player_name} are assigned to the team {team.id}",
                    },
                    player_name,
                )
    except WebSocketDisconnect:
        logger.info(f"Player {player_name} disconnected")


# class GameManager:-
#     """
#     - match details (match_id, teams, players)
#     - match result
#     - update_player_stats
#     """
