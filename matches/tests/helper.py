import random

from groups.services import CreateGroupService
from teams.services import CreateTeamService
from tournaments.models import Tournament

from ..models import Match
from ..services import MatchResultsService


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
        teams, tournament = CreateTeamService(teams_names).perform()
        CreateGroupService(teams, tournament).perform()
        tournament.phase = Tournament.FIRST_PHASE
        tournament.save()

    def generate_fake_result(self, phase, draw=True, partial=False):
        results = []
        matches = Match.objects.filter(phase=phase)
        for match in matches:
            single_match = {
                'id': match.id,
                'away_goals': random.randint(0, 10),
                'home_goals': random.randint(0, 10)
            }
            if single_match['away_goals'] == single_match['home_goals']:
                if not draw:
                    single_match['away_goals'] += 1
            results.append(single_match)
            if partial:
                results.pop()
        MatchResultsService(results).perform()

    def generate_first_phase_results(self, partial=False):
        self.generate_first_phase()
        self.generate_fake_result(Tournament.FIRST_PHASE, partial=partial)

    def generate_second_phase_results(self):
        self.generate_first_phase_results()
        self.generate_fake_result(Tournament.SECOND_PHASE, draw=False)

    def generate_semifinal_phase_results(self):
        self.generate_second_phase_results()
        self.generate_fake_result(Tournament.SEMI_FINAL, draw=False)

    def generate_final_phase_results(self):
        self.generate_semifinal_phase_results()
        self.generate_fake_result(Tournament.FINAL, draw=False)
