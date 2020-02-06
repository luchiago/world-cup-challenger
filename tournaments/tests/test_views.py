import json

from django.test import Client, TestCase
from rest_framework import status

from ..models import Tournament


class TournamentViewTest(TestCase):

    def setUp(self):
        self.teams_names = [
            {"name": "Austrália"},
            {"name": "Saudi Arabia"},
            {"name": "Mexico"},
            {"name": "Brazil"},
            {"name": "Argentina"},
            {"name": "USA"},
            {"name": "Portugal"},
            {"name": "Russia"},
            {"name": "France"},
            {"name": "England"},
            {"name": "Colombia"},
            {"name": "Germany"}
        ]
        self.list_of_teams = [team['name'] for team in self.teams_names]
        self.client = Client()
        self.client.post('/teams/', data=json.dumps(self.teams_names),
                         content_type='application/json'
                         )
        self.created_tournament = Tournament.objects.last()
        self.response = self.client.get('/tournaments/')

    def test_can_read_the_current_phase(self):
        self.assertEquals(self.response.data['id'], self.created_tournament.id)
        current_phase = self.created_tournament.phase
        self.assertEquals(
            self.response.data['phase'],
            Tournament.PHASE_CHOICES[current_phase][1])
        self.assertFalse(self.response.data['finished'])
        self.assertEquals(self.response.status_code, status.HTTP_200_OK)

    def test_can_read_list_of_teams_of_first_phase(self):
        self.response = self.client.get('/tournaments/teams/')
        allowed_amout_groups = 4
        allowed_amout_teams = 3
        allowed_groups_names = ['A', 'B', 'C', 'D']
        allowed_groups_names.reverse()
        self.assertEquals(len(self.response.data), allowed_amout_groups)
        for group in self.response.data:
            self.assertEquals(group['letter'], allowed_groups_names.pop())
            self.assertEquals(len(group['teams']), allowed_amout_teams)
            for team in group['teams']:
                self.assertIn(team['name'], self.list_of_teams)

    def test_can_read_list_of_matches_of_first_phase(self):
        self.response = self.client.get('/tournaments/matches/')
        expected_amount_next_matches = 12
        expected_amount_played_matches = 0
        self.assertEquals(
            len(self.response.data['next_matches']), expected_amount_next_matches)
        self.assertEquals(
            len(self.response.data['played_matches']), expected_amount_played_matches)

    def test_can_read_list_of_teams_of_other_phase(self):
        self.created_tournament.phase = Tournament.SECOND_PHASE
        self.created_tournament.save()
        self.response = self.client.get('/tournaments/teams/')
        for team in self.response.data:
            self.assertIn(team['name'], self.list_of_teams)

    def test_cannot_read_data_without_tournament(self):
        self.created_tournament.delete()
        tournament_controller_response = self.client.get('/tournaments/')
        tournament_teams_controller_response = self.client.get(
            '/tournaments/teams/')
        tournament_matches_controller_response = self.client.get(
            '/tournaments/matches/')
        self.assertEquals(
            tournament_controller_response.status_code,
            status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            tournament_teams_controller_response.status_code,
            status.HTTP_404_NOT_FOUND)
        self.assertEquals(
            tournament_matches_controller_response.status_code,
            status.HTTP_404_NOT_FOUND)
