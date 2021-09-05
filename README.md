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
|-----------|------------------|
| [Campsites](https://campsites.puzzlebaron.com/) | Model with MiniZinc and verify with MD5 digest |
| [Campsites](https://sudoku.puzzlebaron.com/) | Model with MiniZinc |
| [WordTwist](https://wordtwist.puzzlebaron.com/) | Request board data from server |

## License

MIT
