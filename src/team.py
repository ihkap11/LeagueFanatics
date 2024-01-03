from skill import StatsCalculator
from player import Player


class Team:
    def __init__(
        self,
        players: Player = None,
        size: int = 5,
        skill=None,
        wins=None,
        uncertainty=None,
    ):
        self.players = players
        self.size = size
        self.skill = skill
        self.uncertainty = uncertainty
        self.wins = wins
        if self.__validate_team_size:
            self.__set_team_stats(self.players)

    def __validate_team_size(self):
        return len(self.players) == self.size

    def __set_team_stats(self, players):
        self.skill, self.uncertainty = StatsCalculator.avg_team_stats(players)

    def __players_str_(self):
        for player in self.players:
            print(player.__str__())

    def __str__(self):
        return f"Team(Skill: {self.skill}, Uncertainty: {self.uncertainty}"
