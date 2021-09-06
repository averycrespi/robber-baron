# Robber Baron

> Bots for [Puzzle Baron](https://www.puzzlebaron.com/) games.

## Disclaimer

These bots probably violates Puzzle Baron's Site Terms & Rules. Use at your own risk!

## Requirements

- [Poetry](https://python-poetry.org/) dependency manager
- [Google Chrome](https://www.google.com/chrome/) with [chromedriver](https://chromedriver.chromium.org/) in your `PATH`
- [MiniZinc](https://www.minizinc.org/) constraint modeler

## Getting started

```sh
git clone https://github.com/averycrespi/robber-baron.git
cd robber-baron
poetry install

# E.g. run the WordTwist bot
poetry run python robber_baron/wordtwist.py
```

## Available bots

| Game      | Solution method |
|-----------|-----------------|
| [Campsites](https://campsites.puzzlebaron.com/) | Solve with MiniZinc, then encode and submit solution |
| [Sudoku](https://sudoku.puzzlebaron.com/) | Solve with MiniZinc, then fill grid manually |
| [WordTwist](https://wordtwist.puzzlebaron.com/) | Request board data from server, then submit words manually |

## License

MIT
