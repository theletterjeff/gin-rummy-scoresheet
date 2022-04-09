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
