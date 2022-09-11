from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from accounts.models import Player
from base.models import Game, Match
from tests.fixtures import *


def test_current_matches_table_contains_incomplete_matches(
        player0, incomplete_match_with_one_game, driver, live_server, wait):
    url = live_server.url + reverse('frontend:match-list', kwargs={'username': 'player0'})
    driver.get(url)

    match_pk = incomplete_match_with_one_game.pk
    xpath = ('//table[@id="current-matches-table"]/tbody/'
             f'tr[@id="row-match-{match_pk}"]')
    match_row = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    assert match_row

def test_past_matches_table_contains_finished_complete_matches(
        player0, complete_match_with_one_game, driver, live_server, wait):
    url = live_server.url + reverse('frontend:match-list', kwargs={'username': 'player0'})
    driver.get(url)

    match_pk = complete_match_with_one_game.pk
    xpath = ('//table[@id="past-matches-table"]/tbody/'
             f'tr[@id="row-match-{match_pk}"]')
    match_row = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

    assert match_row
