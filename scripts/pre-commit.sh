#! /usr/bin/env bash

set -eo pipefail

source scripts/venv.sh
mypy bot/TypoBot.py
