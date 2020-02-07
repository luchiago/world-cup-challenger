import json

from django.test import Client, TestCase
from rest_framework import status

from groups.models import Group
from matches.tests.helper import MatchTestHelper
from teams.models import Team

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

    def test_can_read_list_of_matches(self):
        self.response = self.client.get('/tournaments/matches/')
        expected_amount = 12
        expected_empty = 0
        first_phase = 'First Phase'
        second_phase = 'Second Phase'
        self.assertEquals(
            len(self.response.data[0]['next_matches']), expected_amount)
        self.assertEquals(
            len(self.response.data[0]['played_matches']), expected_empty)
        self.assertEquals(
            len(self.response.data[1]['next_matches']), expected_empty)
        self.assertEquals(
            len(self.response.data[1]['played_matches']), expected_empty)

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


class RankingViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.results_helper = MatchTestHelper()

    def test_first_ranking_all_teams_in_first_position(self):
        self.results_helper.generate_first_phase()
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_of_groups = response.data
        for group in list_of_groups:
            group_from_db = Group.objects.get(pk=group['id'])
            self.assertEquals(group_from_db.letter, group['letter'])
            for team in group['teams']:
                team_from_db = group_from_db.teams.get(pk=team['id'])
                self.assertEquals(team_from_db.name, team['name'])
                self.assertEquals(team_from_db.position, team['position'])

    def test_ranking_first_phase(self):
        self.results_helper.generate_first_phase_results(partial=True)
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_of_groups = response.data
        for group in list_of_groups:
            group_from_db = Group.objects.get(pk=group['id'])
            self.assertEquals(group_from_db.letter, group['letter'])
            for team in group['teams']:
                team_from_db = group_from_db.teams.get(pk=team['id'])
                self.assertEquals(team_from_db.name, team['name'])
                self.assertEquals(team_from_db.position, team['position'])

    def test_ranking_second_phase(self):
        self.results_helper.generate_second_phase_results()
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_of_teams = response.data
        for team in list_of_teams:
            team_from_db = Team.objects.get(pk=team['id'])
            self.assertEquals(team_from_db.name, team['name'])
            self.assertEquals(team_from_db.position, team['position'])

    def test_ranking_semi_final_phase(self):
        self.results_helper.generate_semifinal_phase_results()
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_of_teams = response.data
        for team in list_of_teams:
            team_from_db = Team.objects.get(pk=team['id'])
            self.assertEquals(team_from_db.name, team['name'])
            self.assertEquals(team_from_db.position, team['position'])

    def test_ranking_final_phase(self):
        self.results_helper.generate_final_phase_results()
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        list_of_teams = response.data
        for team in list_of_teams:
            team_from_db = Team.objects.get(pk=team['id'])
            self.assertEquals(team_from_db.name, team['name'])
            self.assertEquals(team_from_db.position, team['position'])

    def test_ranking_without_tournament(self):
        response = self.client.get('/tournaments/rankings/')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
