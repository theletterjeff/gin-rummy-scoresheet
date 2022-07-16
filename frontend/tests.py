from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from accounts.models import Player
from base.models import Match

class TestSetUpTearDown(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """Create driver"""
        super().setUpClass()

        options = Options()
        options.headless = True

        cls.driver = WebDriver(options=options)
    
    @classmethod
    def tearDownClass(cls) -> None:
        """Close driver"""
        cls.driver.quit()
        super().tearDownClass()
    
    def setUp(self):
        """Create and log in user (aka player)"""
        super(TestSetUpTearDown, self).setUp()

        # Create user (aka player)
        player = Player.objects.create(username='username')
        player.set_password('password')
        player.save()

        # Log in user
        self.assertTrue(self.client.login(
            username='username',
            password='password',
        ))

        # Add cookie to log in the browser
        cookie = self.client.cookies['sessionid']
        self.driver.get(self.live_server_url)
        self.driver.add_cookie(
            {
                'name': 'sessionid',
                'value': cookie.value,
                'secure': False,
                'path': '/',
            }
        )
    
class MatchesTests(TestSetUpTearDown):

    fixtures = ['accounts']

    def setUp(self):
        # Create and log in user
        super().setUp()

        # Load driver for the matches view
        self.driver.get('%s%s' % (self.live_server_url, reverse('matches-all')))

    def test_current_matches_table_empty_before_match_creation(self):
        """Current matches table has no rows prior to the creation of
        a match.
        """
        wait = WebDriverWait(self.driver, 1)
        with self.assertRaises(selenium.common.exceptions.TimeoutException):
            wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'row-current-match')))

    def test_current_matches_table_lists_match_after_match_creation(self):
        """Current matches table has one row for a match after tha match
        is created.
        """
        # Create a new match
        player_self = Player.objects.get(username='username')
        player_opponent = Player.objects.get(username='player1')

        match = Match.objects.create()
        match.players.add(player_self)
        match.players.add(player_opponent)
        match.save()
        
        self.driver.refresh()
        
        # Wait until table rows are present
        wait = WebDriverWait(self.driver, 1)
        table_rows = wait.until(EC.presence_of_all_elements_located(
            (By.CLASS_NAME, 'row-current-match')))

        self.assertEqual(len(table_rows), 1)
    
    def test_current_matches_table_delete_button_deletes_match(self):
        """Clicking the delete button next to a match deletes that match."""
        # Create a new match
        player_self = Player.objects.get(username='username')
        player_opponent = Player.objects.get(username='player1')

        match = Match.objects.create(created_by=player_self)
        match.players.add(player_self)
        match.players.add(player_opponent)
        match.save()
        
        self.driver.refresh()

        # Wait until delete button is present
        wait = WebDriverWait(self.driver, 3)
        delete_button = wait.until(EC.presence_of_element_located(
            (By.ID, f'delete-match-{match.pk}')
        ))

        # Test if row disappears when delete button is clicked
        delete_button.click()

        self.assertTrue(
            wait.until_not(EC.presence_of_element_located(
                (By.ID, f'delete-match-{match.pk}')
            ))
        )
        
        # Make sure that the match doesn't appear after re-pinging API
        self.driver.refresh()
        with self.assertRaises(selenium.common.exceptions.TimeoutException):
            wait.until(EC.presence_of_element_located(
                (By.ID, f'delete-match-{match.pk}')
            ))