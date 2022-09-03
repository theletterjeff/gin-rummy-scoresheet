from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api-root'),

    path('player/<str:username>', views.PlayerDetail.as_view(), name='player-detail'),

    path('matches/<str:username>/', views.MatchList.as_view(), name='match-list'),
    path('matches/<int:match_pk>/', views.MatchDetail.as_view(), name='match-detail'),
    path('matches/create/', views.MatchCreate.as_view(), name='match-create'),

    path('scores/<str:username>/', views.ScoreList.as_view(), name='score-list'),
    path('scores/<str:username>/matches/<int:match_pk>/', views.ScoreDetail.as_view(), name='score-detail'),

    path('outcomes/<str:username>/', views.ScoreList.as_view(), name='outcome-list'),
    path('outcomes/<str:username>/matches/<int:match_pk>/', views.ScoreDetail.as_view(), name='outcome-detail')

#     # List and Create
#     path('game/', views.GameList.as_view(), name='game-list-create'),
#     path('all-players/', views.PlayerList.as_view(), name='player-list'),

#     # Player matches (to refactor/rename later)
#     path('player-matches/', views.PlayerMatches.as_view(), name='player-matches'),

#     # Players
#     path('player-create/', views.PlayerCreate.as_view(), name='player-create'),
#     path('player/<str:username>/', views.PlayerDetail.as_view(), name='player-detail'),
#     path('logged-in-player/', views.LoggedInPlayerDetail.as_view(), name='logged-in-player'),

#     # Detail
#     path('match/<str:pk>/', views.MatchDetail.as_view(), name='match-detail'),
#     path('game/<str:pk>/', views.GameDetail.as_view(), name='game-detail'),
#     path('match/player-score/<str:pk>/', views.ScoreDetail.as_view(),
#          name='score-detail'),
#     path('match/player-outcome/<str:pk>/', views.OutcomeDetail.as_view(),
#          name='outcome-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
