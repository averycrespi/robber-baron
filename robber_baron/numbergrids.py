from argparse import ArgumentParser
from enum import Enum
from pathlib import Path

from robber_baron import Bot, ConstraintSolver


class Size(Enum):
    FIVE_BY_FIVE = "5"
    TEN_BY_TEN = "10"
    FIFTEEN_BY_FIFTEEN = "15"
    TWENTY_BY_TWENTY = "20"
    TWENTY_FIVE_BY_TWENTY_FIVE = "25"

    def __str__(self) -> str:
        return self.value


class Difficulty(Enum):
    VERY_EASY = "very_easy"
    MODERATE = "moderate"
    CHALLENGING = "challenging"
    DIFFICULT = "difficult"
    FIENDISH = "fiendish"

    def __str__(self) -> str:
        return self.value


DIFFICULTY_IDS = {
    Difficulty.VERY_EASY: 1,
    Difficulty.MODERATE: 2,
    Difficulty.CHALLENGING: 3,
    Difficulty.DIFFICULT: 4,
    Difficulty.FIENDISH: 5,
}


class NumbergridsBot(Bot):
    def play(self, size: Size, difficulty: Difficulty):
        """Play a Numbergrids game."""
        grid_size = int(str(size))

        new_game_url = "https://numbergrids.puzzlebaron.com/init.php"
        print(f"Loading new game URL: {new_game_url} ...")
        self.browser.get(new_game_url)

        print(f"Setting puzzle size to: {str(size)} ...")
        print(f"Setting puzzle difficulty to: {str(difficulty)} ...")
        _ = self.browser.find_element('form[action="init2.php"]')
        self.browser.execute_script(
            """
            document.getElementById('sg').value = arguments[0];
            document.getElementById('sd').value = arguments[1];
            """,
            str(size),
            str(DIFFICULTY_IDS[difficulty]),
        )

        print("Starting game ...")
        self.browser.find_element('input[name="CreatePuzzle"]').click()
        self.browser.find_element('input[name="submit"]').click()

        row_clues = []
        for i in range(grid_size):
            cell = self.browser.find_element(f"td#X0Y{i+1}")
            row_clues.append(
                [int(c) for c in cell.get_attribute("innerText").strip().split(",")]
            )
        print(f"Extracted row clues: {row_clues}")

        col_clues = []
        for i in range(grid_size):
            cell = self.browser.find_element(f"td#X{i+1}Y0")
            col_clues.append(
                [int(c) for c in cell.get_attribute("innerText").strip().split("\n")]
            )
        print(f"Extracted column clues: {col_clues}")

        max_clues = max(max(len(c) for c in row_clues), max(len(c) for c in col_clues))
        pad = lambda clues: clues + [0] * (max_clues - len(clues))  # noqa: E731
        padded_row_clues = list(map(pad, row_clues))
        padded_col_clues = list(map(pad, col_clues))

        print("Solving problem instance ...")
        model_file = Path(__file__).parent / "models" / "numbergrid.mzn"
        instance_params = {
            "grid_size": grid_size,
            "num_clues": max_clues,
            "row_clues": padded_row_clues,
            "col_clues": padded_col_clues,
        }
        result = self.solver.solve(model_file, instance_params)

        final_state = []
        for i in range(grid_size):
            for j in range(grid_size):
                if result["grid"][i][j]:
                    final_state.append("O")
                else:
                    final_state.append("_")
        solution = "".join(final_state)
        print(f"Formatted solution: {solution}")

        print("Submitting game ...")
        self.browser.execute_script(
            "document.getElementById('ans').setAttribute('value', arguments[0])",
            solution,
        )
        self.browser.find_element("form#gameform").submit()


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play a Numbergrids game")
    parser.add_argument(
        "-s",
        "--size",
        type=Size,
        default=Size.FIVE_BY_FIVE,
        choices=list(Size),
        help="Puzzle size; default '5'",
    )
    parser.add_argument(
        "-d",
        "--difficulty",
        type=Difficulty,
        default=Difficulty.VERY_EASY,
        choices=list(Difficulty),
        help="Puzzle difficulty; default 'very_easy'",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    # Chuffed has much better performance than Gecode for this problem
    bot = NumbergridsBot(solver=ConstraintSolver("chuffed"))
    bot.play(args.size, args.difficulty)

    input("Press enter to quit: ")
    bot.browser.quit()
