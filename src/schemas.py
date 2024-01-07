import uuid
from pydantic import BaseModel, Field
from typing import List, Optional
from player import Player


class PlayerData(BaseModel):
    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    skill: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    level: Optional[int] = 0
    role_preference: Optional[List[int]] = []


class TeamData(BaseModel):
    class Config:
        arbitrary_types_allowed = True

    players: List[Player] = []
    size: int = 5
    skill: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    wins: bool
