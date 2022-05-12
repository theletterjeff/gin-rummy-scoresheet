from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenRefreshView, TokenVerifyView)
from . import views

urlpatterns = [
    
    # Root
    path('', views.api_root, name='api-root'),

    # List and Create
    path('match', views.MatchList.as_view(), name='match-list-create'),
    path('game', views.GameList.as_view(), name='game-list-create'),
    path('all-players', views.PlayerList.as_view(), name='player-list'),

    # Create new Player
    path('player-create/', views.PlayerCreate.as_view(), name='player-create'),

    # Detail
    path('match/<str:pk>/', views.MatchDetail.as_view(), name='match-detail'),
    path('game/<str:pk>/', views.GameDetail.as_view(), name='game-detail'),
    path('player/<str:pk>/', views.PlayerDetail.as_view(), name='player-detail'),

    # JWT
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
