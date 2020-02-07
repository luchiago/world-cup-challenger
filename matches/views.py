from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import MatchResultsService


class MatchResults(APIView):

    def patch(self, request, format=None):
        try:
            MatchResultsService(request).perform()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            data = {'message': str(e)}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
