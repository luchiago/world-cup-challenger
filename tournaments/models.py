from django.db import models


class Tournament(models.Model):
    phase = models.CharField(max_length=100, null=True)
    finished = models.BooleanField(null=False, default=False)
