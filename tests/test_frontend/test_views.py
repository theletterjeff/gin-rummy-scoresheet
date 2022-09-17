from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.urls import reverse

import pytest

from frontend import views
from tests.fixtures import (make_player, authenticate_api_request,
                            logged_out_driver, player0, player1, auth_client,
                            simple_match, make_match, make_game,
                            incomplete_match_with_one_game)

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

@pytest.mark.parametrize(
        'view_name,kwargs',
        [('player-detail', {'username': 'player0'}),
         ('player-edit', {'username': 'player0'}),
         ('match-list', {'username': 'player0'}),
         ('match-detail', {'match_pk': 1}),
         ('game-detail', {'match_pk': 1, 'game_pk': 1}),
         ('game-edit', {'match_pk': 1, 'game_pk': 1})])
def test_views_redirect_if_not_logged_in(client, view_name, kwargs):
    """The `home` view redirects to the `login` page if the user is not 
    authenticated."""
    url = reverse(f'frontend:{view_name}', kwargs=kwargs)
    response = client.get(url)
    assert isinstance(response, HttpResponseRedirect)
    target_path = '/' + response.url
    assert reverse('login')[:-1] in target_path

@pytest.mark.parametrize(
        'view_name,kwargs',
        [('player-detail', {'username': 'player0'}),
         ('player-edit', {'username': 'player0'}),
         ('match-list', {'username': 'player0'}),
         ('match-detail', {'match_pk': 1}),
         ('game-edit', {'match_pk': 1, 'game_pk': 1})])
def test_views_return_200_response(
        incomplete_match_with_one_game, auth_client, view_name, kwargs):
    """Sending a GET request with valid API kwargs returns a 200 response."""
    url = reverse(f'frontend:{view_name}', kwargs=kwargs)
    response = auth_client.get(url)
    assert response.status_code == 200

@pytest.mark.parametrize(
        'view_name,kwargs',
        [('player-detail', {'username': 'xyz'}),
         ('player-edit', {'username': 'xyz'}),
         ('match-list', {'username': 'xyz'}),
         ('match-detail', {'match_pk': 1000}),
         ('game-detail', {'match_pk': 1000, 'game_pk': 1000}),
         ('game-edit', {'match_pk': 1000, 'game_pk': 1000})])
def test_views_return_404_with_invalid_lookup_kwargs(
        player0, simple_match, auth_client, view_name, kwargs):
    """Sending a GET request with invalid API kwargs returns a 404 response."""
    url = reverse(f'frontend:{view_name}', kwargs=kwargs)
    response = auth_client.get(url)
    assert isinstance(response, HttpResponseNotFound)
    assert response.status_code == 404
