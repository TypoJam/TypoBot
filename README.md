# TypoBot

Discord bot for the TypoJam Discord server.

# Quick Start

Not sure if this works on your machine, just made it work for hosting and development.

```shell
$ . scripts/venv.sh
$ micro config.py # Set up config to your heart's desire
$ python3 TypoJam.py
```

# Contributing

Contributing is always appreciated! Feel free to create a pull request.

Before you do, make sure you checked your code with `mypy` (Included in `requirements.txt`).

If you're on Linux (or any other environment that has bash) you can create a symlink so it checks your code before you commit:
```sh
$ ln -s $PWD/scripts/pre-commit.sh .git/hooks/pre-commit
```
