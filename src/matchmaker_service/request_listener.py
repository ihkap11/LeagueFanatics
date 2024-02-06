from collections import deque
import time
import random


class Listener:
    def __init__(self) -> None:
        self.player_stream = deque()
        self.buffer_time = 30  # seconds
        self.teams_formed = []

    def add_ticket_to_stream(self, ticket):
        self.player_stream.append(ticket)

    def process_stream(self):
        while True:
            current_time = time.time()
            buffer = [
                player
                for player in self.player_stream
                if current_time - player["timestamp"] <= self.buffer_time
            ]
            if len(buffer) >= 10:
                self.form_teams(buffer[:10])
                for player in buffer[:10]:
                    self.player_stream.remove(player)

    def form_teams(self, players):
        random.shuffle(players)
        team1 = players[:5]
        team2 = players[5:]
        self.teams_formed.append((team1, team2))
