from .views import BlogViewSet
from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'blog', BlogViewSet)

urlpatterns = [
    url('^', include(router.urls))
]