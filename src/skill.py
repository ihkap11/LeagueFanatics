import numpy as np
from scipy.stats import norm


class TrueSkill:
    """
    Class to score player's true skill.
    """

    def __init__(self, skill_range=[0.0, 50.0]):
        self.skill_range = skill_range
        self.beta = self.skill_range[1] / 3  # game's inherent variability
        self.tau = (
            self.beta / 10
        )  # τ is added to the uncertainty (σ) to prevent it from becoming too small

    def new_player_skill(self):
        skill = (self.skill_range[0] + self.skill_range[1]) / 2
        uncertainty = skill / 3
        level = 0
        return skill, uncertainty, level

    # def avg_team_stats(self, players: List[Player]):
    #     skill_sum = 0
    #     uncertainty_sum = 0
    #     for player in players:
    #         skill_sum += player.skill
    #         uncertainty_sum += player.uncertainty
    #     return skill_sum / len(players), uncertainty_sum / len(players)

    def v(self, x, epsilon=0):
        pdf = norm.pdf(x)
        cdf = norm.cdf(
            x * epsilon
        )  # epsilon modifies the direction based on win or loss
        return pdf / cdf

    def w(self, x, epsilon):
        pdf = norm.pdf(x)
        cdf = norm.cdf(x * epsilon)
        v_value = self.v(x, epsilon)
        return (pdf**2) / cdf + x * v_value

    def update_stats(self, skill1, skill2, uncertainty1, uncertainty2, win1):
        c = np.sqrt(2 * self.beta**2 + uncertainty1**2 + uncertainty2**2)
        x = (skill1 - skill2) / c

        if win1:
            cfd1 = self.v(x, epsilon=1)
            cdf2 = self.v(x, epsilon=-1)
            skill1_adjusted = skill1 + cfd1
            skill2_adjusted = skill2 - cdf2

            sigma1_prime = np.sqrt(
                uncertainty1**2 - (uncertainty2**4 / c**2) * self.w(x, epsilon=1)
            )
            sigma2_prime = np.sqrt(
                uncertainty1**2 - (uncertainty2**4 / c**2) * self.w(x, epsilon=-1)
            )
            sigma1_adjusted = np.sqrt(sigma1_prime**2 + self.tau**2)
            sigma2_adjusted = np.sqrt(sigma2_prime**2 + self.tau**2)

        else:
            cfd1 = self.v(x, epsilon=-1)
            cdf2 = self.v(x, epsilon=1)
            skill1_adjusted = skill1 + cfd1
            skill2_adjusted = skill2 - cdf2

            sigma1_prime = np.sqrt(
                uncertainty1**2 - (uncertainty2**4 / c**2) * self.w(x, epsilon=-1)
            )
            sigma2_prime = np.sqrt(
                uncertainty1**2 - (uncertainty2**4 / c**2) * self.w(x, epsilon=1)
            )
            sigma1_adjusted = np.sqrt(sigma1_prime**2 + self.tau**2)
            sigma2_adjusted = np.sqrt(sigma2_prime**2 + self.tau**2)

        return skill1_adjusted, skill2_adjusted, sigma1_adjusted, sigma2_adjusted

    # def update_uncertainty(self, skill1, skill2, uncertainty1, uncertainty2):
    #     c = np.sqrt(2 * self.beta**2 + uncertainty1**2 + uncertainty2**2)
    #     x = (skill1 - skill2) / c
    #     sigma_prime = np.sqrt(
    #         uncertainty1**2 - (uncertainty2**4 / c**2) * self.w(x, epsilon)
    #     )
    #     sigma_adjusted = np.sqrt(sigma_prime**2 + self.tau**2)
    #     return sigma_adjusted

    # # def update_team_skill(self, team1: Team, team2: Team):
    # #     c = math.sqrt(
    # #         2 * self.beta**2 + team1.uncertainty**2 + team2.uncertainty**2
    # #     )
    # #     x = (team1.skill - team2.skill) / c

    # #     if team1.wins:
    # #         team1_cdf = self.v(x, epsilon=1)
    # #         team2_cdf = self.v(x, epsilon=-1)
    # #         team1.skill = team1.skill + team1_cdf
    # #         team2.skill = team2.skill - team2_cdf
    # #     else:
    # #         team1_cdf = self.v(x, epsilon=-1)
    # #         team2_cdf = self.v(x, epsilon=1)
    # #         team1.skill = team1.skill - team1_cdf
    # #         team2.skill = team2.skill + team2_cdf
    # #     return team1, team2

    # # def update_team_player_skills(self, team1: Team, team2: Team):
    # #     updated_team1, updated_team2 = self.update_team_skill(team1, team2)

    # #     for player in updated_team1.players:
    # #         player.skill = updated_team1.skill
    # #         player.uncertainty = np.sqrt(updated_team1.skill**2 + self.tau**2)

    # #     for player in updated_team2.players:
    # #         player.skill = updated_team2
    # #         player.uncertainty = np.sqrt(updated_team2.skill**2 + self.tau**2)

    # #     return updated_team1, updated_team2


StatsCalculator = TrueSkill()
