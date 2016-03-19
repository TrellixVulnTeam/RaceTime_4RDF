from .models import Race, RaceCategory, Participant
from .serializers import RaceSerializer, RaceCategorySerializer, ParticipantSerializer
from django.core import serializers
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import detail_route
from rest_framework.exceptions import APIException
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

    def get_permissions(self):
        if not self.request.method == 'GET':
            self.permission_classes = [permissions.IsAdminUser]
        return super(RaceViewSet, self).get_permissions()


class RaceCategoryViewSet(viewsets.ModelViewSet):
    queryset = RaceCategory.objects.all()
    serializer_class = RaceCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def get_race(self, race_pk):
        try:
            return Race.objects.get(id=race_pk)
        except ObjectDoesNotExist:
            raise APIException('This race does not exist')

    def perform_create(self, serializer):
        race = self.get_race(self.kwargs['race_pk'])
        serializer.save(race=race)


class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(race=kwargs['race_pk'])
        return super(ParticipantViewSet, self).list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=kwargs['pk'], race=kwargs['race_pk'])
        return super(ParticipantViewSet, self).list(request, *args, **kwargs)

    def get_race(self, race_pk):
        try:
            return Race.objects.get(id=race_pk)
        except ObjectDoesNotExist:
            raise APIException('This race does not exist')

    def set_participant_category(self):
        race_categories = RaceCategory.objects.filter(race=self.kwargs['race_pk'])
        for category in race_categories:
            if category.min_age < self.request.user.age <= category.max_age:
                return category
        return None

    def create_participant(self, serializer,  participants_ids):
        if self.request.user.id in participants_ids:
            raise APIException('You are already registered for this race')
        else:
            race = self.get_race(self.kwargs['race_pk'])
            participant_category = self.set_participant_category()
            serializer.save(user=self.request.user, race=race, category=participant_category)

    def perform_create(self, serializer):
        race_pk = self.kwargs['race_pk']
        participants = Participant.objects.filter(race=race_pk)
        participants_ids = [participant.user.id for participant in participants]
        self.create_participant(serializer, participants_ids)







