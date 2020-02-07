from tournaments.models import Tournament

from .models import Team


class VerifyTeamService:
    def __init__(self, teams):
        self.teams = teams

    def check_number_of_teams(self):
        allowed_amount = 12
        if len(self.teams) == allowed_amount:
            return True
        return False

    def check_repeated_teams(self):
        list_of_teams = [team['name'] for team in self.teams]
        if len(self.teams) == len(set(list_of_teams)):
            return True
        return False

    def is_valid(self):
        return self.check_number_of_teams() and self.check_repeated_teams()


class CreateTeamService:
    def __init__(self, teams):
        self.data = teams

    def create_teams(self):
        if VerifyTeamService(self.data).is_valid():
            list_of_teams_objects = []
            for data in self.data:
                team = Team(name=data['name'])
                list_of_teams_objects.append(team)
            return list_of_teams_objects
        else:
            raise Exception('Invalid teams')

    def perform(self):
        last_tournament = Tournament.objects.last()
        if last_tournament and not last_tournament.finished:
            raise Exception('The last tournament did not finished')
        else:
            tournament = Tournament()
            return self.create_teams(), tournament
