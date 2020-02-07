# Generated by Django 3.0.2 on 2020-02-06 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='phase',
            field=models.CharField(choices=[(0, 'First Phase'), (1, 'Second Phase'), (2, 'Semifinals'), (3, 'Final')], default=None, max_length=25),
        ),
    ]