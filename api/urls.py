from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api-root'),

    # List and Create
    path('match', views.MatchList.as_view(), name='match-list-create'),
    path('game', views.GameList.as_view(), name='game-list-create'),
    path('all-players', views.PlayerList.as_view(), name='player-list'),

    # Detail
    path('match/<str:pk>/', views.MatchDetail.as_view(), name='match-detail'),
    path('game/<str:pk>/', views.GameDetail.as_view(), name='game-detail'),
    path('player/<str:pk>/', views.PlayerDetail.as_view(), name='player-detail'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
