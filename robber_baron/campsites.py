from argparse import ArgumentParser
from enum import Enum
from more_itertools import sliced
from pathlib import Path

from robber_baron import Bot


class Size(Enum):
    EXTRA_SMALL = "extra_small"
    SMALL = "small"
    MEDIUM = "medium"
    MEDIUM_LARGE = "medium_large"
    LARGE = "large"
    EXTRA_LARGE = "extra_large"

    def __str__(self) -> str:
        return self.value


class Difficulty(Enum):
    EASY = "easy"
    CHALLENGING = "challenging"

    def __str__(self) -> str:
        return self.value


# Map size to (num_rows, num_cols, id)
SIZE_DATA = {
    Size.EXTRA_SMALL: (5, 10, 1),
    Size.SMALL: (10, 10, 2),
    Size.MEDIUM: (10, 15, 3),
    Size.MEDIUM_LARGE: (15, 15, 4),
    Size.LARGE: (15, 20, 5),
    Size.EXTRA_LARGE: (20, 20, 6),
}

DIFFICULTY_IDS = {Difficulty.EASY: 1, Difficulty.CHALLENGING: 3}


class CampsitesBot(Bot):
    def play(self, size: Size, difficulty: Difficulty):
        """Play a Campsites game."""
        num_rows, num_cols, size_id = SIZE_DATA[size]
        difficulty_id = DIFFICULTY_IDS[difficulty]

        new_game_url = "https://campsites.puzzlebaron.com/init.php"
        print(f"Loading new game URL: {new_game_url} ...")
        self.browser.get(new_game_url)

        print(f"Setting puzzle size to: {str(size)} ...")
        self.browser.select_by_value(
            self.browser.find_element('select[name="sg"]'), str(size_id)
        )

        print(f"Setting puzzle difficulty to: {str(difficulty)} ...")
        self.browser.select_by_value(
            self.browser.find_element('select[name="sd"]'),
            str(difficulty_id),
        )

        print("Starting game ...")
        self.browser.find_element('input[name="CreatePuzzle"]').click()
        self.browser.find_element('input[name="submit"]').click()

        initial_state = self.browser.find_invisible_element(
            "div#savedgridstates"
        ).get_attribute("innerText")
        print(f"Extracted initial game state: {initial_state}")

        tree_rows = []
        tree_cols = []
        for i, row in enumerate(sliced(initial_state, num_cols)):
            for j, cell in enumerate(row):
                if cell == "T":
                    # MiniZinc uses 1-based indexing
                    tree_rows.append(i + 1)
                    tree_cols.append(j + 1)
        print(f"Parsed state into tree rows: {tree_rows} and tree columns: {tree_cols}")

        num_tents_in_row = [
            int(self.browser.find_element(f"td#nr{i}").get_attribute("innerText"))
            for i in range(num_rows)
        ]
        print(f"Extracted number of tents in each row: {num_tents_in_row}")

        num_tents_in_col = [
            int(self.browser.find_element(f"td#nb{j}").get_attribute("innerText"))
            for j in range(num_cols)
        ]
        print(f"Extracted number of tents in each column: {num_tents_in_col}")

        print("Solving problem instance ...")
        model_file = Path(__file__).parent / "models" / "campsites.mzn"
        instance_params = {
            "num_rows": num_rows,
            "num_cols": num_cols,
            "num_tents_in_row": num_tents_in_row,
            "num_tents_in_col": num_tents_in_col,
            "num_trees": sum(num_tents_in_row),
            "tree_rows": tree_rows,
            "tree_cols": tree_cols,
        }
        result = self.solver.solve(model_file, instance_params)

        final_state = []
        for i in range(num_rows):
            for j in range(num_cols):
                if result["trees"][i][j]:
                    final_state.append("T")
                elif result["tents"][i][j]:
                    final_state.append("C")
                else:
                    final_state.append(".")
        solution = "".join(final_state)
        print(f"Formatted solution: {solution}")

        print("Submitting game ...")
        self.browser.execute_script(
            "document.getElementById('ans').setAttribute('value', arguments[0])",
            solution,
        )
        self.browser.find_element("form#gameform").submit()

        print("Verifying submission ...")
        congrats = self.browser.find_element("div#container_left > h1.header_font")
        assert congrats.get_attribute("innerText") == "Congratulations!"


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play a Campsites game")
    parser.add_argument(
        "-s",
        "--size",
        type=Size,
        default=Size.EXTRA_SMALL,
        choices=list(Size),
        help="Puzzle size; default 'extra_small'",
    )
    parser.add_argument(
        "-d",
        "--difficulty",
        type=Difficulty,
        default=Difficulty.EASY,
        choices=list(Difficulty),
        help="Puzzle difficulty; default 'easy'",
    )
    parser.add_argument(
        "--login", action="store_true", help="Login to Puzzle Baron account"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    bot = CampsitesBot()
    if args.login:
        bot.login()
    bot.play(args.size, args.difficulty)

    input("Press enter to quit: ")
    bot.browser.quit()
