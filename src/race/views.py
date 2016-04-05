from .mixins import CheckRaceExistenceMixin
from .models import Race, RaceCategory, Participant, RaceTiming
from .serializers import RaceSerializer, RaceCategorySerializer, ParticipantSerializer, RaceTimingSerializer
from datetime import date
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils import timezone
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from authentication.permissions import IsAdminOrReadOnly


class RaceViewSet(viewsets.ModelViewSet):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer
    permission_classes = [IsAdminOrReadOnly]

    @detail_route(methods=['get'])
    def results(self, *args, **kwargs):
        queryset = Participant.objects.order_by('finish_time')
        results = get_list_or_404(queryset, race=kwargs['pk'])
        serializer = ParticipantSerializer(results, many=True)
        return Response(serializer.data)


class RaceCategoryViewSet(CheckRaceExistenceMixin, viewsets.ModelViewSet):
    queryset = RaceCategory.objects.all()
    serializer_class = RaceCategorySerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        race = Race.objects.get(id=self.kwargs['race_pk'])
        serializer.save(race=race)


class RaceTimingViewSet(CheckRaceExistenceMixin, viewsets.ModelViewSet):
    queryset = RaceTiming.objects.all()
    serializer_class = RaceTimingSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_timedelta(self):
        timing = get_object_or_404(self.queryset, race=self.kwargs['race_pk'])
        return timezone.now() - timing.time_started

    def get_avg_speed(self, race):
        timedelta = self.get_timedelta()
        timedelta_hours = timedelta.total_seconds() / 3600
        return float(race.distance) / timedelta_hours

    def save_participant_results(self, participant, avg_speed, timedelta):
        serializer = ParticipantSerializer(participant, data=self.request.data)
        if serializer.is_valid():
            serializer.save(avg_speed=avg_speed, finish_time=timedelta)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def measure(self, *args, **kwargs):
        race_pk = kwargs['race_pk']
        queryset = Participant.objects.all()
        participant = get_object_or_404(queryset, user=kwargs['pk'], race=race_pk)
        race = Race.objects.get(id=race_pk)
        avg_speed = self.get_avg_speed(race)
        timedelta = self.get_timedelta()
        return self.save_participant_results(participant, avg_speed, timedelta)

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(race=kwargs['race_pk'])
        serializer = RaceTimingSerializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        race = Race.objects.get(id=self.kwargs['race_pk'])
        if RaceTiming.objects.filter(race=race).exists():
            raise ValidationError('There is timing for this race')
        serializer.save(race=race)


class ParticipantViewSet(CheckRaceExistenceMixin, viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.filter(race=kwargs['race_pk'])
        serializer = ParticipantSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        participant = get_object_or_404(self.queryset, user=kwargs['pk'], race=kwargs['race_pk'])
        serializer = ParticipantSerializer(participant)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        participant = get_object_or_404(self.queryset, user=kwargs['pk'], race=kwargs['race_pk'])
        self.perform_destroy(participant)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def set_participant_category(self, age):
        race_categories = RaceCategory.objects.filter(race=self.kwargs['race_pk'])
        for category in race_categories:
            if category.min_age < age <= category.max_age:
                return category
        return None

    @staticmethod
    def calculate_age(date_of_birth):
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def perform_create(self, serializer):
        if Participant.objects.filter(user=self.request.user.id, race=self.kwargs['race_pk']):
            raise ValidationError('You are already registered for this race')
        race = Race.objects.get(id=self.kwargs['race_pk'])
        age = self.calculate_age(self.request.user.date_of_birth)
        participant_category = self.set_participant_category(age)
        serializer.save(user=self.request.user, race=race, age=age, category=participant_category)







