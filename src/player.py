import yaml
import uuid
from skill import TrueSkill
from player_db import PlayerDB

player_db = PlayerDB()


class Player:
    def __init__(
        self,
        name,
        db=player_db.db,
        id=None,
        skill=None,
        uncertainty=None,
        level=None,
        role_preference=None,
    ):
        self.db = db
        self.name = name
        self.id = id if id is not None else uuid.uuid4()
        self.skill = skill
        self.uncertainty = uncertainty
        self.level = level
        self.role_preference = role_preference

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
        self.skill, self.uncertainty, self.level = TrueSkill().new_player_skill()
        self.__save_player_details()

    def load_existing_player(self):
        existing_player_data = self.db["Players"][self.name]
        self.skill = existing_player_data["skill"]
        self.uncertainty = existing_player_data["uncertainty"]
        self.level = existing_player_data["level"]
        self.role_preference = existing_player_data["role_preference"]

    def set_role_preference(self, role_preference):
        self.role_preference = role_preference

    def __str__(self):
        return (
            f"Player(Name: {self.name}, ID: {self.id}, "
            f"Skill: {self.skill}, Uncertainty: {self.uncertainty}, "
            f"Level: {self.level}, Role Preference: {self.role_preference})"
        )


# pl = Player("jamie")
# pl.set_role_preference([4, 2, 1, 0, 3])
# print(pl.__str__())
