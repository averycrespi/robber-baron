# Untwist

> A proof-of-concept [WordTwist](https://wordtwist.puzzlebaron.com/) bot.

## Disclaimer

This bot probably violates Puzzle Baron's Site Terms & Rules. Use at your own risk!

## Requirements

- [Poetry](https://python-poetry.org/)
- [Google Chrome](https://www.google.com/chrome/)
- [chromedriver](https://chromedriver.chromium.org/) in your `PATH`

## Getting started

```sh
git clone https://github.com/averycrespi/untwist.git
cd untwist
poetry install
poetry run python play.py
```

## How it works

- When you start a game, the WordTwist client asks their server for a list of valid words
- We can trivially replicate this request in order to retrieve the board data
- However, we need to load the board URL _before_ requesting the data, otherwise Wordtwist will complain that the game has already been completed

## License

MIT
