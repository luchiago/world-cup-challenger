from django.db import models


class Tournament(models.Model):

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

    phase = models.IntegerField(choices=PHASE_CHOICES, default=None, null=True)
    finished = models.BooleanField(null=False, default=False)
