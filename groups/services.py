from matches.services import CreateMatchService

from .models import Group


class CreateGroupService:
    def __init__(self, teams, tournament):
        self.teams = teams
        self.tournament = tournament

    def create_group_matches(self, group):
        CreateMatchService(self.tournament).perform(group)

    def associate_teams(self, group):
        teams = self.teams[:3]
        for team in teams:
            team.group_id = group.id
            team.save()
            self.teams.remove(self.teams[0])

    def create_groups(self):
        group_letters = ['A', 'B', 'C', 'D']
        allowed_amount_teams = 12
        if len(self.teams) == allowed_amount_teams:
            for name in group_letters:
                group = Group(letter=name, tournament=self.tournament)
                group.save()
                self.associate_teams(group)
                self.create_group_matches(group)
        else:
            raise Exception('Wrong number of Teams')

    def perform(self):
        self.tournament.save()
        return self.create_groups()
