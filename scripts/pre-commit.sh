#! /usr/bin/env bash

set -eo pipefail

source scripts/venv.sh
mypy -m bot.TypoBot --check-untyped-defs
