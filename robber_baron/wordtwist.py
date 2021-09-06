from argparse import ArgumentParser
from enum import Enum
import json
import requests
import time

from robber_baron import Bot


class Size(Enum):
    FOUR_BY_FOUR = "4"
    FIVE_BY_FIVE = "5"

    def __str__(self) -> str:
        return self.value


class WordTwistBot(Bot):
    def play(self, size: Size):
        """Play a WordTwist game."""
        new_game_url = f"https://wordtwist.puzzlebaron.com/init{str(size)}.php"
        print(f"Loading new game URL: {new_game_url} ...")
        self.browser.get(new_game_url)
        board_url = self.browser.find_element("div#newgameboard a").get_attribute(
            "href"
        )
        board_uid = board_url.split("u=")[-1]
        print(f"Extracted board UID: {board_uid}")

        # We need load the board URL _before_ requesting the board data,
        # otherwise WordTwist will complain that the game has already been completed
        print(f"Loading board URL: {board_url} ...")
        self.browser.get(board_url)
        data_url = f"https://wordtwist.puzzlebaron.com/boarddata.php?uid={board_uid}"
        print(f"Requesting board data from: {data_url} ...")
        board_data = json.loads(requests.get(data_url).text)
        print(f"Parsed board data: {json.dumps(board_data)}")

        # TODO: reverse engineer encoding logic instead of entering words manually
        print("Starting game and entering words ...")
        self.browser.find_element("a#start").click()
        words = list(board_data["wordList"].keys())
        word_input = self.browser.find_element("input#word")
        for word in words:
            self.browser.send_keys_with_return(word_input, word)
            time.sleep(0.1)

        print("Submitting game ...")
        self.browser.find_element("a#submit").click()
        self.browser.find_element("div.TB_modal > div.alert a.yes").click()


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play a Wordtwist game")
    parser.add_argument(
        "-s",
        "--board-size",
        type=Size,
        default=Size.FOUR_BY_FOUR,
        choices=list(Size),
        help="Board size; default '4'",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bot = WordTwistBot()
    bot.play(args.board_size)

    input("Press enter to quit: ")
    bot.browser.quit()
