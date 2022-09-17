"""
Tests for the models for the base app.
"""
from datetime import datetime, timezone, timedelta
from unittest import mock

from django.test import TestCase

from accounts.models import Player
from base.models import Match, Score
from tests.fixtures import *

### Match

def test_default_match_has_target_score_500_and_outcome_false(simple_match):
    """Match instances that are created without any additional parameters
    have .target_score=500 and .complete=False..
    """
    assert simple_match.target_score == 500
    assert simple_match.complete == False

def test_create_match_sets_datetime_started_to_now(mock_now, simple_match):
    """Creating a new Match sets the `datetime_started` attribute to now."""
    target_datetime = timezone.datetime(2022, 1, 1, 0, 0, tzinfo=timezone.utc)
    assert simple_match.datetime_started == target_datetime

def test_match_str(mock_now, simple_match):
    """String representation of a Match is '<date started string> (<pk>)',
    e.g., '01/01/22 (3)'.
    """
    target_str = f'01/01/22 ({simple_match.pk})'
    assert simple_match.__str__() == target_str

### Score

def test_score_str(mock_now, simple_match, simple_score):
    """String representation of Score object returns as 
    f'{self.player.username} {date_started_str} - {self.player_score} ({self.pk})'
    """
    target_str = f'player0 01/01/22 - 0 ({simple_score.pk})'
    assert simple_score.__str__() == target_str
