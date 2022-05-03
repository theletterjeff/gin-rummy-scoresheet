from django.urls import path
from . import views

urlpatterns = [
    path('match/<int:match_id>', views.match, name='match-detail'),
]