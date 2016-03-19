from rest_framework import serializers
from .models import Race, RaceCategory, Participant


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ('id', 'name', 'date', 'distance')


class RaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceCategory
        fields = ('min_age', 'max_age')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        exclude = ('user', 'race', 'date_registered', 'last_modified')
