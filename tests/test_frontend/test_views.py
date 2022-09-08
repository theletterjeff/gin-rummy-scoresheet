from django.http import HttpResponseRedirect
from django.urls import reverse

from frontend import views
from tests.fixtures import make_player, authenticate_api_request

def test_home_view(authenticate_api_request, make_player):
    """The 'home' view redirects to the 'match-list' page."""
    view = views.home
    url = reverse('frontend:home')
    http_method = 'get'
    player = make_player()

    request = authenticate_api_request(view_func=view, url=url, 
                                       http_method=http_method, player=player)
    response = view(request)

    assert isinstance(response, HttpResponseRedirect)
    assert response.url == reverse('frontend:match-list',
                                   kwargs={'username': player.username})
