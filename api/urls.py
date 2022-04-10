from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllMatches, name='all_matches'),
    path('get-match/<str:pk>/', views.getMatch, name='get_match'),
    path('get-game/<str:pk>/', views.getGame, name='get_game'),
]