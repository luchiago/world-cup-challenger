from rest_framework import serializers

from .models import Match


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = [
            'id',
            'away_team',
            'home_team',
            'away_team_goals',
            'home_team_goals']
