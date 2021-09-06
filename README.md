# Robber Baron

> Bots for [Puzzle Baron](https://www.puzzlebaron.com/) games.

## Disclaimer

These bots probably violates Puzzle Baron's Site Terms & Rules. Use at your own risk!

## Requirements

- [Poetry](https://python-poetry.org/)
- [Google Chrome](https://www.google.com/chrome/) with [chromedriver](https://chromedriver.chromium.org/) in your `PATH`
- [MiniZinc](https://www.minizinc.org/)
- [OpenSSL](https://www.openssl.org/) for bots that intercept requests

## Getting started

```sh
git clone https://github.com/averycrespi/robber-baron.git
cd robber-baron
poetry install

# E.g. run the WordTwist bot
poetry run python robber_baron/wordtwist.py
```

## Available bots

| Game      | Solution method | In-game performance (configuration) |
|-----------|-----------------|-------------------------------------|
| [Campsites](https://campsites.puzzlebaron.com/) | Solve with MiniZinc, then encode and submit solution | 5-10s (Extra Large, Challenging) |
| [Sudoku](https://sudoku.puzzlebaron.com/) | Solve with MiniZinc, then fill grid manually | 5s (Insane) |
| [Word Search](https://wordsearch.puzzlebaron.com/) | Intercept board data request, then encode and submit solution | Instantaneous due to time manipulation |
| [WordTwist](https://wordtwist.puzzlebaron.com/) | Request board data from server, then encode and submit solution | Time not measured |

## License

MIT
