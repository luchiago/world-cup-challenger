# Generated by Django 3.0.2 on 2020-02-06 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='played',
            field=models.BooleanField(default=False),
        ),
    ]
