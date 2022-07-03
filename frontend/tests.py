from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.firefox.options import Options

from accounts.models import Player

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

    def setUp(self):
        # Create and log in user
        super(TestSetUpTearDown, self).setUp()

        # Load driver for the matches view
        self.driver.get('%s%s' % (self.live_server_url, reverse('matches-all')))

    def test_current_matches_table_empty_before_match_creation(self):
        """Current matches table has no rows prior to the creation of
        a match.
        """
        table_body = self.driver.find_element(By.ID, 'current-matches-body')
        table_rows = table_body.find_elements(By.XPATH, './child::*')
        self.assertEqual(len(table_rows), 0)