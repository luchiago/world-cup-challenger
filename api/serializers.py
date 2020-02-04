from rest_framework import serializers

from .models import Team


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ['id', 'name', 'points', 'goals', 'position']

    def validate(self, data):
        if not data['name'] or data['name'] == '':
            raise serializers.ValidationError('Name must not be empty')
        
        return data

