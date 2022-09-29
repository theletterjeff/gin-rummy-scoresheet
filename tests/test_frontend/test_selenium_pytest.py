from time import sleep

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

def test_add_game_multiple_times_correctly_calculates_score(
        driver, wait, simple_match, live_server, transactional_db):
    """Adding multiple games through the `new-game-form` element adds up 
    their cumulative scores and adds it to the scoreboard.
    """
    url = live_server.url + reverse('frontend:match-detail',
                                    kwargs={'match_pk': simple_match.pk})
    driver.get(url)
    create_games_with_new_game_form(10, wait)

    scoreboard_points = driver.find_elements(By.CLASS_NAME, 'scoreboard-points')
    scoreboard_wins_losses = driver.find_elements(By.CLASS_NAME, 'scoreboard-wins-losses')
    
    assert any([points.text == f'55/{simple_match.target_score}'
                for points in scoreboard_points])
    assert any([points.text == f'0/{simple_match.target_score}'
                for points in scoreboard_points])

    assert any([wins_losses.text == '(10 Wins, 0 Losses)' for wins_losses in scoreboard_wins_losses])
    assert any([wins_losses.text == '(0 Wins, 10 Losses)' for wins_losses in scoreboard_wins_losses])


def test_game_creation_with_gin_and_undercut(
        driver, wait, simple_match, live_server, transactional_db):
    """Creating games with gin/undercut selected creates the correct number of 
    games and adds the correct points to the scoreboard.
    """
    url = live_server.url + reverse('frontend:match-detail',
                                    kwargs={'match_pk': simple_match.pk})
    driver.get(url)

    points_input = driver.find_element(By.ID, 'points-input')
    submit_btn = driver.find_element(By.ID, 'new-game-submit')
    gin_input = driver.find_element(By.ID, 'gin-input')
    undercut_input = driver.find_element(By.ID, 'undercut-input')
    player0_username_option = driver.find_element(By.ID, 'player0-username-option')
    player1_username_option = driver.find_element(By.ID, 'player1-username-option')
    scoreboard_points = driver.find_elements(By.CLASS_NAME, 'scoreboard-points')
    scoreboard_wins_losses = driver.find_elements(By.CLASS_NAME, 'scoreboard-wins-losses')

    points_input.send_keys('7')
    gin_input.click()
    undercut_input.click()
    submit_btn.click()

    points_input.send_keys('5')
    undercut_input.click()
    submit_btn.click()

    game_rows = driver.find_elements(By.CLASS_NAME, 'game-row')
    assert len(game_rows) == 2
    assert len(Game.objects.all()) == 2

    assert any([points.text == f'12/{simple_match.target_score}'
                for points in scoreboard_points])
    assert any([points.text == f'0/{simple_match.target_score}'
                for points in scoreboard_points])

    assert any([wins_losses.text == '(2 Wins, 0 Losses)' for wins_losses in scoreboard_wins_losses])
    assert any([wins_losses.text == '(0 Wins, 2 Losses)' for wins_losses in scoreboard_wins_losses])

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
    
    assert all([points.text == f'0/{incomplete_match_with_ten_games.target_score}'
                for points in scoreboard_points])
    assert all([wins_losses.text == '(0 Wins, 0 Losses)'
                for wins_losses in scoreboard_wins_losses])

def test_add_then_delete_then_add_match_creates_one_match(
        player0, player1, driver, wait, live_server, transactional_db):
    """Adding then deleting then adding a match results in one match in the 
    match list.
    """
    url = live_server.url + reverse('frontend:match-list',
                                    kwargs={'username': 'player0'})
    driver.get(url)
    driver.find_elements(By.CLASS_NAME, 'opponent-option')[0].click()
    driver.find_element(By.ID, 'new-match-submit').click()

    # Reload match-list page after match-detail page loads
    wait.until(EC.presence_of_element_located(
        (By.ID, 'player0-username-option')))
    driver.get(url)
    
    delete_btn = driver.find_elements(By.CLASS_NAME, 'delete-match')[0]
    delete_btn.click()
    wait.until(EC.staleness_of(delete_btn))

    driver.find_elements(By.CLASS_NAME, 'opponent-option')[0].click()
    driver.find_element(By.ID, 'new-match-submit').click()

    # Reload match-list page
    driver.get(url)

    match_rows = driver.find_elements(By.CLASS_NAME, 'row-current-match')
    assert len(match_rows) == 1

def test_add_then_delete_then_add_game_creates_one_game(
        player0, player1, simple_match, driver, wait,
        live_server, transactional_db):
    """Adding then deleting then adding a game results in one game in the 
    game list. (Manual testing resulted in multiple matches.)
    """
    url = live_server.url + reverse('frontend:match-detail',
                                    kwargs={'match_pk': simple_match.pk})
    driver.get(url)
    wait.until(EC.presence_of_element_located(
        (By.ID, 'player0-username-option')))
    
    submit_btn = driver.find_element(By.ID, 'new-game-submit')
    points_input = driver.find_element(By.ID, 'points-input')

    points_input.send_keys('5')
    submit_btn.click()
    
    game_rows = driver.find_elements(By.CLASS_NAME, 'game-row')
    assert len(game_rows) == 1

    delete_btn = driver.find_elements(By.CLASS_NAME, 'delete')[0]
    delete_btn.click()
    wait.until(EC.staleness_of(delete_btn))

    points_input.send_keys('5')
    submit_btn.click()

    game_rows = driver.find_elements(By.CLASS_NAME, 'game-row')
    assert len(game_rows) == 1


def test_edit_game_correctly_changes_score(
        driver, wait, incomplete_match_with_ten_games,
        live_server, transactional_db, player0, player1):
    """Editing a game's points on the game-edit page correctly changes the 
    total points on the match scoreboard and in the game's row in the game list.
    """
    driver.implicitly_wait(1)
    match = incomplete_match_with_ten_games
    game = match.games.all()[0]
    url = live_server.url + reverse('frontend:game-edit',
                                    kwargs={
                                        'match_pk': match.pk,
                                        'game_pk': game.pk,
                                    })
    driver.get(url)
    points_input = wait.until(EC.presence_of_element_located(
        (By.ID, 'points-input')))
    submit_btn = wait.until(EC.presence_of_element_located(
        (By.ID, 'new-game-submit')))
    
    sleep(0.1)
    points_input.clear()
    points_input.send_keys('100')
    submit_btn.click()

    xpath = (f'//tr[@id="game-row-{game.pk}"]/td[3]')
    game_points = wait.until(EC.presence_of_element_located(
        (By.XPATH, xpath)))
    assert game_points.text == '100'

    scoreboard_points = wait.until(EC.presence_of_all_elements_located(
        (By.CLASS_NAME, 'scoreboard-points')))
    target_score = incomplete_match_with_ten_games.target_score
    assert any([points.text == f'120/{target_score}'
                for points in scoreboard_points])

def test_match_list_page_for_invalid_player_returns_404_page(
        player0, live_server, driver):
    """Navigating to the match-list page with the URL kwarg `username` set 
    to an invalid value returns a 404 error.
    """
    url = live_server.url + reverse('frontend:match-list',
                                    kwargs={'username': 'invalid_player'})
    driver.get(url)
    assert driver.title == 'Not Found'

def test_player_usernames_on_player_list_page_and_link_correctly(
        player0, player1, live_server, driver):
    """Players' usernames in the player-list-all page are the correct usernames 
    and link to each player's detail page.
    """
    url = live_server.url + reverse('frontend:player-list-all')
    driver.get(url)

    for player in [player0, player1]:
        xpath = f'//td[@id="player-username-{player.username}"]/a'
        assert player.username == driver.find_element(
            By.XPATH, xpath).get_attribute('text')
        target_url = player.get_absolute_url().replace('api/', '')
        assert target_url in driver.find_element(
            By.XPATH, xpath).get_attribute('href')
