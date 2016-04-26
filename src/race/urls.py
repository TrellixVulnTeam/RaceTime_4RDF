from django.conf.urls import include, url
from .views import RaceViewSet, RaceCategoryViewSet, RaceTimingViewSet, ParticipantViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


router = DefaultRouter()
router.register(r'races', RaceViewSet)

races_router = routers.NestedSimpleRouter(router, r'races', lookup='race')
races_router.register(r'participants', ParticipantViewSet)
races_router.register(r'categories', RaceCategoryViewSet)
races_router.register(r'timing', RaceTimingViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(races_router.urls)),
]

