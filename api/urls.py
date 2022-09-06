from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api-root'),

    path('player/<str:username>', views.PlayerDetail.as_view(), name='player-detail'),
    path('logged-in-player/', views.LoggedInPlayerDetail.as_view(), name='logged-in-player'),

    path('matches/<str:username>/', views.MatchList.as_view(), name='match-list'),
    path('matches/<int:match_pk>/', views.MatchDetail.as_view(), name='match-detail'),
    path('matches/create/', views.MatchCreate.as_view(), name='match-create'),

    path('matches/<int:match_pk>/games/', views.GameList.as_view(), name='game-list'),
    path('matches/<int:match_pk>/games/<int:game_pk>', views.GameDetail.as_view(), name='game-detail'),
    path('matches/<int:match_pk>/games/create/', views.GameCreate.as_view(), name='game-create'),

    path('scores/<str:username>/', views.ScoreList.as_view(), name='score-list'),
    path('scores/<str:username>/matches/<int:match_pk>/', views.ScoreDetail.as_view(), name='score-detail'),

    path('outcomes/<str:username>/', views.OutcomeList.as_view(), name='outcome-list'),
    path('outcomes/<str:username>/matches/<int:match_pk>/', views.OutcomeDetail.as_view(), name='outcome-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
