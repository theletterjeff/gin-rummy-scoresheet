from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('all-matches', views.getAllMatches, name='all_matches'),
    path('all-games', views.getAllGames, name='all-games'),
    path('get-match/<str:pk>/', views.getMatch, name='get_match'),
    path('get-game/<str:pk>/', views.getGame, name='get_game'),
    path('create-match', views.createMatch, name='create_match'),
    path('create-game', views.createGame, name='create_game'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
