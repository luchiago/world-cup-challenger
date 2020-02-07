from django.conf.urls import url

from .views import MatchResults

urlpatterns = [
    url(r'^', MatchResults.as_view(), name='match_results'),
]
