# Robber Baron

> Bots for [Puzzle Baron](https://www.puzzlebaron.com/) games.

## Disclaimer

These bots probably violate Puzzle Baron's Site Terms & Rules. Use at your own risk!

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

# E.g. run the Campsites bot after logging in
PB_USERNAME=username PB_PASSWORD=password poetry run python robber_baron/campsites.py --login
```

## Available bots

| Game | Solution method | In-game performance (configuration) |
|------|-----------------|-------------------------------------|
| [Campsites](https://campsites.puzzlebaron.com/) | Solve with MiniZinc, then encode and submit solution | 5-10s (Extra Large, Challenging) |
| [Numbergrids](https://numbergrids.puzzlebaron.com/) | Solve with MiniZinc, then encode and submit solution | 10-20s (25x25, Fiendish) |
| [Sudoku](https://sudoku.puzzlebaron.com/) | Solve with MiniZinc, then fill grid manually | 5s (Insane) |
| [Word Search](https://wordsearch.puzzlebaron.com/) | Intercept board data request, then encode and submit solution | Instantaneous due to time manipulation |
| [WordTwist](https://wordtwist.puzzlebaron.com/) | Request board data from server, then encode and submit solution | Time not measured |

## Missing bots

| Game | Reason |
|------|--------|
| [Acrostics](https://acrostics.puzzlebaron.com/) | Not viable |
| [Balance Quest](https://balancequest.puzzlebaron.com/) | Difficult to model |
| [Calcudoku](https://calcudoku.puzzlebaron.com/) | TODO (MiniZinc?) |
| [Circuits](https://circuits.puzzlebaron.com/) | Difficult to model |
| [Clueless Crosswords](https://clueless.puzzlebaron.com/) | Not viable |
| [Crosswords](https://crosswords.puzzlebaron.com/) | Not viable |
| [Cryptograms](https://cryptograms.puzzlebaron.com/) | TODO (frequency analysis?) |
| [Drop Quotes](https://dropquotes.puzzlebaron.com/) | Not viable |
| [Fillomino](https://fillomino.puzzlebaron.com/) | Difficult to model |
| [Hangman](https://hangman.puzzlebaron.com/) | Out of scope |
| [Jigsaw Puzzles](https://jigsaw.puzzlebaron.com/) | TODO (reverse engineer?) |
| [Lasergrids](https://lasergrids.puzzlebaron.com/) | Difficult to model |
| [Logic Puzzles](https://logic.puzzlebaron.com/) | Not viable |
| [Patchwords](https://patchwords.puzzlebaron.com/) | Not viable |
| [Numberlinks](https://numberlinks.puzzlebaron.com/) | Difficult to model |
| [Printable Puzzles](https://www.printable-puzzles.com/) | Out of scope |
| [Puzzle Baron Games](https://games.puzzlebaron.com/) | Out of scope |
| [Reverse Word Search](https://rws.puzzlebaron.com/) | TODO (MiniZinc?) |
| [Trivia Challenge](https://trivia.puzzlebaron.com/) | Not viable |
| [Word Puzzles](https://www.word-puzzles.org/) | Out of scope |

## License

MIT
