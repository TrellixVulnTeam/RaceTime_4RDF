from .models import Race, RaceCategory, Participant
from .serializers import RaceSerializer, RaceCategorySerializer, ParticipantSerializer
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import APIException

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
        if not self.queryset.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        return super(ParticipantViewSet, self).list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        participant = self.queryset.filter(user=kwargs['pk'], race=kwargs['race_pk'])
        if not participant.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(participant)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_race(self, race_pk):
        try:
            return Race.objects.get(id=race_pk)
        except ObjectDoesNotExist:
            raise APIException('This race does not exist')

    def set_participant_category(self, age):
        race_categories = RaceCategory.objects.filter(race=self.kwargs['race_pk'])
        for category in race_categories:
            if category.min_age < age <= category.max_age:
                return category
        return None

    def calculate_age(self, date_of_birth):
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def create_participant(self, serializer,  participants_ids):
        if self.request.user.id in participants_ids:
            raise APIException('You are already registered for this race')
        else:
            race = self.get_race(self.kwargs['race_pk'])
            age = self.calculate_age(self.request.user.date_of_birth)
            participant_category = self.set_participant_category(age)
            serializer.save(user=self.request.user, race=race, age=age, category=participant_category)

    def perform_create(self, serializer):
        race_pk = self.kwargs['race_pk']
        participants = Participant.objects.filter(race=race_pk)
        participants_ids = [participant.user.id for participant in participants]
        self.create_participant(serializer, participants_ids)







