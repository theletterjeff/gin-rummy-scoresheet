from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('players/', views.PlayerList.as_view(), name='player-list'),
    re_path('players/(?P<username>[a-zA-z]+.*)/$', views.PlayerDetail.as_view(), name='player-detail'),
    path('players/create/', views.PlayerCreate.as_view(), name='player-create'),
    path('logged-in-player/', views.LoggedInPlayerDetail.as_view(), name='logged-in-player'),

    re_path('matches/(?P<username>[a-zA-z]+.*)/$', views.MatchList.as_view(), name='match-list'),
    re_path('matches/(?P<match_pk>[0-9]+)/$', views.MatchDetail.as_view(), name='match-detail'),
    path('matches/create/', views.MatchCreate.as_view(), name='match-create'),

    re_path('matches/(?P<match_pk>[0-9]+)/games/$', views.GameList.as_view(), name='game-list'),
    re_path('matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/$', views.GameDetail.as_view(), name='game-detail'),
    re_path('matches/(?P<match_pk>[0-9]+)/games/create/$', views.GameCreate.as_view(), name='game-create'),

    re_path('scores/(?P<username>[a-zA-z]+.*)/$', views.ScoreList.as_view(), name='score-list'),
    re_path('scores/(?P<username>[a-zA-z]+.*)/matches/(?P<match_pk>[0-9]+)/$', views.ScoreDetail.as_view(), name='score-detail'),

    re_path('outcomes/(?P<username>[a-zA-z]+.*)/$', views.OutcomeList.as_view(), name='outcome-list'),
    re_path('outcomes/(?P<username>[a-zA-z]+.*)/matches/(?P<match_pk>[0-9]+)/$', views.OutcomeDetail.as_view(), name='outcome-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
