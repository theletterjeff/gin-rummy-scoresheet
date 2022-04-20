from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api-root'),

    # List
    path('all-matches', views.AllMatches.as_view(), name='all-matches'),
    path('all-games', views.AllGames.as_view(), name='all-games'),
    path('all-players', views.AllPlayers.as_view(), name='all-players'),

    # Detail
    path('match/<str:pk>/', views.MatchDetail.as_view(), name='match-detail'),
    path('game/<str:pk>/', views.GameDetail.as_view(), name='game-detail'),
    path('player/<str:pk>/', views.PlayerDetail.as_view(), name='player-detail'),

    # Create
    path('create-match', views.CreateMatch.as_view(), name='create-match'),
    path('create-game', views.CreateGame.as_view(), name='create-game'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
