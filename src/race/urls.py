from .views import RaceList, RaceCreate
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', RaceList.as_view()),
    url(r'^create', RaceCreate.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)