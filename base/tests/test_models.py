"""
Tests for the models for the base app.
"""
from django.test import TestCase

from base.models import Match

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