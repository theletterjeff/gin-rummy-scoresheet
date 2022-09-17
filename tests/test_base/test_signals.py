from datetime import datetime
import json
import pytz
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from accounts.models import Player
from base.models import Game, Match, Outcome, Score
from tests.fixtures import make_player, player0, player1, auth_client

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


class TestSignals(TestCase):
    """
    Test signals for Base models.
    """
    fixtures = ['accounts', 'base']

    def test_update_score(self):
        """
        When a Game is entered, the .player_score attribute of Score
        records are updated.
        """
        # Load data from fixtures
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        match = Match.objects.get(pk=2)

        # Create a Game that player1 got 50 points from
        Game.objects.create(
            match=match,
            winner=player1,
            loser=player2,
            points=50,
        )

        # Assert that player1's new Score is 50, player2's score is 0
        self.assertEqual(
            Score.objects.get(match=match, player=player1).player_score,
            50
        )
        self.assertEqual(
            Score.objects.get(match=match, player=player2).player_score,
            0
        )

        # Create a Game that player 2 got 25 points from
        Game.objects.create(
            match=match,
            winner=player2,
            loser=player1,
            points=25,
        )

        # Assert that player1's Score is still 50 and player2's score is 25
        self.assertEqual(
            Score.objects.get(match=match, player=player1).player_score,
            50
        )
        self.assertEqual(
            Score.objects.get(match=match, player=player2).player_score,
            25
        )
    
    def test_unfinished_matches_do_not_have_outcome_instances(self):
        """
        Unfinished Match instances do not have associated Outcome instances.
        """
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        match = Match.objects.get(pk=2)

        self.assertEqual(match.target_score, 500)
        self.assertFalse(match.complete)

        # Assert that Outome objects for the Match do not yet exist
        self.assertRaises(
            Outcome.DoesNotExist,
            Outcome.objects.get,
            match=match,
            player=player1,
        )
        self.assertRaises(
            Outcome.DoesNotExist,
            Outcome.objects.get,
            match=match,
            player=player2,
        )
    
    def test_finish_match(self):
        """
        When one player's Score.player_score exceed Match.target_score,
        the Match is marked as complete, the winner's Outcome.player_outcome
        is set as 1, and the loser's Outcome.player_outcome is set as 0.
        """
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        match = Match.objects.get(pk=2)

        # Add a Game whose .points are equal to Match.target_score
        Game.objects.create(
            match=match,
            winner=player1,
            loser=player2,
            points=500,
        )

        winner_outcome = Outcome.objects.get(player=player1, match=match)
        loser_outcome = Outcome.objects.get(player=player2, match=match)

        self.assertEqual(winner_outcome.player_outcome, 1)
        self.assertEqual(loser_outcome.player_outcome, 0)

    def test_delete_game_remove_score_points(self):
        """
        When Game is deleted, remove its points from the associated
        Score objects.
        """
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        match = Match.objects.get(pk=2)

        game = Game.objects.create(
            match=match,
            winner=player1,
            loser=player2,
            points=50,
        )

        self.assertEqual(
            Score.objects.get(player=player1, match=match).player_score,
            50
        )

        game.delete()

        self.assertEqual(
            Score.objects.get(player=player1, match=match).player_score,
            0
        )
    
    def test_delete_game_deletes_outcomes(self):
        """
        When Game is deleted, if deleted points put the associated Match below
        its target_score, delete the associated Outcome objects.
        """
        # Load data from fixtures
        match = Match.objects.get(pk=4)
        player1 = Player.objects.get(pk=1)
        player2 = Player.objects.get(pk=2)

        # Verify that the Outcome instances exist
        try:
            Outcome.objects.get(match=match, player=player1, player_outcome=1)
            Outcome.objects.get(match=match, player=player2, player_outcome=0)
        except:
            assert False

        Game.objects.get(pk=2).delete()

        with self.assertRaises(Outcome.DoesNotExist):
            Outcome.objects.get(
                match=match, player=player1, player_outcome=1)
            Outcome.objects.get(
                match=match, player=player2, player_outcome=0)

    def test_delete_game_sets_completed_to_false(self):
        """
        When Game is deleted, if deleted points put the associated Match below
        its target_score, Match.complete changes to False.
        """
        Game.objects.get(pk=2).delete()
        self.assertFalse(Match.objects.get(pk=4).complete)
    
    def test_finish_match_adds_datetime_ended(self):
        """When a Score object for a Match exceeds the point threshold,
        the Match's `datetime_ended` attribute gets set to timezone.now().
        """
        target_date = datetime(2022, 1, 1, tzinfo=pytz.timezone('utc'))

        with mock.patch('django.utils.timezone.now', return_value=target_date):
            score = Score.objects.get(pk=1)
            score.player_score = 501
            score.save()

            match = Match.objects.get(pk=2)
            self.assertEqual(match.datetime_ended, target_date)