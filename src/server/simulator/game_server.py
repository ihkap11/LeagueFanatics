from player import Player, player_db
from team import Team, TeamData
import random
from typing import List
from src.game_server.matchmaking.trueskill import StatsCalculator
from enum import Enum
from schemas import PlayerData
from src.utils.constants import GameMode


class Game:
    def __init__(self):
        """
        TODO: Add properties for game simulation
        """
        return

    def __is_queue_ready(self, queue: List):
        return len(queue) > 10

    def __is_player_calliberated(self, player: Player):
        return player.level > 10

    def play_outcome(self, team1: TeamData, team2: TeamData):
        """
        TODO: Add logic for game simulation
        """
        return random.choice(0, 1)


class PracticeGame(Game):
    def __init__(self):
        super().__init__()

    def assign_player_team(self, player: PlayerData):
        skill = player.skill
        uncertainty = player.uncertainty
        team_size = self.team_size

        players = [player]
        team_size -= 1
        for i in range(team_size):
            AI_player = Player(
                PlayerData(name=f"AI_{i}", skill=skill, uncertainty=uncertainty)
            )
            players.append(AI_player)
        return Team(team_data=TeamData(players=players))

    def assign_opponent_team(self, player: PlayerData):
        skill = player.skill
        uncertainty = player.uncertainty
        team_size = self.team_size
        players = []
        team_size -= 1
        for i in range(team_size):
            AI_player = Player(
                PlayerData(name=f"AI_{i}", skill=skill, uncertainty=uncertainty)
            )
            players.append(AI_player)
        return Team(team_data=TeamData(players=players))

    def play(self, player: PlayerData):
        team1 = self.assign_player_team(player)
        team2 = self.assign_opponent_team(player)
        return self.play_outcome(team1, team2)


class RankedGame(Game):
    def __init__(self):
        super().__init__()

    def assign_player_team(self, player: PlayerData):
        skill = player.skill
        uncertainty = player.uncertainty
        team_size = self.team_size

        players = [player]
        team_size -= 1
        for i in range(team_size):
            AI_player = Player(
                PlayerData(name=f"AI_{i}", skill=skill, uncertainty=uncertainty)
            )
            players.append(AI_player)
        return Team(team_data=TeamData(players=players))

    def assign_opponent_team(self, player: PlayerData):
        skill = player.skill
        uncertainty = player.uncertainty
        team_size = self.team_size
        players = []
        team_size -= 1
        for i in range(team_size):
            AI_player = Player(
                PlayerData(name=f"AI_{i}", skill=skill, uncertainty=uncertainty)
            )
            players.append(AI_player)
        return Team(team_data=TeamData(players=players))

    def play(self, player: PlayerData):
        team1 = self.assign_player_team(player)
        team2 = self.assign_opponent_team(player)
        return self.play_outcome(team1, team2)
