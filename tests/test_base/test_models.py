"""
Tests for the models for the base app.
"""
from datetime import datetime, timezone, timedelta
from unittest import mock

from django.test import TestCase

from accounts.models import Player
from base.models import Match, Score

class TestMatchModel(TestCase):
    """
    Tests for the Match model.
    """
    fixtures = ['accounts', 'base']

    def test_default_match_has_target_score_500_and_outcome_false(self):
        """
        Match instances that are created without any additional parameters
        have .target_score=500 and .complete=False..
        """
        match = Match()
        self.assertEqual(match.target_score, 500)
        self.assertFalse(match.complete)
    
    @mock.patch('django.utils.timezone.now')
    def test_create_match_sets_datetime_started_to_now(self, mock_datetime):
        """
        Creating a new Match sets the `datetime_started` attribute to now.
        """
        tz = timezone(timedelta(hours=-4))
        mock_datetime.return_value = datetime(2022, 1, 1, tzinfo=tz)
        
        match = Match.objects.create()
        assert match.datetime_started == mock_datetime()

    def test_str(self):
        """
        String representation of a Match is '<date started string> (<pk>)',
        e.g., '01/01/22 (3)'.
        """
        # Load match from fixture
        match = Match.objects.get(pk=1)

        target_str = '04/02/22 (1)'

        self.assertEqual(match.__str__(), target_str)

class TestScoreModel(TestCase):
    """
    Tests for the Score model.
    """
    fixtures = ['accounts', 'base']
    
    def test_str(self):
        """
        String representation of a Match is 
        '<username> <date started string (<pk>) ({self.pk})',
        e.g., 'player1 04/02/22 (1)'
        """
        # Load score from fixture
        score = Score.objects.get(pk=1)

        target_str = 'player1 04/02/22 (1)'

        self.assertEqual(score.__str__(), target_str)