from datetime import datetime
from typing import Callable, List

from django.middleware.csrf import get_token
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

import pytest
from rest_framework.test import APIClient, APIRequestFactory, force_authenticate

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from accounts.models import Player
from base.models import Game, Match


"""Players"""

@pytest.fixture
def make_player(db) -> Callable:
    """Factory as fixture for creating a new Player instance"""
    def _make_player(username: str = 'player0', password: str = 'test_password',
                     *args, **kwargs) -> Player:
        return Player.objects.create(username=username, password=password,
                                     *args, **kwargs)
    return _make_player

@pytest.fixture
def make_players(db, make_player) -> Callable:
    """Factory as fixture to return a list of Player instances."""
    def _make_players(num) -> List[Player]:
        start_num = -1

        # Make sure we aren't creating players that already exist
        while True:
            try:
                start_num += 1
                Player.objects.get(username=f'player{start_num}')
            except Player.DoesNotExist:
                break

        return [make_player(username=f'player{i}') for i
                in range(start_num, num + start_num)]
    return _make_players


"""Matches"""

@pytest.fixture
def make_match(db) -> Callable:
    """Factory as fixture for creating a single Match instance."""
    def _make_match(players: List[Player], *args, **kwargs) -> Match:
        match = Match.objects.create(*args, **kwargs)
        [match.players.add(player) for player in players]
        return match
    return _make_match

@pytest.fixture
def make_matches(db, make_match) -> Callable:
    """Factory as fixture for creating multiple Match instances."""
    def _make_matches(num: int, players: List[Player], *args, **kwargs) -> List[Match]:
        return [make_match(players, *args, **kwargs) for i in range(num)]
    return _make_matches


"""Games"""

@pytest.fixture
def make_game(db) -> Callable:
    """Factory as fixture for creating a single Game instance."""
    def _make_game(match: Match, winner: Player, loser: Player, points: int,
                   *args, **kwargs) -> Game:
        return Game.objects.create(match, winner, loser, points, *args, **kwargs)
    return _make_game

@pytest.fixture
def make_games(db, make_game) -> Callable:
    """Factory as fixture for creating multiple Game instances."""
    def _make_matches(num: int, match: Match, winner_loser: Tuple[Player, Player],
                      points: Tuple, *args, **kwargs) -> Tuple[Match]:
        return (_make_game(match, winner_loser[0], winner_loser[1], points,
                           *args, **kwargs) for i in range(num))
    return _make_games


"""Client/driver"""

@pytest.fixture
def log_in_client(client) -> Callable:
    """Factory as fixture, returns a logged-in Django test Client instance."""
    def _log_in_client(player: Player) -> Client:
        client.force_login(player)
        return client
    return _log_in_client

@pytest.fixture
def log_in_api_client() -> Callable:
    """Factory as fixture, returns a logged-in DRF API Client instance."""
    def _log_in_api_client(player: Player) -> APIClient:
        api_client = APIClient()
        api_client.force_authenticate(user=player)
        return api_client
    return _log_in_api_client

@pytest.fixture
def logged_out_driver():
    options = Options()
    options.headless = True
    return WebDriver(options=options)

@pytest.fixture
def log_in_driver(live_server, log_in_client, rf,   # Built-in
                  make_player) -> Callable:         # Have to import
    """Add sessionid and csrftoken cookies to a driver instance. The client
    passed to the `client` arg should not already be logged in.
    """
    def _log_in_driver(player: Player, client: Client) -> WebDriver:

        options = Options()
        options.headless = True
        driver = WebDriver(options=options)
        
        client = log_in_client(player)
        driver.get(live_server.url)

        session_id_cookie = client.cookies.get('sessionid')
        if not session_id_cookie:
            raise Exception('Client is not logged in.')

        driver.add_cookie(
            {
                'name': 'sessionid',
                'value': session_id_cookie.value,
                'secure': False,
                'path': '/',
            }
        )
        csrftoken = get_token(rf.get(live_server.url))
        driver.add_cookie(
            {
                'name': 'csrftoken',
                'value': csrftoken,
                'secure': False,
                'path': '/',
            }
        )
        return driver
    return _log_in_driver

@pytest.fixture
def authenticate_api_request(make_player) -> Callable:
    """Return an API Request object to pass to a view function."""
    def _authenticate_api_request(view_func, url: str, http_method: str,
                                  player: Player = None, *args, **kwargs):
        if not player:
            player = make_player()
        factory = APIRequestFactory()
        method_handler = {
            'get': factory.get,
            'post': factory.post,
            'put': factory.put,
            'patch': factory.patch,
            'delete': factory.delete,
        }
        request = method_handler[http_method](url, *args, **kwargs)
        force_authenticate(request, user=player)
        return request
    return _authenticate_api_request

@pytest.fixture
def mock_now(monkeypatch):
    def _mock_now():
        return timezone.datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc)
    monkeypatch.setattr(timezone, 'now', _mock_now)
    return monkeypatch