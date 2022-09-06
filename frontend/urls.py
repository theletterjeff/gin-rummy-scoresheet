from django.urls import include, path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('players/', views.player_list, name='player-list'),
    re_path('players/(?P<username>[a-zA-z]+.*)/$', views.player_detail, name='player-detail'),
    re_path('players/(?P<username>[a-zA-z]+.*)/edit/$', views.player_edit, name='player-edit'),

    re_path('matches/(?P<username>[a-zA-z]+.*)/$', views.match_list, name='match-list'),
    re_path('matches/(?P<match_pk>[0-9]+)/$', views.match_detail, name='match-detail'),
    re_path('matches/(?P<match_pk>[0-9]+)/edit/$', views.match_edit, name='match-edit'),

    re_path('matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/$', views.game_detail, name='game-detail'),
    re_path('matches/(?P<match_pk>[0-9]+)/games/(?P<game_pk>[0-9]+)/edit/$', views.game_edit, name='game-edit'),
]