from rest_framework import serializers
from .models import Race, RaceCategory, RaceTiming, Participant


class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'


class RaceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceCategory
        exclude = ('last_modified', 'race')


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        exclude = ('id', 'date_registered', 'last_modified',)
        read_only_fields = ('race', 'age', 'user', 'place')


class RaceTimingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceTiming
        fields = '__all__'
        read_only_fields = ('race',)
