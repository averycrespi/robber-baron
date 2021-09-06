from argparse import ArgumentParser
import brotli
import re
from seleniumwire import webdriver

from robber_baron import Bot, Browser


class WordSearchBot(Bot):
    def play(self):
        """Play a Word Search game."""
        new_game_url = "https://wordsearch.puzzlebaron.com/init.php"
        print(f"Loading new game URL: {new_game_url} ...")
        self.browser.get(new_game_url)

        time_allotted = self.browser.find_element(
            "table.tinytext > tbody > tr:nth-child(2) > td:nth-child(2)"
        ).get_attribute("innerText")
        minutes = re.search(r"(\d+) minute", time_allotted).group(1)
        seconds = re.search(r"(\d+) second", time_allotted).group(1)
        timestamp = f"{minutes.zfill(2)}:{seconds.zfill(2)}"
        print(f"Extracted timestamp: {timestamp}")

        print("Loading board URL ...")
        self.browser.find_element('input[name="submit"]').click()

        # Word Searches prevents you from loading the same board data URL twice,
        # so we need to intercept and parse the original request
        print("Extracting board data from request history ...")
        _ = self.browser.find_element("a#start")
        prefix = "https://wordsearch.puzzlebaron.com/boarddata2.php?uid="
        board_data = None
        for request in self.browser.request_history():
            if request.url.startswith(prefix):
                board_data = brotli.decompress(request.response.body).decode("utf-8")
                break
        else:
            raise ValueError("failed to find board data request")
        print(f"Parsed board data: {board_data}")

        words = re.search(r"wordList=(.*?)&", board_data).group(1).split(",")
        solution = ",".join(f"{timestamp}={word}" for word in words)
        print(f"Encoded solution: {solution}")

        print("Starting game ...")
        self.browser.find_element("a#start").click()

        print("Submitting game ...")
        self.browser.execute_script(
            "document.getElementById('form_timer').value = arguments[0]", timestamp
        )
        # "SHOTGUN" means competitive, "UNLIMITED" means casual
        self.browser.execute_script(
            "document.getElementById('form_type').value = arguments[0]", "SHOTGUN"
        )
        self.browser.execute_script(
            "document.getElementById('form_words').value = arguments[0]", solution
        )
        self.browser.execute_script(
            "document.getElementById('form_hints').value = arguments[0]", "0"
        )
        self.browser.find_element("form#gameover").submit()


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play a Word Search game")
    return parser.parse_args()


if __name__ == "__main__":
    _ = parse_args()
    bot = WordSearchBot(browser=Browser(webdriver.Chrome))
    bot.play()

    input("Press enter to quit: ")
    bot.browser.quit()
