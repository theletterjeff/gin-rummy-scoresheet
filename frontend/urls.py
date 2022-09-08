from django.urls import include, path, re_path
from . import views

app_name = 'frontend'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/$', views.player_detail, name='player-detail'),
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/edit-profile/$', views.player_edit, name='player-edit'),

    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/matches/$', views.match_list, name='match-list'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/$', views.match_detail, name='match-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/edit/$', views.match_edit, name='match-edit'),

    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/$', views.game_detail, name='game-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/edit/$', views.game_edit, name='game-edit'),
]