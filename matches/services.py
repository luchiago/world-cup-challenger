from itertools import combinations

from groups.models import Group

from .models import Match


class CreateMatchService:
    def __init__(self, tournament):
        self.tournament = tournament

    def create_match(self, list_of_teams):
        allowed_amount_teams = 2
        if len(list_of_teams) == allowed_amount_teams:
            away_team = list_of_teams.pop()
            home_team = list_of_teams.pop()
            created_match = Match(
                away_team=away_team,
                home_team=home_team,
                tournament=self.tournament)
            created_match.save()
            return created_match
        else:
            raise Exception('Wrong number of Teams')

    def create_group_matches(self, list_of_teams):
        allowed_amount_teams = 3
        group_teams = list_of_teams.teams.all()
        if len(group_teams) == allowed_amount_teams:
            teams_combinations = list(combinations(group_teams, 2))
            for pair in teams_combinations:
                self.create_match(list(pair))
        else:
            raise Exception('Wrong number of Teams')

    def perform(self, list_of_teams):
        if isinstance(list_of_teams, Group):
            self.create_group_matches(list_of_teams)
        else:
            self.create_match(list_of_teams)
