from datetime import datetime
import re

from django.urls import reverse
from django.utils import timezone

import pytest

from rest_framework.test import APIRequestFactory, force_authenticate

from api.views import (MatchCreate, MatchDetail, MatchList, OutcomeDetail,
                       ScoreDetail, GameDetail, GameList, GameCreate, 
                       OutcomeList, ScoreList, PlayerDetail, PlayerList,
                       PlayerCreate, LoggedInPlayerDetail)
from base.models import Outcome, Score
from tests.fixtures import (make_match, make_matches, make_player, make_players,
                            make_game, make_games, authenticate_api_request,
                            mock_now)

def test_player_list(make_players, authenticate_api_request):
    """GET request to the PlayerList view returns multiple Player instances."""
    player_num = 5
    players = make_players(player_num)
    view = PlayerList.as_view()
    url = reverse('player-list')

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request)

    assert response.status_code == 200
    assert response.data['count'] == player_num

def test_player_detail(make_player, authenticate_api_request):
    """GET request to the PlayerDetail view returns the Player instance."""
    username = 'player0'
    player = make_player(username=username)
    kwargs = {'username': username}

    view = PlayerDetail.as_view()
    url = reverse('player-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', player, kwargs)
    response = view(request, **kwargs)

    assert response.status_code == 200
    assert response.data

def test_player_create(db):
    """POST request to PlayerCreate view creates a new player."""
    factory = APIRequestFactory()
    url = reverse('player-create')
    view = PlayerCreate.as_view()
    kwargs = {'username': 'player0', 'password': 'test_password'}

    request = factory.post(url, kwargs)
    response = view(request, kwargs)

    assert response.status_code == 201
    assert response.data

def test_logged_in_player(make_player, authenticate_api_request):
    """GET request to the LoggedInPlayer view returns the logged-in Player's
    data.
    """
    player = make_player()
    view = LoggedInPlayerDetail.as_view()
    url = reverse('logged-in-player')
    request = authenticate_api_request(view, url, 'get', player)
    response = view(request)

    assert response.status_code == 200
    assert response.data['username'] == player.username

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

def test_match_create(make_players, authenticate_api_request):
    """Sending a POST request to the MatchCreate view creates a new Match."""
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

@pytest.mark.parametrize('game_count', [2, 4, 6])
def test_game_list(game_count, make_players, make_match, make_games, 
                   authenticate_api_request):
    """GameList view returns list of Game instances for a Match instance."""
    players = make_players(2)
    match = make_match(players)
    winners = [players[0], players[1]] * int(game_count / 2)
    losers = [players[1], players[0]] * int(game_count / 2)
    points = [5, 10] * int(game_count / 2)

    games = make_games(num=game_count, match=match, winners=winners,
                       losers=losers, points=points)
    
    view = GameList.as_view()
    kwargs = {'match_pk': match.pk}
    url = reverse('game-list', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.status_code == 200
    assert response.data['count'] == game_count
    assert len(response.data['results']) == game_count

def test_game_detail_get(make_players, make_match, make_game,
                         authenticate_api_request, mock_now):
    """A GET request to the GameDetail view returns a Game instance."""
    players = make_players(2)
    match = make_match(players)
    winner = players[0]
    loser = players[1]
    points = 50

    game = make_game(match, winner, loser, points)

    view = GameDetail.as_view()
    kwargs = {'match_pk': match.pk, 'game_pk': game.pk}
    url = reverse('game-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.status_code == 200
    assert response.data['url'].endswith(url)
    assert response.data['match'].endswith(match.get_absolute_url())
    assert response.data['winner'].endswith(winner.get_absolute_url())
    assert response.data['loser'].endswith(loser.get_absolute_url())
    assert response.data['points'] == 50
    assert response.data['gin'] == False
    assert response.data['undercut'] == False

    datetime_played_str = response.data['datetime_played']
    datetime_played = datetime.strptime(
        datetime_played_str, '%Y-%m-%dT%H:%M:%S%z')
    assert datetime_played == timezone.datetime(
            2022, 1, 1, 0, 0, tzinfo=timezone.utc)

def test_game_detail_patch(make_players, make_match, make_game,
                           authenticate_api_request):
    """A PATCH request to the GameDetail view updates the Game instance."""
    players = make_players(2)
    match = make_match(players)
    winner = players[0]
    loser = players[1]
    points = 50

    game = make_game(match, winner, loser, points)

    view = GameDetail.as_view()
    url_kwargs = {'match_pk': match.pk, 'game_pk': game.pk}
    url = reverse('game-detail', kwargs=url_kwargs)

    patch_kwargs = {'gin': True, 'undercut': True}
    patch_kwargs.update(url_kwargs)

    request = authenticate_api_request(view, url, 'patch', players[0], patch_kwargs)
    response = view(request, **patch_kwargs)

    assert response.status_code == 200
    assert response.data['gin'] == True
    assert response.data['undercut'] == True

def test_game_detail_delete(make_players, make_match, make_game,
                            authenticate_api_request):
    """DELETE request to the GameDetail view deletes Game instance."""
    players = make_players(2)
    match = make_match(players)
    winner = players[0]
    loser = players[1]
    points = 50

    game = make_game(match, winner, loser, points)

    view = GameDetail.as_view()
    kwargs = {'match_pk': match.pk, 'game_pk': game.pk}
    url = reverse('game-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'delete', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.status_code == 204
    assert not response.data

def test_game_create(make_players, make_match, make_game, authenticate_api_request):
    """A POST request to the GameCreate view creates a new Game."""
    players = make_players(2)
    match = make_match(players)
    url_kwargs = {'match_pk': match.pk}
    url = reverse('game-create', kwargs=url_kwargs)
    
    create_kwargs = {
        'match': match.get_absolute_url(),
        'winner': players[0].get_absolute_url(),
        'loser': players[1].get_absolute_url(),
        'points': 55,
        'gin': True,
        'undercut': False,
    }

    view = GameCreate.as_view()
    request = authenticate_api_request(view, url, 'post',
            players[0], create_kwargs)
    response = view(request, **create_kwargs)
    
    assert response.status_code == 201, response.data

def test_score_list(make_players, make_matches, authenticate_api_request):
    players = make_players(2)
    match = make_matches(3, players)
    kwargs = {'username': players[0].username}
    
    view = ScoreList.as_view()
    url = reverse('score-list', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.data['count'] == 3

def test_score_detail_get(make_players, make_match, authenticate_api_request):
    """Sending a GET request to the ScoreDetail view returns a response
    containing data on the requested Score instance.
    """
    players = make_players(2)
    match = make_match(players)     # Signal creates Score for each Player

    kwargs = {'username': players[0].username, 'match_pk': match.pk}
    view = ScoreDetail.as_view()
    url = reverse('score-detail', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0])
    response = view(request, **kwargs)
    
    assert response.status_code == 200
    assert response.data['url'].endswith(url)
    assert response.data['match'].endswith(match.get_absolute_url())
    assert response.data['player'].endswith(players[0].get_absolute_url())
    assert response.data['player_score'] == 0

def test_outcome_list(make_players, make_matches, authenticate_api_request):
    """A GET request to the OutcomeList view returns Outcome instances."""
    players = make_players(2)
    match_count = 3
    matches = make_matches(match_count, players)
    outcomes = [Outcome.objects.create(
            match=matches[i],
            player=players[0],
            player_outcome=1,
        ) for i in range(match_count)]

    kwargs = {'username': players[0].username}
    
    view = OutcomeList.as_view()
    url = reverse('outcome-list', kwargs=kwargs)

    request = authenticate_api_request(view, url, 'get', players[0], kwargs)
    response = view(request, **kwargs)

    assert response.data['count'] == match_count

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
