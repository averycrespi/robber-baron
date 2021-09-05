from argparse import ArgumentParser
from minizinc import Instance, Model, Solver
from more_itertools import sliced
from pathlib import Path
from selenium import webdriver
from typing import Sequence

from robber_baron import find_element

PUZZLE_DIFFICULTIES = {"easy": "e", "medium": "m", "difficult": "d", "insane": "i"}


def parse_args():
    """Parse command-line arguments."""
    parser = ArgumentParser(description="Play Sudoku")
    parser.add_argument(
        "-d",
        "--puzzle-difficulty",
        type=str,
        default="easy",
        choices=list(PUZZLE_DIFFICULTIES.keys()),
        help="Puzzle difficulty; default 'easy'",
    )
    return parser.parse_args()


def solve_instance(start: Sequence[Sequence[int]]):
    """Solve a Sudoku instance using MiniZinc."""
    model_file = Path(__file__).parent / "models" / "sudoku.mzn"
    model = Model(model_file)
    solver = Solver.lookup("gecode")

    instance = Instance(solver, model)
    instance["start"] = start

    return instance.solve()


if __name__ == "__main__":
    args = parse_args()
    difficulty = PUZZLE_DIFFICULTIES[args.puzzle_difficulty]
    driver = webdriver.Chrome()

    new_game_url = f"https://sudoku.puzzlebaron.com/init.php?d={difficulty}"
    print(f"Loading new game URL: {new_game_url} ...")
    driver.get(new_game_url)

    print("Starting game ...")
    find_element(driver, "td > a.button_orange").click()

    boxes = [
        find_element(driver, f"div#box{i+1}").get_attribute("innerText")
        for i in range(81)
    ]
    initial_state = list(sliced([int(b) if len(b) > 0 else 0 for b in boxes], 9))
    print(f"Extracted initial game state: {initial_state}")

    print("Solving instance with MiniZinc ...")
    result = solve_instance(start=initial_state)

    solution = result["puzzle"]
    print(f"Found solution: {solution}")

    print("Filling in grid ...")
    for j in range(9):
        for i in range(9):
            if initial_state[j][i] == 0:
                driver.execute_script(
                    "document.getElementById('box' + arguments[0]).innerText = arguments[1]",
                    str((j * 9) + i + 1),
                    solution[j][i],
                )

    print("Submitting game ...")
    driver.execute_script("window.xmlhttpPost2('check.php')")

    input("Press enter to quit: ")
    driver.quit()
