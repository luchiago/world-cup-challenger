from django.test import TestCase

from ..models import Tournament


class TournamentModelTestCase(TestCase):

    def setUp(self):
        self.tournament = Tournament()

    def test_model_can_create_tournament(self):
        old_count = Tournament.objects.count()
        self.tournament.save()
        new_count = Tournament.objects.count()
        created_tournament = Tournament.objects.last()

        self.assertNotEquals(old_count, new_count)
        self.assertFalse(created_tournament.finished)
        self.assertIsNone(created_tournament.phase)

    def test_model_can_change_tournament_phase(self):
        phase = Tournament.FIRST_PHASE
        self.tournament.phase = phase
        self.tournament.save()
        created_tournament = Tournament.objects.last()
        self.assertEquals(int(created_tournament.phase), phase)
