from django.db.utils import IntegrityError
from django.test import TestCase

from groups.models import Group
from tournaments.models import Tournament

from ..models import Team


class TeamModelTestCase(TestCase):

    def setUp(self):
        self.tournament = Tournament()
        self.tournament.save()
        self.group = Group(letter='A')
        self.group.tournament_id = self.tournament.id
        self.group.save()
        self.team = Team(name='Brazil')
        self.team.group_id = self.group.id

    def test_model_can_create_team(self):
        old_count = Team.objects.count()
        self.team.save()
        new_count = Team.objects.count()
        created_team = Team.objects.last()

        self.assertNotEqual(old_count, new_count)
        self.assertEquals(self.team.name, created_team.name)
        self.assertEquals(self.team.points, created_team.points)
        self.assertEquals(self.team.goals, created_team.goals)
        self.assertEquals(self.team.position, created_team.position)
        self.assertEquals(self.team.group.letter, self.group.letter)
        self.assertEquals(self.team, self.group.teams.get())

    def test_model_cannot_create_team_without_name(self):
        team_without_name = Team()
        with self.assertRaises(IntegrityError):
            team_without_name.save()

    def test_model_cannot_create_team_without_group(self):
        team_without_group = Team()
        with self.assertRaises(IntegrityError):
            team_without_group.save()
