"""RaceTime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from race.views import RaceViewSet,RaceCategoryViewSet, ParticipantViewSet

router = DefaultRouter()
router.register(r'races', RaceViewSet)

races_router = routers.NestedSimpleRouter(router, r'races', lookup='race')
races_router.register(r'participants', ParticipantViewSet)
races_router.register(r'categories', RaceCategoryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(races_router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('djoser.urls.authtoken')),
]
