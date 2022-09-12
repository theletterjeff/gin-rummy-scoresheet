from django.http import HttpResponseRedirect
from django.urls import reverse

import pytest

from frontend import views
from tests.fixtures import (make_player, authenticate_api_request,
                            logged_out_driver)

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

@pytest.mark.parametrize('view_name', ['home', 'player-detail',
                                       'player-edit', 'match-list',
                                       'match-detail', 'game-detail',
                                       'game-edit'])
def test_views_redirect_if_not_logged_in(client, view_name):
    """The `home` view redirects to the `login` page if the user is not 
    authenticated."""
    url = reverse(f'frontend:{view_name}')
    response = client.get(url)
    assert isinstance(response, HttpResponseRedirect)
    assert reverse('login') in response.url
