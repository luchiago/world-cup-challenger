from groups.services import CreateGroupService
from teams.services import CreateTeamService
from tournaments.models import Tournament


class Request:
    def __init__(self, teams_names):
        self.data = teams_names


class MatchTestHelper:

    def generate_first_phase(self):
        teams_names = [
            {"name": "Austrália"},
            {"name": "Saudi Arabia"},
            {"name": "Mexico"},
            {"name": "Brazil"},
            {"name": "Argentina"},
            {"name": "USA"},
            {"name": "Portugal"},
            {"name": "Russia"},
            {"name": "France"},
            {"name": "England"},
            {"name": "Colombia"},
            {"name": "Germany"}
        ]
        request = Request(teams_names)
        teams, tournament = CreateTeamService(request).perform()
        CreateGroupService(teams, tournament).perform()
        tournament.phase = Tournament.FIRST_PHASE
        tournament.save()
