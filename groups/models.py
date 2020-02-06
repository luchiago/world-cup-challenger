from django.db import models

from tournaments.models import Tournament


class Group(models.Model):
    letter = models.CharField(max_length=1, null=False)
    tournament = models.ForeignKey(
        Tournament,
        related_name='groups',
        on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        allowed_letters = ['A', 'B', 'C', 'D']
        if self.letter in allowed_letters:
            super(Group, self).save(*args, **kwargs)
        else:
            raise NameError
