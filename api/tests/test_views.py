from datetime import datetime
import pytz
from unittest import mock

from cgi import test
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient

from accounts.models import Player
from base.models import Game, Match, Score

class TestMatchViews(TestCase):

    fixtures = ['accounts', 'base']

    @classmethod
    def setUpClass(cls):
        """
        Authenticate player1, set base URL constant.
        """
        super().setUpClass()
        
        player = Player.objects.get(pk=1)
        
        cls.apiclient = APIClient()
        cls.apiclient.force_authenticate(user=player)

        # Set base URL
        cls.BASE_URL = 'http://testserver'

    def test_get_match(self):
        """
        Calling getMatch with a valid pk returns the Match with that pk.
        """
        url = reverse('match-detail', kwargs={'pk': '1'})
        
        response = self.apiclient.get(url)

        # Check that response is working
        self.assertEqual(response.status_code, 200)
        
        # Test response data against target data
        target_data = {
            'url': self.BASE_URL + url,
            'datetime_started': '2022-04-02T20:08:37.108472Z',
            'datetime_ended': None,
            'target_score': 500,
            'complete': False,
            'players': [],
            'created_by': (
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '1'})
            ),
            'games': [],
        }

        # Test each response value individually
        # (testing equivalence between two dicts abbreviated datetime value)
        for key, value in response.data.items():
            self.assertEqual(value, target_data[key])
            del(target_data[key])
        
        # After testing all items, there are no remaining target_data items
        self.assertEqual(len(target_data), 0)
    
    def test_get_invalid_match(self):
        """
        Calling getMatch with an invalid pk returns ???
        """
        url = reverse('match-detail', kwargs={'pk': '9999'})
        response = self.apiclient.get(url)

        self.assertEqual(response.status_code, 404)

    def test_create_match(self):
        """
        Sending valid JSON data to the `/create-match/` endpoint
        creates a new Match.
        """
        url = reverse('create-match')
        data = {
            'target_score': 12345,
            'players': [
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '1'}),
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '2'}),
            ]
        }

        self.apiclient.post(url, data=data)

        try:
            Match.objects.get(target_score=12345)
        except Match.DoesNotExist:
            assert False

    def test_suffix_patterns(self):
        """
        Making a request to the all_matches endpoint with a URL
        ending in .json returns a JSON object. Doing the same
        with a URL ending in HTML returns an HTML object.
        """
        url_json = reverse('all-matches') + '.json'
        url_browsable_api = reverse('all-matches') + '.api'
        
        response_json = self.apiclient.get(url_json)
        response_browsable_api = self.apiclient.get(url_browsable_api)

        self.assertEqual(response_json.accepted_media_type, 'application/json')
        self.assertEqual(response_browsable_api.accepted_media_type,
            'text/html')
    
    def test_update_match(self):
        """
        Sending a PATCH request to the match_detail URL endpoint for match 1
        with data update {'target_score': 1000} updates match 1's target_score
        to 1000.
        """
        url = reverse('match-detail', kwargs={'pk': '1'})
        update_data = {'target_score': 1000}
        
        response = self.apiclient.patch(url, data=update_data)
        
        # Test response data against target data
        self.assertEqual(response.data['target_score'], 1000)
    
    def test_delete_match(self):
        """
        Sending a DELETE request to the match_detail URL endpoint for match 1
        deletes match 1.
        """
        url = reverse('match-detail', kwargs={'pk': '1'})

        response = self.apiclient.delete(url)
        self.assertEqual(response.status_code, 204)

        # Making a GET call to the resource returns a 404 error
        self.assertEqual(self.apiclient.get(url).status_code, 404)
    
    def test_pagination(self):
        """
        Having more than 10 matches in the database returns datasets with only
        10 matches per page.
        """
        # Create 9 matches (to bring total to 11)
        for i in range(9):
            Match.objects.create()

        url = reverse('all-matches')
        response = self.apiclient.get(url)
        
        self.assertEqual(response.data['count'], 13)
        self.assertEqual(len(response.data['results']), 10)

class TestGameViews(TestCase):

    fixtures = ['accounts', 'base']

    @classmethod
    def setUpClass(cls):
        """
        Authenticate player1, set base URL constant.
        """
        super().setUpClass()
        
        player = Player.objects.get(pk=1)
        
        cls.apiclient = APIClient()
        cls.apiclient.force_authenticate(user=player)

        # Set base URL
        cls.BASE_URL = 'http://testserver'

    def test_get_game(self):
        """
        Calling getGame with a valid pk returns the Game with that pk.
        """
        url = reverse('game-detail', kwargs={'pk': '1'})
        
        response = self.apiclient.get(url)

        # Check that response is working
        self.assertEqual(response.status_code, 200)

        # Test response data against target data
        target_data = {
            'url': self.BASE_URL + url,
            'points': 400,
            'gin': False,
            'undercut': False,
            'datetime_played': '2022-04-03T13:00:00Z',
            'match': (
                self.BASE_URL + reverse('match-detail', kwargs={'pk': '4'})
            ),
            'winner': (
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '2'})
            ),
            'loser': (
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '1'})
            ),
            'created_by': (
                self.BASE_URL + reverse('player-detail', kwargs={'pk': '1'})
            ),
        }
        
        for key, value in response.data.items():
            self.assertEqual(value, target_data[key])
            del(target_data[key])
        
        # After testing all items, there are no remaining target_data items
        self.assertEqual(len(target_data), 0)

    def test_get_invalid_game(self):
        """
        Calling getMatch with an invalid pk returns ???
        """
        url = reverse('game-detail', kwargs={'pk': '9999'})
        response = self.apiclient.get(url)

        self.assertEqual(response.status_code, 404)
    
    def test_create_game(self):
        """
        Sending a POST request with required fields filled out to the
        `create-game` endpoint creates a new Game in the database.
        """
        MATCH_URL = self.BASE_URL + reverse('match-detail', kwargs={'pk': '2'})
        WINNER_URL = self.BASE_URL + reverse('player-detail', kwargs={'pk': '1'})
        LOSER_URL = self.BASE_URL + reverse('player-detail', kwargs={'pk': '2'})
        POINTS = 50

        MOCKED_DATETIME = datetime(2000, 1, 1, tzinfo=pytz.timezone('UTC'))

        data = {
            'match': MATCH_URL,
            'winner': WINNER_URL,
            'loser': LOSER_URL,
            'points': POINTS,
        }

        url = reverse('create-game')

        with mock.patch(
            'django.utils.timezone.now',
            mock.Mock(return_value=MOCKED_DATETIME)
        ):
            self.apiclient.post(url, data=data)

        try:
            Game.objects.get(datetime_played=MOCKED_DATETIME)
        except Game.DoesNotExist:
            assert False, 'Game object not created.'
    
    def test_update_game(self):
        """
        Sending a PATCH request to the game_detail URL endpoint for game 1
        with data update {'points': 1000} updates game 1's points to 1000.
        """
        url = reverse('game-detail', kwargs={'pk': '1'})
        update_data = {'points': 1000}
        
        response = self.apiclient.patch(url, data=update_data)
        
        # Test response data against target data
        self.assertEqual(response.data['points'], 1000)
    
    def test_delete_game(self):
        """
        Sending a DELETE request to the game_detail URL endpoint for match 1
        deletes game 1. (Note: this test does not evaluate deletion's impact
        on the associated signals Outcome and Score; it simply evaluates
        whether the delete call deletes the record.)
        """
        url = reverse('game-detail', kwargs={'pk': '1'})
        
        response = self.apiclient.delete(url)
        
        self.assertEqual(response.status_code, 204)

        # Making a GET call to the resource returns a 404 error
        self.assertEqual(self.apiclient.get(url).status_code, 404)

    def test_suffix_patterns(self):
        """
        Making a request to the all-games endpoint with a URL
        ending in .json returns a JSON object. Doing the same
        with a URL ending in HTML returns an HTML object.
        """
        url_json = reverse('all-games') + '.json'
        url_browsable_api = reverse('all-games') + '.api'
        
        response_json = self.apiclient.get(url_json)
        response_browsable_api = self.apiclient.get(url_browsable_api)

        self.assertEqual(response_json.accepted_media_type, 'application/json')
        self.assertEqual(response_browsable_api.accepted_media_type,
            'text/html')

class TestPlayerViews(TestCase):

    fixtures = ['accounts', 'base']

    @classmethod
    def setUpClass(cls):
        """
        Authenticate player1.
        """
        super().setUpClass()
        
        player = Player.objects.get(pk=1)
        
        cls.apiclient = APIClient()
        cls.apiclient.force_authenticate(user=player)

    def test_all_players_view(self):
        """
        Sending a GET request to the `all_players` endpoint returns
        a list of all players.
        """
        url = reverse('all-players')
        response = self.apiclient.get(url)

        # Sort response Players & database Players
        sorted_response_pks = sorted(
            [player['username'] for player in response.data['results']]
        )
        sorted_database_pks = sorted(
            [player.username for player in Player.objects.all()]
        )

        # Compare the two
        self.assertEqual(sorted_response_pks, sorted_database_pks)

    def test_player_detail_view(self):
        """
        Sending a GET request for a specific Player returns that Player.
        """
        url = reverse('player-detail', kwargs={'pk': '1'})
        response = self.apiclient.get(url)

        self.assertEqual(response.data['username'], 'player1')

class TestRootView(TestCase):

    fixtures = ['accounts']

    @classmethod
    def setUpClass(cls):
        """
        Authenticate player1.
        """
        super().setUpClass()
        
        player = Player.objects.get(pk=1)
        
        cls.apiclient = APIClient()
        cls.apiclient.force_authenticate(user=player)
    
    def test_api_root_status(self):
        """
        Sending a GET request to the `api_root` endpoint returns a status
        code 200.
        """
        url = reverse('api-root')
        response = self.apiclient.get(url)

        self.assertEqual(response.status_code, 200)
    
    def test_api_root_keys(self):
        """
        The `api_root` endpoint returns a dictionary in the `data` attribute
        with keys ['matches', 'games', 'players']
        """
        url = reverse('api-root')
        response = self.apiclient.get(url)

        response_keys = [key for key in response.data.keys()]
        response_keys = sorted(response_keys)

        target_keys = [
            'games',
            'matches',
            'players',
        ]

        self.assertEqual(response_keys, target_keys)