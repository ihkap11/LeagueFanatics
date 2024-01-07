from player import Player, player_db
from team import Team
import random
from typing import List
from skill import StatsCalculator
from enum import Enum
from schemas import PlayerData


class GameType(Enum):
    PRACTICE = 0
    RANKED = 1


class Game:
    def __init__(self):
        self.matchmaker = Matchmaking("practice")
        self.ranked_queue = []

    def __is_queue_ready(self, queue: List):
        return len(queue) > 10

    def request_match(self, player: Player, mode: GameType):
        match mode:
            case GameType.PRACTICE:
                outcome = self.matchmaker.simulate_match(player, mode)
            case GameType.RANKED:
                self.ranked_queue.append(player)
                if self.__is_queue_ready(self.ranked_queue):
                    outcome = self.matchmaker.simulate_match(player, mode)

    def update_player_stats(self):
        return


class Matchmaking:
    def __init__(self, mode: GameType, team_size: int = 5):
        self.mode = mode
        self.team_size = team_size

    def __set_match_mode(self, mode: GameType):
        self.mode = mode

    def __create_bot_team(self, player: Player, all_bots: bool = False):
        skill = player.skill
        uncertainty = player.uncertainty
        team_size = self.team_size

        if all_bots:
            players = []
        else:
            players = [player]
            team_size -= 1

        for i in range(team_size):
            bot_player = Player(
                PlayerData(name=f"bot_{i}", skill=skill, uncertainty=uncertainty)
            )
            players.append(bot_player)
        return Team(players=players)

    def __match_outcome(self, team1: Team, team2: Team):
        if random.choice([True, False]):
            team1.wins = True
            team2.wins = False
        else:
            team1.wins = False
            team2.wins = True

    def simulate_match(self, player: Player, mode: GameType):
        self.__set_match_mode(mode=mode)
        match mode:
            case GameType.PRACTICE:
                return self.calliberate_player(player)
            case GameType.RANKED:
                return self.launch_ranked_game(player)

    def calliberate_player(self, player: Player, calliberation_rounds: int = 10):
        for i in range(calliberation_rounds):
            # add game history
            self.launch_practice_game(player)
            print(f"Match {i}")
        return True

    def launch_practice_game(self, player: Player):
        # create team for player
        team1 = self.__create_bot_team(player)
        team2 = self.__create_bot_team(player, all_bots=True)
        self.__match_outcome(team1, team2)
        updated_team1, updated_team2 = Team().update_team_stats(team1, team2)

        print(updated_team1)
        print(updated_team2)

    def launch_ranked_game(self, player: Player):
        return True
