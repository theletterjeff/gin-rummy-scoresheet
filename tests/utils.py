import re

from django.middleware.csrf import get_token

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from accounts.models import Player

def get_value_from_url(pattern: re.Pattern, url: str):
    """Given a re.Pattern, return the matched substring from a URL string."""
    matched_strings = pattern.findall(url)
    if len(matched_strings) > 1:
        raise Exception('More than one match returned from URL.')
    return matched_strings[0]

def get_pk_from_match_url(url: str):
    """Get the `pk` kwarg from a Match URL following the URL pattern:
    'match/<str:pk>/'
    """
    pattern = re.compile(r'\d+(?=\/$)')
    return get_value_from_url(pattern, url)

def create_games_with_new_game_form(game_num: int, wait: WebDriverWait) -> None:
    """Fill and create `game_num` new games through the `new-game-form` 
    element.
    """
    for i in range(1, game_num+1):
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

def delete_games_from_match_detail_games_list(driver: WebDriver,
                                              wait: WebDriverWait):
    """Use the 'Delete' button in every game-row to delete all games."""
    while True:
        try:
            delete_btn = wait.until(EC.presence_of_all_elements_located(
                (By.CLASS_NAME, 'delete')))[0]
        except TimeoutException:
            break
        delete_btn_id = delete_btn.get_attribute('id')
        delete_btn.click()
        wait.until_not(EC.presence_of_element_located((By.ID, delete_btn_id)))
