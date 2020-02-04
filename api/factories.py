import random

import factory

from .models import Team

WORLDWIDE_TEAMS = [
        'Austrália',
        'Iran',
        'Japan',
        'Saudi Arabia',
        'South Korea',
        'Egypt',
        'Morocco',
        'Nigeria',
        'Senegal',
        'Tunisia',
        'Costa Rica',
        'Mexico',
        'Panama',
        'Argentina',
        'Brazil',
        'Colombia',
        'Peru',
        'Uruguay',
        'Belgium',
        'Croatia',
        'Denmark',
        'England',
        'France',
        'Germany',
        'Iceland',
        'Poland',
        'Portugal',
        'Russia',
        'Serbia',
        'Spain',
        'Sweden',
        'Switzerland']

class TeamFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = Team

    name = random.choice(WORLDWIDE_TEAMS)
    points = random.randint(0, 10)
    goals = random.randint(0, 10)
    position = random.randint(0, 10)
    