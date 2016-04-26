from .models import Participant
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError


def has_participant_finished(function):
    def wrap(self, *args, **kwargs):
        queryset = Participant.objects.filter(race=kwargs.get('race_pk'))
        participant = get_object_or_404(queryset, user=kwargs.get('pk'))
        if participant.finish_time:
            raise ValidationError("This participant has already finished")
        return function(self, participant, queryset, *args, **kwargs)
    return wrap

