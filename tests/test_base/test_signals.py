from datetime import datetime
import json
import pytz
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from accounts.models import Player
from base.models import Game, Match, Outcome, Score
from tests.fixtures import *

def test_create_score_with_client(player0, player1, auth_client, transactional_db):
    """When a Match is created through a POST request, an associated Score is 
    created for each Player playing in the Match.
    """
    match_create_endpoint = reverse('api:match-create')
    test_server_prefix = 'http://testserver'
    player0_url = test_server_prefix + player0.get_absolute_url()
    player1_url = test_server_prefix + player1.get_absolute_url()

    body = {
        'players': [
            player0_url,
            player1_url,
        ],
        'target_score': 400
    }
    response = auth_client.post(match_create_endpoint, body)
    content = json.loads(response.content)

    match_pk = content['url'].split('/')[-2]
    match = Match.objects.get(pk=match_pk)

    assert Score.objects.get(player=player0)
    assert Score.objects.get(player=player1)

    assert Score.objects.get(player=player0).player_score == 0
    assert Score.objects.get(player=player1).player_score == 0

    assert len(Score.objects.filter(match=match)) == 2

def test_create_score_with_obj_manager(player0, player1, db):
    """When a Match is created with the model manager, an associated Score is 
    created for each Player playing in the Match.
    """
    match = Match.objects.create()
    match.players.set([player0, player1])
    match.save()

    assert Score.objects.get(player=player0)
    assert Score.objects.get(player=player1)

    assert Score.objects.get(player=player0).player_score == 0
    assert Score.objects.get(player=player1).player_score == 0

    assert len(Score.objects.filter(match=match)) == 2

def test_update_score_on_game_creation(
        player0, player1, simple_match, simple_game):
    """Creating a Game (`simple_game`) updates the Score object for the winner 
    by the amount of points in the `points` attribute.
    """
    score = Score.objects.get(player=player0, match=simple_match)
    assert score.player_score == 25

def test_update_score_on_game_edit(
        player0, player1, simple_match, simple_game):
    """Editing a Game's `.points` value updates the Match's Score."""
    simple_game.points = 50
    simple_game.save()

    score = Score.objects.get(player=player0, match=simple_match)
    assert score.player_score == 50

def test_unfinished_matches_do_not_have_outcome_instances(
        player0, player1, simple_match):
    """Unfinished Match instances do not have associated Outcome instances."""
    with pytest.raises(Outcome.DoesNotExist):
        Outcome.objects.get(player=player0, match=simple_match)
        Outcome.objects.get(player=player1, match=simple_match)

def test_finish_match(
        player0, player1, simple_match, winning_game,
        player0_outcome, player1_outcome):
    """When one player's Score.player_score exceed Match.target_score,
    the Match is marked as complete, the winner's Outcome.player_outcome
    is set as 1, and the loser's Outcome.player_outcome is set as 0.
    """
    assert player0_outcome.player_outcome == 1
    assert player1_outcome.player_outcome == 0

    simple_match.refresh_from_db()
    assert simple_match.complete == True
    assert simple_match.datetime_ended

def test_delete_game_removes_score_points(
        player0, simple_match, simple_game, simple_score):
    """When Game is deleted, remove its points from the associated
    Score objects.
    """
    assert simple_score.player_score == 25
    simple_game.delete()

    score = Score.objects.get(player=player0, match=simple_match)
    assert score.player_score == 0

def test_delete_game_deletes_outcomes_and_sets_completed_to_false(
        player0, player1, simple_match, winning_game):
    """When Game is deleted, if deleted points put the associated Match below
    its target_score, delete the associated Outcome objects.
    """
    assert Outcome.objects.count() == 2
    winning_game.delete()

    assert Outcome.objects.count() == 0
    assert simple_match.complete == False
