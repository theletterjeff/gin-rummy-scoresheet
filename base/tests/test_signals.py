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
        player1 = Player.objects.get(username='player1')
        player2 = Player.objects.get(username='player2')

        # Load the Match fixture that doesn't have Players in it yet
        match = Match.objects.get(pk=1)

        # Add players
        match.players.add(player1)
        match.players.add(player2)
        match.save()

        # Assert that the starting scores for both players are 0
        self.assertEqual(
            Score.objects.get(match=match, player=player1).player_score,
            0
        )
        self.assertEqual(
            Score.objects.get(match=match, player=player2).player_score,
            0
        )

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
    
    def test_default_match_has_target_score_500_and_outcome_false(self):
        """
        Match instances that are created without any additional parameters
        have .target_score=500 and .complete=False..
        """
        match = Match()
        self.assertEqual(match.target_score, 500)
        self.assertFalse(match.complete)
    
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