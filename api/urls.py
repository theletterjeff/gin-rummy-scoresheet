from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('all-matches', views.AllMatches.as_view(), name='all_matches'),
    path('all-games', views.AllGames.as_view(), name='all-games'),
    path('match/<str:pk>/', views.MatchDetail.as_view(), name='match_detail'),
    path('game/<str:pk>/', views.GameDetail.as_view(), name='game_detail'),
    path('create-match', views.CreateMatch.as_view(), name='create_match'),
    path('create-game', views.CreateGame.as_view(), name='create_game'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
