from datetime import datetime
import pytz
from unittest import mock

from django.test import TestCase

from accounts.models import Player
from base.models import Game, Match, Outcome, Score

class TestSignals(TestCase):
    """
    Test signals for Base models.
    """
    fixtures = ['accounts', 'base']

    def test_create_score(self):
        """
        When a Match is created, an associated Score is created for each
        Player playing in the Match.
        """
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        match = Match()
        match.save()

        for player_count, player in enumerate([player1, player2]):
            match.players.add(player)
            match.save()
            
            score_count = Score.objects.filter(match=match)
            self.assertEqual(len(score_count), player_count + 1)

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