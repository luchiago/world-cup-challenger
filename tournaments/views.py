from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from matches.services import MatchService

from .models import Tournament
from .serializer import TournamentSerializer
from .services import RankingService, TournamentService


@api_view(['GET'])
def tournament_list(request):
    current_tournament = Tournament.objects.last()
    if not current_tournament:
        data = {'phase': current_tournament}
        return Response(data=data, status=status.HTTP_404_NOT_FOUND)
    serialized = TournamentSerializer(current_tournament)
    return Response(data=serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tournament_teams_list(request):
    current_tournament = Tournament.objects.last()
    if not current_tournament:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized = TournamentService(current_tournament).perform()
    return Response(data=serialized.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def tournament_matches_list(request):
    current_tournament = Tournament.objects.last()
    if not current_tournament:
        return Response(status=status.HTTP_404_NOT_FOUND)
    matches = MatchService(current_tournament).perform()
    return Response(data=matches, status=status.HTTP_200_OK)


@api_view(['GET'])
def tournament_ranking(request):
    current_tournament = Tournament.objects.last()
    if not current_tournament:
        return Response(status=status.HTTP_404_NOT_FOUND)
    ranking = RankingService(current_tournament).perform()
    return Response(data=ranking, status=status.HTTP_200_OK)
