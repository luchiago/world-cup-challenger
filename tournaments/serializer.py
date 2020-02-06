from rest_framework import serializers

from groups.serializer import GroupSerializer
from matches.serializer import MatchSerializer

from .models import Tournament


class TournamentSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    matches = MatchSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ['id', 'phase', 'finished', 'groups', 'matches']
