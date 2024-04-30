import random
from utils.constants import Roles, GameMode
from schemas import schemas
import uuid
from database import datetime


class TeamBuilder:
    def __init__(self) -> None:
        self.team_size = 5

    def __team_member(self, player: schemas.PlayerData, is_human: bool):
        return schemas.TeamMates(
            player_id=player["id"],
            skill=player["skill"],
            uncertainty=player["uncertainty"],
            level=player["level"],
            assigned_role=Roles(player["role_preference"][0]),
            is_human=is_human,
        )

    def __generate_ai_player(self, player: schemas.PlayerData, idx: int):
        return schemas.PlayerData(
            name=f"ai_{Roles(idx)}",
            skill=player["skill"],
            uncertainty=player["uncertainty"],
            level=player["level"],
            role_preference=[idx],
        )

    def assign_practice_team_pair(self, player: schemas.PlayerData):
        team1 = []
        team1.append(self.__team_member(player, True))
        for i in range(1, self.team_size):
            ai_player = self.__generate_ai_player(player, i)
            team1.append(self.__team_member(ai_player, False))

        team2 = []
        for i in range(self.team_size):
            ai_player = self.__generate_ai_player(player, i)
            team2.append(self.__team_member(ai_player, False))

        return team1, team2


class Matchmaker:
    def __init__(self) -> None:
        self.team_builder = TeamBuilder()

    def __generate_match_id(self):
        return uuid.uuid4

    def practice_match(self, ticket: schemas.Ticket):
        # TODO: add threads
        player = ticket["player_data"]
        team1, team2 = self.team_builder.assign_practice_team_pair(player)
        match = schemas.Match(
            ticket_id=ticket["id"],
            creation_time=datetime.now(),
            team1=team1,
            team2=team2,
        )
        return match

    def ranked_match(self, ticket: schemas.Ticket):
        player = ticket["player_data"]
        team1, team2 = self.team_builder.assign_practice_team_pair(player)
        match = schemas.Match(
            ticket_id=ticket["id"],
            creation_time=datetime.now(),
            team1=team1,
            team2=team2,
        )
        return match

    def assigned_match(self, ticket_steam: schemas.Ticket):
        # TODO: add threads
        match ticket_steam["mode"]:
            case GameMode.PRACTICE:
                return self.practice_match(ticket_steam)
            case GameMode.RANKED:
                return self.ranked_match(ticket_steam)

    # def match_function(self, profile_name, pool_tickets: List[Dict]) -> List[Dict]:
    #     matches = []
    #     pool_tickets.sort(key=self.skill)

    #     for i in range(0, len(pool_tickets) - self.players_per_game + 1):
    #         mt = pool_tickets[i : i + self.players_per_game]
    #         if self.skill(mt[-1]) - self.skill(mt[0]) < self.max_skill_difference:
    #             avg_skill = np.mean([self.skill(t) for t in mt])
    #             quality = -sum((self.skill(t) - avg_skill) ** 2 for t in mt)

    #             match_id = f"profile-{profile_name}-time-{time.strftime('%Y-%m-%dT%H:%M:%S')}-{len(matches)}"
    #             matches.append(
    #                 {
    #                     "id": match_id,
    #                     "match_profile": profile_name,
    #                     "match_function": "skillmatcher",
    #                     "tickets": mt,
    #                     "quality": quality,
    #                 }
    #             )

    #     return matches
