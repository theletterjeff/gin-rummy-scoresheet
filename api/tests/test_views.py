from datetime import datetime, timedelta, timezone
from unittest import mock

from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from accounts.models import Player
from base.models import Game, Match, Score

class TestViews(TestCase):

    fixtures = ['accounts', 'base']

    def test_get_match(self):
        """
        Calling getMatch with a valid pk returns the Match with that pk.
        """
        client = APIClient()
        url = reverse('get_match', kwargs={'pk': '1'})
        
        response = client.get(url)

        # Check that response is working
        self.assertEqual(response.status_code, 200)
        
        # Test response data against target data
        target_data = {
            'id': 1,
            'datetime_started': '2022-04-02T20:08:37.108472Z',
            'datetime_ended': None,
            'target_score': 500,
            'complete': False,
            'players': [],
        }
        self.assertEqual(response.data, target_data)

    def test_get_game(self):
        """
        Calling getGame with a valid pk returns the Game with that pk.
        """
        client = APIClient()
        url = reverse('get_game', kwargs={'pk': '1'})
        
        response = client.get(url)

        # Check that response is working
        self.assertEqual(response.status_code, 200)

        # Test response data against target data
        target_data = {
            'id': 1,
            'points': 400,
            'gin': False,
            'undercut': False,
            'datetime_played': '2022-04-03T13:00:00Z',
            'match': 4,
            'winner': 2,
            'loser': 1,
        }
        self.assertEqual(response.data, target_data)