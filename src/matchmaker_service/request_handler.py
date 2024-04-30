from collections import deque
import time
import random
from schemas  import schemas
import matchmaker_service.skill as skill
from typing import List
from utils.constants import GameMode

class Listener:
    def __init__(self) -> None:
        self.ranked_ticket_stream = deque()
        self.practice_ticket_stream = deque()
        self.buffer_time = 30  # seconds
        self.team_size = 5
    
    def __get_buffer(self, stream: deque):
        current_time = time.time()
        buffer = [
            ticket
            for ticket in stream
            if current_time - ticket["timestamp"] <= self.buffer_time
        ]
        return buffer

    def add_ticket_to_stream(self, ticket: schemas.Ticket):
        match ticket.player_data["mode"]:
            case GameMode.PRACTICE:
                self.practice_ticket_stream.append(ticket)
            case GameMode.RANKED:
                self.ranked_ticket_stream.append(ticket)
    
    def process_practice_stream(self):
        # TODO
        pass
            
                

        

    def process_stream(self):
        while True:
            current_time = time.time()
            buffer =self.__get_buffer(self.ranked_ticket_stream)
            if len(buffer) >= 2 * self.team_size:
                team1, team2 = self.form_teams(buffer)
                
    def form_teams(self, ticket_batch):
        random.shuffle(ticket_batch)
        team1 = ticket_batch[:5]
        team2 = ticket_batch[5:]
        self.teams_formed.append((team1, team2))

    def assign_server(self, )
        