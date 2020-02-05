# Generated by Django 3.0.2 on 2020-02-05 02:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tournaments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letter', models.CharField(max_length=1)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='tournaments.Tournament')),
            ],
        ),
    ]
