from player import Player
from game_server import Game, GameType
from schemas import PlayerData


class Play:
    def __init__(self):
        self.game = Game()

    def play(self, name: str, mode: GameType):
        player_data = PlayerData(name=name, role_preference=[4, 2, 1, 0, 3])
        player = Player(player_data)
        outcome = self.game.request_match(player, mode)


Play().play("huleo", mode=GameType.PRACTICE)
