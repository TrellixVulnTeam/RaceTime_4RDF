from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('race.urls')),
    url(r'^', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth/', include('djoser.urls.authtoken')),
]

