from argparse import ArgumentParser
from collections import namedtuple
import hashlib
from minizinc import Instance, Model, Solver
from more_itertools import sliced
from pathlib import Path
import re
from selenium import webdriver
from selenium.webdriver.support.select import Select
from typing import Sequence

from robber_baron import find_element


PuzzleSize = namedtuple("PuzzleSize", ("num_rows", "num_cols", "value"))
PUZZLE_SIZES = {
    "extra_small": PuzzleSize(num_rows=5, num_cols=10, value=1),
    "small": PuzzleSize(num_rows=10, num_cols=10, value=2),
    "medium": PuzzleSize(num_rows=10, num_cols=15, value=3),
    "medium_large": PuzzleSize(num_rows=15, num_cols=15, value=4),
    "large": PuzzleSize(num_rows=15, num_cols=20, value=5),
    "extra_large": PuzzleSize(num_rows=20, num_cols=20, value=6),
}

PuzzleDifficulty = namedtuple("PuzzleDifficulty", ("value",))
PUZZLE_DIFFICULTIES = {
    "easy": PuzzleDifficulty(value=1),
    "challenging": PuzzleDifficulty(value=3),
}


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play Campsites")
    parser.add_argument(
        "-s",
        "--puzzle-size",
        type=str,
        default="extra_small",
        choices=list(PUZZLE_SIZES.keys()),
        help="Puzzle size; default 'extra_small'",
    )
    parser.add_argument(
        "-d",
        "--puzzle-difficulty",
        type=str,
        default="easy",
        choices=list(PUZZLE_DIFFICULTIES.keys()),
        help="Puzzle difficulty; default 'easy'",
    )
    parser.add_argument(
        "--no-verify", action="store_true", help="Skip MD5 verification"
    )
    return parser.parse_args()


def solve_instance(
    *,
    num_rows: int,
    num_cols: int,
    num_tents_in_row: Sequence[int],
    num_tents_in_col: Sequence[int],
    num_trees: int,
    tree_rows: Sequence[int],
    tree_cols: Sequence[int],
):
    """Solve a Campsites instance using MiniZinc."""
    model_file = Path(__file__).parent / "models" / "campsites.mzn"
    model = Model(model_file)
    solver = Solver.lookup("gecode")

    instance = Instance(solver, model)
    instance["num_rows"] = num_rows
    instance["num_cols"] = num_cols
    instance["num_tents_in_row"] = num_tents_in_row
    instance["num_tents_in_col"] = num_tents_in_col
    instance["num_trees"] = num_trees
    instance["tree_rows"] = tree_rows
    instance["tree_cols"] = tree_cols

    return instance.solve()


if __name__ == "__main__":
    args = parse_args()
    size = PUZZLE_SIZES[args.puzzle_size]
    difficulty = PUZZLE_DIFFICULTIES[args.puzzle_difficulty]
    driver = webdriver.Chrome()

    new_game_url = "https://campsites.puzzlebaron.com/init.php"
    print(f"Loading new game URL: {new_game_url} ...")
    driver.get(new_game_url)

    print("Setting puzzle size and difficulty ...")
    Select(find_element(driver, 'select[name="sg"]')).select_by_value(str(size.value))
    Select(find_element(driver, 'select[name="sd"]')).select_by_value(
        str(difficulty.value)
    )

    print("Starting game ...")
    find_element(driver, 'input[name="CreatePuzzle"]').click()
    find_element(driver, 'input[name="submit"]').click()

    # We can't use find_element because the element is invisible
    initial_state = driver.find_element_by_css_selector(
        "div#savedgridstates"
    ).get_attribute("innerText")
    print(f"Extracted initial game state: {initial_state}")

    tree_rows = []
    tree_cols = []
    for i, row in enumerate(sliced(initial_state, size.num_cols)):
        for j, cell in enumerate(row):
            if cell == "T":
                # MiniZinc uses 1-based indexing
                tree_rows.append(i + 1)
                tree_cols.append(j + 1)
    print(f"Parsed state into tree rows: {tree_rows} and tree columns: {tree_cols}")

    num_tents_in_row = [
        int(find_element(driver, f"td#nr{i}").get_attribute("innerText"))
        for i in range(size.num_rows)
    ]
    print(f"Extracted number of tents in each row: {num_tents_in_row}")

    num_tents_in_col = [
        int(find_element(driver, f"td#nb{j}").get_attribute("innerText"))
        for j in range(size.num_cols)
    ]
    print(f"Extracted number of tents in each column: {num_tents_in_col}")

    print("Solving instance with MiniZinc ...")
    result = solve_instance(
        num_rows=size.num_rows,
        num_cols=size.num_cols,
        num_tents_in_row=num_tents_in_row,
        num_tents_in_col=num_tents_in_col,
        num_trees=initial_state.count("T"),
        tree_rows=tree_rows,
        tree_cols=tree_cols,
    )

    final_state = []
    for i in range(size.num_rows):
        for j in range(size.num_cols):
            if result["trees"][i][j]:
                final_state.append("T")
            elif result["tents"][i][j]:
                final_state.append("C")
            else:
                final_state.append(".")
    solution = "".join(final_state)
    print(f"Formatted solution: {solution}")

    if not args.no_verify:
        print("Verifying solution ...")
        pattern = r"if\(MD5\(cgs2\)=='([a-z0-9]{32})'\)"
        expected_digest = re.search(pattern, driver.page_source).group(1)  # type: ignore
        actual_digest = hashlib.md5(  # nosec
            solution.replace(".", "_").encode("utf-8")
        ).hexdigest()
        if expected_digest != actual_digest:
            raise ValueError(
                f"Expected MD5 digest to be {expected_digest}, but got {actual_digest}"
            )

    print("Submitting game ...")
    # We need to execute JavaScript because Selenium doesn't support setting attributes
    driver.execute_script(
        "document.getElementById('ans').setAttribute('value', arguments[0])", solution
    )
    find_element(driver, "form#gameform").submit()

    input("Press enter to quit: ")
    driver.quit()
