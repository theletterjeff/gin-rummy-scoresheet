from django.urls import include, path, re_path
from . import views

urlpatterns = [
    re_path(r'^players/(?P<username>[a-zA-z]+.*)/$', views.player_detail, name='player-detail'),
    re_path(r'^players/(?P<username>[a-zA-z]+.*)/edit-profile/$', views.player_edit, name='player-edit'),

    re_path(r'^players/(?P<username>[a-zA-Z]+.*)/matches/$', views.match_list, name='match-list'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/$', views.match_detail, name='match-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/edit/$', views.match_edit, name='match-edit'),

    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/$', views.game_detail, name='game-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/edit/$', views.game_edit, name='game-edit'),
]