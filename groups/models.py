from django.db import models

from tournaments.models import Tournament


class Group(models.Model):
    letter = models.CharField(max_length=1)
    tournament = models.ForeignKey(
        Tournament,
        related_name='groups',
        on_delete=models.CASCADE)
