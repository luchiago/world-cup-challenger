from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.services import CreateGroupService
from tournaments.models import Tournament
from tournaments.serializer import TournamentSerializer

from .services import CreateTeamService


class TeamList(APIView):
    def post(self, request, format=None):
        try:
            tournament = Tournament()
            teams = CreateTeamService(request).perform()
            CreateGroupService(teams, tournament).perform()
            tournament.phase = 'First Phase'
            tournament.save()
            serialized = TournamentSerializer(tournament)
            return Response(
                data=serialized.data,
                status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {'message': str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
