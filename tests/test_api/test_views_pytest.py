import re

from django.urls import reverse

import pytest

from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import (MatchCreate, MatchDetail, MatchList, OutcomeDetail,
                       ScoreDetail)
from base.models import Outcome, Score
from tests.fixtures import (make_match, make_matches, make_player, make_players,
                            authenticate_api_request)

def test_match_list_view_returns_no_records_when_no_records_present(
        make_player, authenticate_api_request):
    """The MatchList view returns no records when no Matches have been created.
    """
    player = make_player()
    kwargs = {'username': player.username}
    
    view = MatchList.as_view()
    url = reverse('match-list', kwargs=kwargs)

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
    url = reverse('match-list', kwargs=kwargs)

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
    url = reverse('match-list', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)

    assert response.data['count'] == match_num

def test_match_create_creates_new_match(make_players,
        authenticate_api_request):
    """Sending a POST request to the MatchCreate view creates a new Match.
    """
    players = make_players(2)
    player_urls = [player.get_absolute_url() for player in players]
    
    view = MatchCreate.as_view()
    url = reverse('match-create')
    kwargs = {'players': player_urls}

    request = authenticate_api_request(view, url, 'post', players[0], kwargs)

    response = view(request, kwargs)
    
    assert response.status_code == 201

    # Both of the players are in the `.players` set
    for player_url in player_urls:
        regex = re.compile(player_url)
        assert any([regex.search(response_player_url)
                    for response_player_url in response.data['players']])

def test_match_detail_get(make_players, make_match,
        authenticate_api_request):
    """GET requests to the MatchDetail view return Match instance."""
    players = make_players(2)
    match = make_match(players)
    kwargs = {'match_pk': match.pk}
    
    view = MatchDetail.as_view()
    url = reverse('match-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0], kwargs)
    response = view(request, **kwargs)

    assert url in response.data['url']

def test_match_detail_patch(make_players, make_match,
        authenticate_api_request):
    """PATCH requests to the MatchDetail view update Match instance."""
    players = make_players(2)
    match = make_match(players)
    url_kwargs = {'match_pk': match.pk}
    
    view = MatchDetail.as_view()
    url = reverse('match-detail', kwargs=url_kwargs)

    patch_kwargs = {'complete': True, 'target_score': 250}
    patch_kwargs.update(url_kwargs)

    request = authenticate_api_request(view, url, 'patch', players[0], patch_kwargs)
    response = view(request, **patch_kwargs)

    assert response.status_code == 200
    assert response.data['complete'] == True
    assert response.data['target_score'] == 250

def test_match_detail_delete(make_players, make_match, authenticate_api_request):
    """DELETE request to the MatchDetail view deletes Match instance."""
    players = make_players(2)
    match = make_match(players)
    kwargs = {'match_pk': match.pk}
    
    view = MatchDetail.as_view()
    url = reverse('match-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'delete', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.status_code == 204
    assert not response.data

def test_score_detail(make_players, make_match, authenticate_api_request):
    """Sending a GET request to the ScoreDetail view returns a response
    containing data on the requested Score instance.
    """
    players = make_players(2)
    match = make_match(players)
    score = Score.objects.create(player=players[0], match=match,
            player_score=250)
    
    kwargs = {'username': players[0].username, 'match_pk': match.pk}
    view = ScoreDetail.as_view()
    url = reverse('score-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)
    
    assert response.status_code == 200
    assert response.data['url'].endswith(url)
    assert response.data['match'].endswith(match.get_absolute_url())
    assert response.data['player'].endswith(players[0].get_absolute_url())
    assert response.data['player_score'] == 250

def test_outcome_detail(make_players, make_match, authenticate_api_request):
    """Sending a GET request to the OutcomeDetail view returns a response
    containing data on the requested Outcome instance.
    """
    players = make_players(2)
    match = make_match(players)
    outcome = Outcome.objects.create(player=players[0], match=match,
            player_outcome=1)
    
    kwargs = {'username': players[0].username, 'match_pk': match.pk}
    view = OutcomeDetail.as_view()
    url = reverse('outcome-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)
    
    assert response.status_code == 200
    assert response.data['url'].endswith(url)
    assert response.data['match'].endswith(match.get_absolute_url())
    assert response.data['player'].endswith(players[0].get_absolute_url())
    assert response.data['player_outcome'] == 1
