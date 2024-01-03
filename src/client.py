from player import Player
from game_server import Game, GameType


class Play:
    def __init__(self):
        self.game = Game()

    def play(self, name: str, mode: GameType):
        player = Player(name)
        player.set_role_preference([4, 2, 1, 0, 3])

        # print(player.__str__())

        outcome = self.game.request_match(player, mode)


Play().play("huleo", mode=GameType.PRACTICE)
