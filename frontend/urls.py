from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<str:username>/', views.player_detail, name='player-detail'),
    path('<str:username>/edit/', views.player_edit, name='player-edit'),
    path('<str:username>/matches/', views.match_list, name='match-list'),
    path('<str:username>/matches/<int:match_pk>/', views.match_detail, name='match-detail'),
    path('<str:username>/matches/<int:match_pk>/games/<int:game_pk>/', views.game_detail, name='game-detail'),
    path('<str:username>/matches/<int:match_pk>/games/<int:game_pk>/edit/', views.game_detail, name='game-edit'),
]