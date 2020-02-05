from django.db import models

from teams.models import Team


class Tournament(models.Model):
    phase = models.CharField(max_length=100, null=True)
    finished = models.BooleanField(null=False, default=False)
    winner = models.OneToOneField(
        Team,
        on_delete=models.CASCADE,
        related_name='winner')
