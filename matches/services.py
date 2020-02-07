from itertools import combinations

from groups.models import Group
from teams.models import Team
from tournaments.models import Tournament

from .models import Match
from .serializer import MatchSerializer


class MatchService:
    def __init__(self, tournament):
        self.tournament = tournament

    def list_played_matches(self):
        played_matches = Match.objects.filter(
            tournament__pk=self.tournament.id,
            played=True,
            phase=self.tournament.phase)
        serialized = MatchSerializer(played_matches, many=True)
        return serialized.data

    def list_not_played_matches(self):
        not_played_matches = Match.objects.filter(
            tournament__pk=self.tournament.id,
            played=False,
            phase=self.tournament.phase)
        serialized = MatchSerializer(not_played_matches, many=True)
        return serialized.data

    def list_phase_matches(self):
        matches = {}
        matches['next_matches'] = self.list_not_played_matches()
        matches['played_matches'] = self.list_played_matches()
        return matches

    def perform(self):
        return self.list_phase_matches()


class CreateMatchService:
    def __init__(self, tournament):
        self.tournament = tournament

    def create_match(self, list_of_teams):
        allowed_amount_teams = 2
        if len(list_of_teams) == allowed_amount_teams:
            away_team = list_of_teams.pop()
            home_team = list_of_teams.pop()
            phase = self.tournament.phase
            if not phase:
                phase = Tournament.FIRST_PHASE
            created_match = Match(
                away_team=away_team,
                home_team=home_team,
                tournament=self.tournament,
                phase=phase)
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


class MatchResultsService:

    def __init__(self, request):
        self.results = request.data
        self.tournament = Tournament.objects.last()

    def verify_matches(self):
        for received_match in self.results:
            match = Match.objects.filter(
                pk=received_match['id'],
                tournament__phase=self.tournament.phase,
                played=False)
            if not match:
                raise Exception('Invalid Matches')

    def can_advance_next_phase(self):
        has_not_played_matches = Match.objects.filter(
            tournament__phase=self.tournament.phase,
            played=False)
        if not has_not_played_matches:
            if self.tournament.phase != Tournament.FINAL:
                self.tournament.phase += 1
                self.tournament.save()
            else:
                raise Exception('The tournament has finished')

    def check_match_winner(self, away_team, home_team, result):
        if result['away_goals'] > result['home_goals']:
            away_team.points += 3
        if result['away_goals'] < result['home_goals']:
            home_team.points += 3
        if result['away_goals'] == result['home_goals']:
            if self.tournament.phase != Tournament.FIRST_PHASE:
                raise Exception('Draw is not allowed')
            away_team.points += 1
            home_team.points += 1
        home_team.save()
        away_team.save()

    def update_team_position_in_group(self, team):
        group = Group.objects.get(pk=team.group.id)
        list_group_teams = list(
            group.teams.all().order_by(
                '-points', '-goals'))
        for team in list_group_teams:
            new_position = list_group_teams.index(team) + 1
            team.position = new_position
            team.save()

    def update_team_position_in_tournament(self, team):
        list_tournament_teams = list(
            Team.objects.filter(
                group__tournament__pk=self.tournament.pk).order_by(
                '-points', '-goals'))
        for team in list_tournament_teams:
            new_position = list_tournament_teams.index(team) + 1
            team.position = new_position
            team.save()

    def put_match_results(self):
        for received_match in self.results:
            match = Match.objects.get(pk=received_match['id'])
            match.away_team_goals = received_match['away_goals']
            match.home_team_goals = received_match['home_goals']
            match.away_team.goals += received_match['away_goals']
            match.home_team.goals += received_match['home_goals']
            match.played = True
            match.save()
            self.check_match_winner(
                match.away_team,
                match.home_team,
                received_match)
            if self.tournament.phase == Tournament.FIRST_PHASE:
                self.update_team_position_in_group(match.away_team)
                self.update_team_position_in_group(match.home_team)
            else:
                self.update_team_position_in_tournament(match.away_team)
                self.update_team_position_in_tournament(match.home_team)

        self.can_advance_next_phase()

    def perform(self):
        self.verify_matches()
        return self.put_match_results()
