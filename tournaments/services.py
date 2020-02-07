from groups.models import Group
from groups.serializer import GroupSerializer
from teams.models import Team
from teams.serializer import TeamSerializer

from .models import Tournament


class TournamentService:
    def __init__(self, tournament):
        self.tournament = tournament

    def check_current_phase(self):
        if self.tournament.phase == Tournament.FIRST_PHASE:
            groups = Group.objects.filter(tournament__pk=self.tournament.pk)
            return GroupSerializer(groups, many=True)
        else:
            teams = Team.objects.filter(
                group__tournament__pk=self.tournament.pk)
            return TeamSerializer(teams, many=True)

    def perform(self):
        return self.check_current_phase()


class RankingService:
    def __init__(self, tournament):
        self.tournament = tournament

    def generate_ranking(self):
        if self.tournament.phase == Tournament.FIRST_PHASE:
            return self.generate_group_ranking()
        else:
            return self.generate_general_ranking()

    def create_serialized_teams(self, teams):
        serialized_teams = []
        for team in teams:
            team_data = {}
            team_data['id'] = team.id
            team_data['name'] = team.name
            team_data['position'] = team.position
            serialized_teams.append(team_data)
        return serialized_teams

    def generate_group_ranking(self):
        groups = Group.objects.filter(tournament__pk=self.tournament.pk)
        ranking = []
        for group in groups:
            serialized_group = {}
            serialized_group['id'] = group.id
            serialized_group['letter'] = group.letter
            serialized_group['teams'] = self.create_serialized_teams(
                group.teams.all().order_by('position'))
            ranking.append(serialized_group)
        return ranking

    def generate_general_ranking(self):
        teams = Team.objects.filter(
            group__tournament__pk=self.tournament.pk).order_by('position')
        return self.create_serialized_teams(teams)

    def perform(self):
        ranking = self.generate_ranking()
        return ranking
