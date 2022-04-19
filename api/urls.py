from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api_root'),

    # List
    path('all-matches', views.AllMatches.as_view(), name='all_matches'),
    path('all-games', views.AllGames.as_view(), name='all_games'),
    path('all-players', views.AllPlayers.as_view(), name='all_players'),

    # Detail
    path('match/<str:pk>/', views.MatchDetail.as_view(), name='match_detail'),
    path('game/<str:pk>/', views.GameDetail.as_view(), name='game_detail'),
    path('players/<str:pk>/', views.PlayerDetail.as_view(), name='player_detail'),

    # Create
    path('create-match', views.CreateMatch.as_view(), name='create_match'),
    path('create-game', views.CreateGame.as_view(), name='create_game'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
