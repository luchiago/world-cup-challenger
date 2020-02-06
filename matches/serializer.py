from rest_framework import serializers

from teams.serializer import TeamSerializer

from .models import Match


class MatchSerializer(serializers.ModelSerializer):

    away_team = TeamSerializer(many=False)
    home_team = TeamSerializer(many=False)
    phase = serializers.CharField(source='get_phase_display')

    class Meta:
        model = Match
        fields = [
            'id',
            'away_team',
            'home_team',
            'away_team_goals',
            'home_team_goals',
            'played',
            'phase'
        ]
