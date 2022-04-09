from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllMatches, name='all_matches'),
    path('create-game/', views.createGame, name='create_game'),
]