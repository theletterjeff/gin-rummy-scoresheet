from typing import List

from django.middleware.csrf import get_token
from django.urls import reverse

import pytest
from rest_framework.test import APIClient

from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from accounts.models import Player
from base.models import Match


@pytest.fixture
def logged_in_client(client, player0):
    client.force_login(player0)
    return client

@pytest.fixture
def base_api_client():
    return APIClient()

@pytest.fixture
def api_client(base_api_client, player0):
    """Logged in APIClient"""
    base_api_client.force_authenticate(user=player0)
    return base_api_client

@pytest.fixture
def base_driver():
    options = Options()
    options.headless = True
    return WebDriver(options=options)

@pytest.fixture
def logged_in_driver(base_driver, live_server, logged_in_client, rf):
    session_id_cookie = logged_in_client.cookies['sessionid']
    base_driver.get(live_server.url)
    base_driver.add_cookie(
        {
            'name': 'sessionid',
            'value': session_id_cookie.value,
            'secure': False,
            'path': '/',
        }
    )
    csrftoken = get_token(rf.get(live_server.url))
    base_driver.add_cookie(
        {
            'name': 'csrftoken',
            'value': csrftoken,
            'secure': False,
            'path': '/',
        }
    )
    return base_driver

@pytest.fixture
def make_player(db):
    """Factory as fixture for creating a new Player instance"""
    def _make_player(username: str, password: str = 'test_password',
                     *args, **kwargs):
        return Player.objects.create(username=username, password=password,
                                     *args, **kwargs)
    return _make_player

@pytest.fixture
def make_players(db, make_player):
    """Factory as fixture for creating multiple Player instances.
    Returns a dictionary whose keys are sequentially numbered usernames
    (player0, player1, ...) and whose values are Player instances.
    """
    def _make_players(num):
        player_dict = {}
        for i in range(num):
            username = f'player{i}'
            player_dict[username] = make_player(username=username)
        return player_dict
    return _make_players

@pytest.fixture
def make_match(db):
    """Factory as fixture for creating matches"""
    def _make_match(players: List[Player], *args, **kwargs):
        match = Match.objects.create(*args, **kwargs)
        [match.players.add(player) for player in players]
        return match
    return _make_match

@pytest.fixture
def simple_match(db, make_players, make_match):
    """A Match instance with player0 and player1 as the `players` attr."""
    players = make_players(2)
    return make_match(players)
