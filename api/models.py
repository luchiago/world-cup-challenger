from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    points = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    position = models.IntegerField(default=1)
    