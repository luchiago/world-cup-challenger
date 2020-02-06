from django.db import models

from teams.models import Team
from tournaments.models import Tournament


class Match(models.Model):
    away_team = models.ForeignKey(
        Team,
        related_name='away_team',
        on_delete=models.CASCADE)
    home_team = models.ForeignKey(
        Team,
        related_name='home_team',
        on_delete=models.CASCADE)
    away_team_goals = models.IntegerField(default=0)
    home_team_goals = models.IntegerField(default=0)
    played = models.BooleanField(default=False)
    tournament = models.ForeignKey(
        Tournament,
        related_name='matches',
        on_delete=models.CASCADE)
