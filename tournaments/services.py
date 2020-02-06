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
