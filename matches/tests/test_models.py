import random

from django.db.utils import IntegrityError
from django.test import TestCase

from groups.models import Group
from teams.models import Team
from tournaments.models import Tournament

from ..models import Match


class MatchModelTestCase(TestCase):

    def setUp(self):
        self.phase = Tournament.FIRST_PHASE
        self.group_letter = 'A'
        self.team_a_name = 'Brazil'
        self.team_b_name = 'Germany'
        self.tournament = Tournament(phase=self.phase)
        self.tournament.save()
        self.group = Group(letter=self.group_letter)
        self.group.tournament_id = self.tournament.id
        self.group.save()
        self.team_a_goals = random.randint(0, 10)
        self.team_b_goals = random.randint(0, 10)
        self.team_a = Team(name=self.team_a_name)
        self.team_b = Team(name=self.team_b_name)
        self.team_a.group_id = self.group.id
        self.team_b.group_id = self.group.id
        self.team_a.save()
        self.team_b.save()

    def test_model_can_create_match(self):
        old_count = Match.objects.count()
        match = Match(
            away_team=self.team_a,
            home_team=self.team_b,
            away_team_goals=self.team_a_goals,
            home_team_goals=self.team_b_goals,
            tournament=self.tournament,
            phase=self.tournament.phase
        )
        match.save()
        new_count = Match.objects.count()
        created_match = Match.objects.last()

        self.assertNotEquals(old_count, new_count)
        self.assertEquals(
            created_match.phase,
            self.tournament.phase)
        self.assertEquals(created_match.away_team.id, self.team_a.id)
        self.assertEquals(created_match.away_team_goals, self.team_a_goals)
        self.assertEquals(created_match.home_team.id, self.team_b.id)
        self.assertEquals(created_match.home_team_goals, self.team_b_goals)
        self.assertFalse(created_match.played)

    def test_model_cannot_create_match_without_teams(self):
        match_without_teams = Match()
        with self.assertRaises(IntegrityError):
            match_without_teams.save()

    def test_model_can_create_match_without_input_goals(self):
        expected_amount_goals = 0
        match_without_goals = Match(
            away_team=self.team_a,
            home_team=self.team_b,
            tournament=self.tournament,
            phase=self.tournament.phase
        )
        match_without_goals.save()
        created_match = Match.objects.last()
        self.assertEquals(created_match.away_team_goals, expected_amount_goals)
        self.assertEquals(created_match.away_team_goals, expected_amount_goals)
        self.assertEquals(created_match.phase, self.phase)
