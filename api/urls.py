from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('all-matches', views.AllMatches.as_view(), name='all_matches'),
    path('all-games', views.AllGames.as_view(), name='all-games'),
    path('match/<str:pk>/', views.matchDetail, name='match_detail'),
    path('game/<str:pk>/', views.gameDetail, name='game_detail'),
    path('create-match', views.createMatch, name='create_match'),
    path('create-game', views.createGame, name='create_game'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
