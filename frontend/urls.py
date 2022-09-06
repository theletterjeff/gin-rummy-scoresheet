from django.urls import include, path
from . import views

urlpatterns = [
    path('players/', views.PlayerList.as_view(), name='player-list'),
    path('players/<str:username>', views.PlayerDetail.as_view(), name='player-detail'),

    path('matches/<str:username>/', views.MatchList.as_view(), name='match-list'),
    path('matches/<int:match_pk>/', views.MatchDetail.as_view(), name='match-detail'),

    path('matches/<int:match_pk>/games/', views.GameList.as_view(), name='game-list'),
    path('matches/<int:match_pk>/games/<int:game_pk>', views.GameDetail.as_view(), name='game-detail'),
]