import json
import random

from django.test import TestCase
from rest_framework import status

from tournaments.models import Tournament

from ..models import Match
from .helper import MatchTestHelper


class MatchResultViewTest(TestCase):

    def setUp(self):
        MatchTestHelper().generate_first_phase()
        self.away_goals = random.randint(0, 10)
        self.home_goals = random.randint(0, 10)

    def test_can_change_result_of_one_match(self):
        match_pk = Match.objects.all().first().pk
        result = [
            {
                'id': match_pk,
                'away_goals': self.away_goals,
                'home_goals': self.home_goals
            }
        ]
        response = self.client.patch(
            '/matches/',
            data=json.dumps(result),
            content_type='application/json')
        match = Match.objects.get(pk=match_pk)
        self.assertEquals(match.away_team_goals, self.away_goals)
        self.assertEquals(match.home_team_goals, self.home_goals)
        self.assertEquals(match.phase, Tournament.FIRST_PHASE)
        self.assertTrue(match.played)
        self.assertIsNotNone(match.winner)
        self.assertEquals(match.tournament.phase, Tournament.FIRST_PHASE)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cannot_change_played_match(self):
        match_pk = 1
        error_message = 'Invalid Matches'
        result = [
            {
                'id': match_pk,
                'away_goals': self.away_goals,
                'home_goals': self.home_goals
            }
        ]
        response = self.client.patch(
            '/matches/',
            data=json.dumps(result),
            content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], error_message)

    def test_cannot_change_an_inexistent_match(self):
        error_message = 'Invalid Matches'
        result = [
            {
                'id': Match.objects.count() + 1,
                'away_goals': self.away_goals,
                'home_goals': self.home_goals
            }
        ]
        response = self.client.patch(
            '/matches/',
            data=json.dumps(result),
            content_type='application/json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEquals(response.data['message'], error_message)

    def test_can_change_a_batch_of_results(self):
        number_of_matches = 12
        current_tournament = Tournament.objects.last()
        current_phase = Tournament.FIRST_PHASE
        self.assertEquals(current_tournament.phase, current_phase)
        left_matches = list(Match.objects.filter(played=False))
        data = []
        match = {}
        for match in left_matches:
            match = {
                'id': match.pk,
                'away_goals': random.randint(0, 10),
                'home_goals': random.randint(0, 10)
            }
            data.append(match)
        response = self.client.patch(
            '/matches/',
            data=json.dumps(data),
            content_type='application/json')
        empty_list = 0
        not_played_matches = list(
            Match.objects.filter(
                phase=current_phase,
                played=False))
        played_matches = list(
            Match.objects.filter(
                phase=current_phase,
                played=True))
        current_tournament = Tournament.objects.last()
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(not_played_matches), empty_list)
        self.assertEquals(len(played_matches), number_of_matches)
        self.assertEquals(current_tournament.phase, current_phase + 1)
