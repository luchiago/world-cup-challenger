import random

from django.test import TestCase

from ..factories import TeamFactory
from ..models import Team


class TeamModelTestCase(TestCase):    

    def test_model_can_create_team(self):
        old_count = Team.objects.count()
        one_team = TeamFactory()
        one_team.save()
        new_count = Team.objects.count()
        created_team = Team.objects.last()

        self.assertNotEqual(old_count, new_count)
        self.assertEquals(one_team.name, created_team.name)
        self.assertEquals(one_team.points, created_team.points)
        self.assertEquals(one_team.goals, created_team.goals)
        self.assertEquals(one_team.position, created_team.position)

    def test_model_can_create_batch_of_teams(self):
        amount_of_teams = 5
        many_teams = TeamFactory.create_batch(amount_of_teams)
        for team in many_teams:
            team.save()
        new_count = Team.objects.count()

        self.assertEqual(amount_of_teams, new_count)

    def test_model_can_create_team_only_with_name(self):
        team_with_default = Team(name='Brazil')
        default_points = default_goals = 0
        default_position = 1
        team_with_default.save()
        created_team = Team.objects.last()

        self.assertEquals(team_with_default.name, created_team.name)
        self.assertEquals(team_with_default.points, default_points)
        self.assertEquals(team_with_default.goals, default_goals)
        self.assertEquals(team_with_default.position, default_position)
