from django.test.client import Client
from rest_framework.test import APIClient
from selenium.webdriver.firefox.webdriver import WebDriver

from accounts.models import Player
from base.models import Match
from tests.fixtures import (make_player, make_players, make_match, make_matches,
                            log_in_client, log_in_api_client, logged_out_driver,
                            log_in_driver)

def test_make_player(make_player):
    """The `make_player` factory returns a single Player instance."""
    player = make_player('player0')
    assert isinstance(player, Player)
    assert player.username == 'player0'
    Player.objects.get(username='player0')

def test_make_player_default_username(make_player):
    """The `make_player` factory without a `username` argument specified
    returns a Player instance with username 'player0'.
    """
    player = make_player()
    assert player.username == 'player0'

def test_make_players_without_existing_player(make_players):
    """The `make_players` factory returns a list of Player instances
    whose usernames are numbered sequentially starting at 0 (e.g., 
    'player0', 'player1', ...).
    """
    players = make_players(3)
    assert len(players) == 3
    assert all([players[i].username == f'player{i}' for i in range(3)])
    assert all([isinstance(player, Player) for player in players])

    for i in range(3):
        Player.objects.get(username=f'player{i}')

def test_make_players_with_existing_player(make_player, make_players):
    """The `make_players` factory returns a list of Player instances
    whose usernames are numbered sequentially starting at the lowest 
    number that isn't already used in a Player username (e.g., if 
    'player0' exists, the first instance would be 'player1').
    """
    make_player('player0')
    new_players = make_players(3)
    all_players = Player.objects.all()

    assert len(new_players) == 3
    assert len(all_players) == 4

    first_target_usernames = [f'player{i}' for i in range(1, 4)]
    new_player_usernames = [player.username for player in new_players]
    assert set(first_target_usernames) == set(new_player_usernames)
    assert 'player0' not in new_player_usernames

    for i in range(4):
        Player.objects.get(username=f'player{i}')
    
    newer_players = make_players(3)
    second_target_usernames = [f'player{i}' for i in range(4, 7)]
    newer_player_usernames = [player.username for player in newer_players]
    assert set(second_target_usernames) == set(newer_player_usernames)

def test_make_match_creates_match(make_match, make_players):
    """The `make_match` fixture returns a single Match object with the
    `.players` attribute populated by the players passed to the fixture.
    The Match appears in the database.
    """
    players = make_players(2)
    match = make_match(players=players)

    assert isinstance(match, Match)
    assert list(match.players.all()) == players
    Match.objects.get(pk=1)
    assert len(Match.objects.all()) == 1

def test_make_match_called_twice_creates_two_matches(make_match, make_players):
    """The fixture `make_match` can be called multiple times without raising
    an IntegrityError. Doing so will create multiple Match instances.
    """
    players = make_players(2)
    match1 = make_match(players=players)
    match2 = make_match(players=players)

    for match in [match1, match2]:
        assert isinstance(match, Match)
        assert list(match.players.all()) == players
    
    assert len(Match.objects.all()) == 2

def test_make_matches_creates_matches(make_matches, make_players):
    """The fixture `make_matches` creates the number of Match instances 
    passed as `num` to the fixture. These Match instances appear in the 
    database.
    """
    players = make_players(2)
    matches = make_matches(3, players)

    assert len(matches) == 3
    assert all([isinstance(match, Match) for match in matches])
    assert len(Match.objects.all()) == 3

def test_make_matches_called_after_make_match_makes_matches(
        make_match, make_matches, make_players):
    """The fixture `make_matches` can be called after `make_match` and 
    create new Match instances without raising an IntegrityError.
    """
    players = make_players(2)
    match = make_match(players)
    matches = make_matches(2, players)

    assert len(Match.objects.all()) == 3

def test_make_matches_called_after_make_matches_makes_matches(
        make_matches, make_players):
    """The fixture `make_matches` can be called after `make_matches` and 
    create new Match instances without raising an IntegrityError.
    """
    players = make_players(2)
    matches1 = make_matches(2, players)
    matches2 = make_matches(2, players)

    assert len(Match.objects.all()) == 4

def test_log_in_client_returns_logged_in_client(log_in_client, make_player):
    """The `log_in_client` fixture returns a logged-in Client instance."""
    player = make_player()
    client = log_in_client(player)

    assert isinstance(client, Client)

    # sessionid cookie shows the client is logged in
    assert client.cookies.get('sessionid')

def test_log_in_api_client_returns_logged_in_api_client(
        log_in_api_client, make_player):
    """The `log_in_api_client` fixture returns a logged-in APIClient instance."""
    player = make_player()
    api_client = log_in_api_client(player)
    assert isinstance(api_client, APIClient)
    # _force_user shows that the client is logged in
    assert api_client.handler._force_user

def test_log_in_driver_returns_logged_in_driver(
        client, make_player, log_in_client, log_in_driver):
    """The `log_in_driver` fixture returns a logged-in Selenium driver."""
    player = make_player()
    driver = log_in_driver(player=player, client=client)
    
    assert isinstance(driver, WebDriver)
    assert driver.get_cookie('sessionid')

def test_log_in_driver_adds_csrf_token(
        client, make_player, log_in_client, log_in_driver):
    """The `log_in_driver` fixture returns a Selenium WebDriver instance
    with a CSRF token included in the cookies.
    """
    player = make_player()
    driver = log_in_driver(player=player, client=client)
    
    assert driver.get_cookie('csrftoken')

def test_logged_out_driver(logged_out_driver):
    """The `logged_out_driver` fixture returns a Selenium WebDriver
    instance that is not logged in.
    """
    assert isinstance(logged_out_driver, WebDriver)
    assert logged_out_driver.get_cookie('sessionid') is None
