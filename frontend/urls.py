from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home(), name='home'),
    
    path('players/', views.player_list(), name='player-list'),
    path('players/<str:username>/', views.player_detail(), name='player-detail'),
    path('players/<str:username>/edit/', views.player_edit(), name='player-edit'),

    path('matches/<str:username>/', views.match_list(), name='match-list'),
    path('matches/<int:match_pk>/', views.match_detail(), name='match-detail'),
    path('matches/<int:match_pk>/edit/', views.match_edit(), name='match-edit'),

    path('matches/<int:match_pk>/games/', views.game_list(), name='game-list'),
    path('matches/<int:match_pk>/games/<int:game_pk>', views.game_detail(), name='game-detail'),
    path('matches/<int:match_pk>/games/<int:game_pk>/edit/', views.game_edit(), name='game-edit'),
]