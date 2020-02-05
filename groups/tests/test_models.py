from django.test import TestCase
from django.db.utils import IntegrityError

from ..models import Group
from tournaments.models import Tournament


class GroupModelTestCase(TestCase):

    def setUp(self):
        self.letter = 'A'
        self.tournament = Tournament()
        self.tournament.save()
        self.group = Group(letter=self.letter)
        self.group.tournament_id = self.tournament.id

    def test_model_can_create_group(self):
        old_count = Group.objects.count()
        self.group.save()
        new_count = Group.objects.count()
        created_group = Group.objects.last()

        self.assertNotEquals(old_count, new_count)
        self.assertEquals(created_group.letter, self.letter)

    def test_model_cannot_create_group_without_letter(self):
        group_without_letter = Group()
        with self.assertRaises(IntegrityError):
            group_without_letter.save()

    def test_model_cannot_create_group_without_tournament(self):
        self.group.tournament_id = None
        with self.assertRaises(IntegrityError):
            self.group.save()
