from argparse import ArgumentParser
from enum import Enum
from more_itertools import sliced
from pathlib import Path

from robber_baron import Bot


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    DIFFICULT = "difficult"
    INSANE = "insane"

    def __str__(self) -> str:
        return self.value


DIFFICULTY_TO_ID = {
    Difficulty.EASY: "e",
    Difficulty.MEDIUM: "m",
    Difficulty.DIFFICULT: "d",
    Difficulty.INSANE: "i",
}


class SudokuBot(Bot):
    def play(self, difficulty: Difficulty):
        """Play a Sudoku game."""
        difficulty_id = DIFFICULTY_TO_ID[difficulty]
        new_game_url = f"https://sudoku.puzzlebaron.com/init.php?d={difficulty_id}"
        print(f"Loading new game URL: {new_game_url} ...")
        self.browser.get(new_game_url)

        print("Starting game ...")
        self.browser.find_element("td > a.button_orange").click()

        boxes = [
            self.browser.find_element(f"div#box{i+1}").get_attribute("innerText")
            for i in range(81)
        ]
        initial_state = list(sliced([int(b) if len(b) > 0 else 0 for b in boxes], 9))
        print(f"Extracted initial game state: {initial_state}")

        print("Solving instance with MiniZinc ...")
        model_file = Path(__file__).parent / "models" / "sudoku.mzn"
        result = self.solver.solve(model_file, {"start": initial_state})
        solution = result["puzzle"]
        print(f"Found solution: {solution}")

        # TODO: reverse engineer encoding logic instead of filling in grid manually
        print("Filling in grid ...")
        for j in range(9):
            for i in range(9):
                if initial_state[j][i] == 0:
                    self.browser.execute_script(
                        "document.getElementById('box' + arguments[0]).innerText = arguments[1]",
                        str((j * 9) + i + 1),
                        solution[j][i],
                    )

        print("Submitting game ...")
        self.browser.execute_script("window.xmlhttpPost2('check.php')")


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play a Sudoku game")
    parser.add_argument(
        "-d",
        "--difficulty",
        type=Difficulty,
        default=Difficulty.EASY,
        choices=list(Difficulty),
        help="Puzzle difficulty; default 'easy'",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bot = SudokuBot()
    bot.play(args.difficulty)

    input("Press enter to quit: ")
    bot.browser.quit()
