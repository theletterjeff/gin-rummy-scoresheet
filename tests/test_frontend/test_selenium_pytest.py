from django.urls import reverse

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from accounts.models import Player
from base.models import Game, Match
from tests.fixtures import *
from tests.utils import (create_games_with_new_game_form,
                         delete_games_from_match_detail_games_list)

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
    create_games_with_new_game_form(10, wait)

    game_rows = driver.find_elements(By.CLASS_NAME, 'game-row')
    assert len(game_rows) == 10
    assert len(Game.objects.all()) == 10

def test_delete_games_returns_score_to_zero(
        driver, wait, incomplete_match_with_ten_games,
        live_server, transactional_db):
    """Deleting all the games in a match returns the scoreboard for both 
    players to zero.
    """
    url = live_server.url + reverse('frontend:match-detail',
            kwargs={'match_pk': incomplete_match_with_ten_games.pk})
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'delete')))
    assert len(driver.find_elements(By.CLASS_NAME, 'delete')) == 10
    delete_games_from_match_detail_games_list(driver, wait)
    
    scoreboard_points = driver.find_elements(By.CLASS_NAME, 'scoreboard-points')
    scoreboard_wins_losses = driver.find_elements(By.CLASS_NAME, 'scoreboard-wins-losses')
    
    assert all([points.text == '0' for points in scoreboard_points])
    assert all([wins_losses.text == '(0 Wins, 0 Losses)' for wins_losses in scoreboard_wins_losses])
