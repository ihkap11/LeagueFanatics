from pydantic import BaseModel, Field
import uuid
from datetime import datetime
from typing import List, Optional
from utils.constants import Roles


class PlayerData(BaseModel):
    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    skill: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    level: Optional[int] = 0
    role_preference: Optional[List[int]] = []


class Ticket(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    mode: str
    creation_time: datetime
    player_data: PlayerData


class TeamMates(BaseModel):
    player_id: uuid.UUID
    skill: int
    uncertainty: float
    level: int
    assigned_role: Roles
    is_human: bool


class Match(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    ticket_id: str
    creation_time: datetime
    team1: List
    team2: List
    outcome: str


class TeamData(BaseModel):
    players: List[TeamMates] = []
    size: int = 5
    skill: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    wins: bool
