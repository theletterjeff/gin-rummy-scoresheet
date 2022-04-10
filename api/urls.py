from django.urls import path
from . import views

urlpatterns = [
    path('', views.getAllMatches, name='all_matches'),
]