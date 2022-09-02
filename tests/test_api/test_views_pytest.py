from django.urls import reverse

import pytest

from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import MatchList
from tests.fixtures import (make_match, make_matches, make_player, make_players,
                            authenticate_api_request)

def test_match_list_view_returns_no_records_when_no_records_present(
        make_player, authenticate_api_request):
    """The MatchList view returns no records when no Matches have been created.
    """
    player = make_player()
    kwargs = {'username': player.username}
    
    view = MatchList.as_view()
    url = reverse('match-list-create', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', player)
    response = view(request, **kwargs)
    
    assert response.data['count'] == 0

def test_match_list_view_returns_no_records_when_matches_are_w_other_players(
        make_players, make_match, authenticate_api_request):
    """The MatchList view returns no records when Matches have been created
    but the target Player is not included in their `players` attribute.
    """
    players = make_players(3)
    make_match(players=[players[1], players[2]])
    kwargs = {'username': players[0].username}

    view = MatchList.as_view()
    url = reverse('match-list-create', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)

    assert response.data['count'] == 0

@pytest.mark.parametrize('match_num', [1, 2, 10])
def test_match_list_view_returns_records_when_matches_are_with_player(
        make_players, make_matches, authenticate_api_request, match_num):
    """The MatchList view returns no records when Matches have been created
    but the target Player is not included in their `players` attribute.
    """
    players = make_players(2)
    make_matches(match_num, players=players)
    kwargs = {'username': players[0].username}

    view = MatchList.as_view()
    url = reverse('match-list-create', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)

    assert response.data['count'] == match_num

def test_match_reate_creates_new_match(make_players,
        authenticate_api_request):
    """Sending a POST request to the MatchCreate view creates a new Match.
    """
    pass