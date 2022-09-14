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

def test_edit_buttons_on_match_list_page_redirect(
        driver, player0, incomplete_match_with_one_game,
        complete_match_with_one_game, live_server, wait):
    """The edit button on match rows on the match list page redirects to 
    the detail view for their respective matches.
    """
    url = live_server.url + reverse('frontend:match-list', kwargs={'username': 'player0'})
    driver.get(url)

    for match in [incomplete_match_with_one_game, complete_match_with_one_game]:
        edit_button = wait.until(EC.presence_of_element_located(
            (By.ID, f'edit-match-{match.pk}')))
        edit_button.click()
        wait.until(EC.url_changes(url))

def test_add_game_multiple_times_creates_one_game_per_submit(
        driver, wait, simple_match, live_server, transactional_db):
    """Adding multiple games through the `new-game-form` element creates one 
    Game instance per submission.
    """
    url = live_server.url + reverse('frontend:match-detail',
                                    kwargs={'match_pk': simple_match.pk})
    driver.get(url)

    # Submit 10 games through new-game-form
    for i in range(1, 11):
        points_input = wait.until(EC.presence_of_element_located(
            (By.ID, 'points-input')))
        submit_btn = wait.until(EC.presence_of_element_located(
            (By.ID, 'new-game-submit')))
        player0_username_option = wait.until(EC.presence_of_element_located(
            (By.ID, 'player0-username-option')))
        player1_username_option = wait.until(EC.presence_of_element_located(
            (By.ID, 'player1-username-option')))

        points_input.send_keys(str(i))
        submit_btn.click()

    game_rows = driver.find_elements(By.CLASS_NAME, 'game-row')
    assert len(game_rows) == 10
    assert len(Game.objects.all()) == 10
