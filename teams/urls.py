from django.conf.urls import url

from .views import TeamList

urlpatterns = [
    url(r'^', TeamList.as_view(), name='team_list'),
]
