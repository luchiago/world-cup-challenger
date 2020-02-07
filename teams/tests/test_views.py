import json

from django.test import Client, TestCase
from rest_framework import status

from groups.models import Group
from matches.models import Match
from tournaments.models import Tournament

from ..models import Team


class TeamViewTest(TestCase):

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
        self.client = Client()
        self.response = self.client.post('/teams/',
                                         data=json.dumps(self.teams_names),
                                         content_type='application/json'
                                         )
        self.created_tournament = Tournament.objects.last()

    def test_can_create_tournament_with_team_names(self):
        sucess_message = "Tournament created and ready for First Phase"
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.data['message'], sucess_message)
        self.assertEqual(self.response.data['id'], self.created_tournament.id)
        self.assertEqual(self.response.data['phase'], Tournament.PHASE_CHOICES[
            self.created_tournament.phase][1])

    def test_can_create_tournament_with_correct_names(self):
        expected_amount_teams = 12
        created_teams = Team.objects.filter(
            group__tournament__pk=self.created_tournament.pk)
        request_names = [team['name'] for team in self.teams_names]
        for team in created_teams:
            self.assertIn(team.name, request_names)
        self.assertEqual(len(created_teams), expected_amount_teams)

    def test_can_create_tournament_with_groups(self):
        expected_amount_groups = 4
        expected_group_names = ['A', 'B', 'C', 'D']
        expected_amount_teams_per_group = 3
        created_groups = Group.objects.filter(
            tournament__pk=self.created_tournament.pk)
        for group in created_groups:
            self.assertIn(group.letter, expected_group_names)
            self.assertEquals(len(group.teams.all()),
                              expected_amount_teams_per_group)
        self.assertEquals(len(created_groups), expected_amount_groups)

    def test_can_create_tournament_with_matches(self):
        expected_amount_matches = 12
        expected_amount_goals = 0
        created_matches = Match.objects.filter(
            tournament__pk=self.created_tournament.pk)
        for match in created_matches:
            self.assertEquals(match.away_team_goals, expected_amount_goals)
            self.assertEquals(match.home_team_goals, expected_amount_goals)
        self.assertEquals(len(created_matches), expected_amount_matches)

    def test_cannot_create_another_tournament_without_finish_the_last(self):
        error_message = 'The last tournament did not finished'
        response = self.client.post('/teams/',
                                    data=json.dumps(self.teams_names),
                                    content_type='application/json'
                                    )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], error_message)

    def test_cannot_create_tournament_with_repeated_teams(self):
        repeated_teams_name = self.teams_names
        repeated_teams_name[1]['name'] = "USA"
        last_tournament = Tournament.objects.last()
        last_tournament.finished = True
        last_tournament.save()
        response = self.client.post('/teams/',
                                    data=json.dumps(repeated_teams_name),
                                    content_type='application/json'
                                    )
        expected_error_message = 'Invalid teams'
        self.assertEquals(response.data['message'], expected_error_message)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cannot_create_tournament_with_wrong_number_of_teams(self):
        less_teams_name = self.teams_names
        less_teams_name.pop()
        last_tournament = Tournament.objects.last()
        last_tournament.finished = True
        last_tournament.save()
        response = self.client.post('/teams/',
                                    data=json.dumps(self.teams_names),
                                    content_type='application/json'
                                    )
        expected_error_message = 'Invalid teams'
        self.assertEquals(response.data['message'], expected_error_message)
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_create_another_tournament_when_last_finish(self):
        old_count = Tournament.objects.count()
        last_tournament = Tournament.objects.last()
        last_tournament.finished = True
        last_tournament.save()
        response = self.client.post('/teams/',
                                         data=json.dumps(self.teams_names),
                                         content_type='application/json'
                                        )
        new_count = Tournament.objects.count()
        new_tournament = Tournament.objects.last()
        self.assertNotEquals(old_count, new_count)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(new_tournament.phase, Tournament.FIRST_PHASE)
