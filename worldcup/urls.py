from django.conf.urls import include, url
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^teams/', include(('teams.urls', 'teams'), namespace='teams')),
    url(r'^tournaments/', include(('tournaments.urls', 'tournaments'), namespace='tournaments')),
    url(r'^matches/', include(('matches.urls', 'matches'), namespace='matches')),

]
