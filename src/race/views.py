from .models import Race
from .serializers import RaceSerializer
from rest_framework import generics, permissions


class RaceList(generics.ListAPIView):
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class RaceCreate(generics.CreateAPIView):
    serializer_class = RaceSerializer
    permission_classes = (permissions.IsAdminUser,)
