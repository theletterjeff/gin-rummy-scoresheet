from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

app_name = 'api'
urlpatterns = [
    # Player
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/$', views.PlayerDetail.as_view(), name='player-detail'),
    re_path(r'^players/$', views.PlayerListAll.as_view(), name='player-list'),
    re_path(r'^players/create/$', views.PlayerCreate.as_view(), name='player-create'),
    re_path(r'^request-player/$', views.RequestPlayer.as_view(), name='request-player'),

    # Lists by Player
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/matches/$', views.MatchListPlayer.as_view(), name='match-list-player'),
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/games/$', views.GameListPlayer.as_view(), name='game-list-player'),
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/scores/$', views.ScoreListPlayer.as_view(), name='score-list-player'),
    re_path(r'^players/(?P<username>[a-zA-Z]+\w*)/outcomes/$', views.OutcomeListPlayer.as_view(), name='outcome-list-player'),

    # Match
    re_path(r'^matches/(?P<match_pk>[0-9]+)/$', views.MatchDetail.as_view(), name='match-detail'),
    re_path(r'^matches/create/$', views.MatchCreate.as_view(), name='match-create'),
    
    # Lists by Match
    re_path(r'^matches/(?P<match_pk>[0-9]+)/players/$', views.PlayerListMatch.as_view(), name='player-list-match'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/$', views.GameListMatch.as_view(), name='game-list-match'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/scores/$', views.ScoreListMatch.as_view(), name='score-list-match'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/outcomes/$', views.OutcomeListMatch.as_view(), name='outcome-list-match'),    

    # Game
    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/$', views.GameDetail.as_view(), name='game-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/games/create/$', views.GameCreate.as_view(), name='game-create'),

    # Score and Outcome
    re_path(r'^matches/(?P<match_pk>[0-9]+)/players/(?P<username>[a-zA-Z]+\w*)/scores/$', views.ScoreDetail.as_view(), name='score-detail'),
    re_path(r'^matches/(?P<match_pk>[0-9]+)/players/(?P<username>[a-zA-Z]+\w*)/outcomes/$', views.OutcomeDetail.as_view(), name='outcome-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
