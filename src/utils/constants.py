from enum import Enum


class GameMode(Enum):
    PRACTICE = 0
    RANKED = 1


class Roles(Enum):
    TOP = 0
    MID = 1
    BOT = 2
    SUPPORT = 3
    JUNGLE = 4


class DBLoc(Enum):
    PLAYER = "src/database/db.yaml"
