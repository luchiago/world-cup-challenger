from django.db import models

from teams.models import Team
from tournaments.models import Tournament


class Match(models.Model):

    FIRST_PHASE = 0
    SECOND_PHASE = 1
    SEMI_FINAL = 2
    FINAL = 3

    PHASE_CHOICES = [
        (FIRST_PHASE, 'First Phase'),
        (SECOND_PHASE, 'Second Phase'),
        (SEMI_FINAL, 'Semifinals'),
        (FINAL, 'Final')
    ]

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
    winner = models.ForeignKey(
        Team,
        related_name='winner',
        on_delete=models.CASCADE,
        default=None,
        null=True
    )
    played = models.BooleanField(default=False)
    phase = models.IntegerField(choices=PHASE_CHOICES, default=None, null=True)
    tournament = models.ForeignKey(
        Tournament,
        related_name='matches',
        on_delete=models.CASCADE)
