from src.utils.constants import GameMode

class Matchmaking:
    def __init__(self, mode: GameMode):
        self.game = self.__get_game(mode)
        self.team_size = 5
    
    def __get_game(self, mode: GameMode):
        match self.mode:
            case GameMode.CALLIBERATION:
                game = PracticeGame()
            case GameMode.PRACTICE:
                game = PracticeGame()
            case GameMode.RANKED:
                game = PracticeGame()
    
    
    def match(self, player: Player):
        match self.mode:
            case GameMode.CALLIBERATION:
                outcome = self.matchmaker.launch_practice_game(player)
            case GameMode.PRACTICE:
                outcome = self.matchmaker.launch_practice_game(player)
            case GameMode.RANKED:
                self.ranked_queue.append(player)
                if self.__is_queue_ready(self.ranked_queue):
                    outcome = self.matchmaker.launch_ranked_game(player)

    def update_player_stats(self):
        return



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
        return Team(team_data=TeamData(players=players, wins=False))

    def __match_outcome(self, team1: Team, team2: Team):
        if random.choice([True, False]):
            return 
        else:
            team1.wins = False
            team2.wins = True
  team1 = self.__create_bot_team(player)
        team2 = self.__create_bot_team(player, all_bots=True)
        winning_team = self.__match_outcome(team1, team2)
        updated_team1, updated_team2 = team1.update_team_stats(team1, team2)
    def launch_practice_game(self, player: Player):
        # create team for player
      

        return updated_team1, updated_team2

    def launch_ranked_game(self, player: Player):
        return True
