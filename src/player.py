import uuid
from skill import StatsCalculator
from player_db import PlayerDB
from typing import List, Optional
from schemas import PlayerData
from pydantic import BaseModel, Field
import uuid


class PlayerData(BaseModel):
    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    skill: Optional[float] = 0.0
    uncertainty: Optional[float] = 0.0
    level: Optional[int] = 0
    role_preference: Optional[List[int]] = []


player_db = PlayerDB()


class Player(BaseModel):
    db: Optional[dict] = None
    name: str
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    skill: Optional[float] = None
    uncertainty: Optional[float] = None
    level: Optional[int] = None
    role_preference: Optional[List[int]] = None

    def __init__(self, player_data: PlayerData, db=player_db.db, **kwargs):
        super().__init__(**player_data.dict(), db=db, **kwargs)
        if self.__is_new_player():
            self.enroll_new_player()
        else:
            self.load_existing_player()

    def __is_new_player(self):
        player_list = list(self.db["Players"].keys())
        return self.name not in player_list

    def __save_player_details(self):
        self.db["Players"][self.name] = {
            "id": str(self.id),
            "skill": self.skill,
            "uncertainty": self.uncertainty,
            "level": self.level,
            "role_preference": self.role_preference,
        }
        player_db.save_db(self.db)

    def enroll_new_player(self):
        """
        New player should have
        - name : str
        - id : uuid
        - default skill
        - default uncertainty
        - default level
        """
        self.id = uuid.uuid4()
        self.role_preference = None
        self.skill, self.uncertainty, self.level = StatsCalculator.new_player_skill()
        self.__save_player_details()

    def load_existing_player(self):
        existing_player_data = self.db["Players"][self.name]
        self.skill = existing_player_data["skill"]
        self.uncertainty = existing_player_data["uncertainty"]
        self.level = existing_player_data["level"]
        self.role_preference = existing_player_data["role_preference"]

    def set_role_preference(self, role_preference: List[int]):
        self.role_preference = role_preference

    def __repr__(self):
        return (
            f"Player(Name: {self.name}, ID: {self.id}, "
            f"Skill: {self.skill}, Uncertainty: {self.uncertainty}, "
            f"Level: {self.level}, Role Preference: {self.role_preference})"
        )


# pl = Player("jamie")
# pl.set_role_preference([4, 2, 1, 0, 3])
# print(pl.__str__())
