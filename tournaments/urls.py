from django.conf.urls import url

from .views import (tournament_list, tournament_matches_list,
                    tournament_teams_list, tournament_ranking)

urlpatterns = [
    url(r'^$', tournament_list, name='tournament_list'),
    url(r'^teams/', tournament_teams_list, name='tournament_teams_list'),
    url(r'^matches/', tournament_matches_list, name='tournament_matches_list'),
    url(r'^rankings/', tournament_ranking, name='tournament_ranking')
]
