import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


BOARD_SIZE = 4  # 4 or 5


def find_element(driver, css_selector: str, timeout_seconds: int = 10):
    """Find an element on the page, waiting for the element to become clickable."""
    return WebDriverWait(driver, timeout_seconds).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
    )


if __name__ == "__main__":
    driver = webdriver.Chrome()

    # Load the Start Game page and extract the board UID.
    driver.get(f"https://wordtwist.puzzlebaron.com/init{BOARD_SIZE}.php")
    board_url = find_element(driver, "div#newgameboard a").get_attribute("href")
    board_uid = board_url.split("u=")[-1]

    # We need to load the board URL _before_ we request the board data,
    # otherwise Wordtwist will complain that the game has already been completed.
    driver.get(board_url)
    data_url = f"https://wordtwist.puzzlebaron.com/boarddata.php?uid={board_uid}"
    board_data = json.loads(requests.get(data_url).text)
    print(json.dumps(board_data, indent=4))

    # Start the game and submit all valid words.
    find_element(driver, "a#start").click()
    words = list(board_data["wordList"].keys())
    word_input = find_element(driver, "input#word")
    for word in words:
        word_input.send_keys(word)
        word_input.send_keys(Keys.RETURN)
        time.sleep(0.1)

    find_element(driver, "a#submit").click()
    find_element(driver, "div.TB_modal > div.alert a.yes").click()

    input("Press enter to quit: ")
    driver.quit()
