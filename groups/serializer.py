from rest_framework import serializers

from teams.serializer import TeamSerializer

from .models import Group


class GroupSerializer(serializers.ModelSerializer):

    teams = TeamSerializer(many=True)

    class Meta:
        model = Group
        fields = ['id', 'letter', 'teams']
