from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('match/<int:match_id>', views.match, name='match-detail'),

    # path('', include('django.contrib.auth.urls')),
]