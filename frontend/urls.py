from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('match/', views.matches, name='matches-all'),
    path('match/<int:match_id>/', views.match, name='match-detail'),
    path('game/<int:game_id>/', views.game_edit, name='game-edit'),
    path('player/<int:player_id>/', views.player_profile, name='player-profile'),
    path('player/<int:player_id>/edit/', views.player_edit, name='player-edit'),
]