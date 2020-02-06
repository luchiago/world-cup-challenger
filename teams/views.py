from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.services import CreateGroupService
from tournaments.models import Tournament

from .services import CreateTeamService


class TeamList(APIView):
    def post(self, request, format=None):
        try:
            teams, tournament = CreateTeamService(request).perform()
            CreateGroupService(teams, tournament).perform()
            tournament.phase = Tournament.FIRST_PHASE
            tournament.save()
            data = {
                'message': 'Tournament created and ready for First Phase',
                'id': tournament.id,
                'phase': Tournament.PHASE_CHOICES[tournament.phase][1],
            }
            return Response(
                data=data,
                status=status.HTTP_201_CREATED)
        except Exception as e:
            data = {'message': str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
