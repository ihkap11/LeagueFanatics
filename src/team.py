from skill import StatsCalculator
from player import Player
from typing import List
from schemas import TeamData


class Team:
    def __init__(self, team_data: TeamData):
        self.players = team_data.players
        self.size = team_data.size
        self.skill = team_data.skill
        self.uncertainty = team_data.uncertainty
        self.wins = team_data.wins

        if self.__validate_team_size():
            self.__set_team_stats(self.players)

    def __validate_team_size(self):
        return len(self.players) == self.size

    def __set_team_stats(self, players: List[Player]):
        self.skill, self.uncertainty = self.avg_team_stats(players)

    def __str__(self):
        return f"Team(Skill: {self.skill}, Uncertainty: {self.uncertainty}, Players: {self.players})"

    def __update_player_stats(self, team: "Team"):
        for player in team.players:
            player.skill = team.skill
            player.uncertainty = team.uncertainty

    def update_team_stats(self, team1: "Team", team2: "Team"):
        skill1, skill2 = team1.skill, team2.skill
        uncertainty1, uncertainty2 = team1.uncertainty, team2.uncertainty
        win1 = team1.wins
        (
            team1.skill,
            team2.skill,
            team1.uncertainty,
            team2.uncertainty,
        ) = StatsCalculator.update_stats(
            skill1, skill2, uncertainty1, uncertainty2, win1
        )
        self.__update_player_stats(team1)
        self.__update_player_stats(team2)

        return team1, team2

    def avg_team_stats(self, players: List[Player]):
        skill_sum = 0
        uncertainty_sum = 0
        for player in players:
            skill_sum += player.skill
            uncertainty_sum += player.uncertainty
        return skill_sum / len(players), uncertainty_sum / len(players)
