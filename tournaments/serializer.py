from rest_framework import serializers

from groups.serializer import GroupSerializer
from matches.serializer import MatchSerializer

from .models import Tournament


class TournamentCompleteSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    matches = MatchSerializer(many=True)

    class Meta:
        model = Tournament
        fields = ['id', 'phase', 'finished', 'groups', 'matches']


class TournamentSerializer(serializers.ModelSerializer):

    phase = serializers.CharField(source='get_phase_display')

    class Meta:
        model = Tournament
        fields = ['id', 'phase', 'finished']

