#! /usr/bin/env bash

VENV_DIR=".venv"
PYTHON="/usr/bin/env python3"
REQUIREMENTS="requirements.txt"

function activate {
    source $VENV_DIR/bin/activate
}

if [[ ! -d "$VENV_DIR" ]] then
    $PYTHON -m venv "$VENV_DIR"
    activate
    pip install -r "$REQUIREMENTS"

    echo "DISCORD_TOKEN = \"token here\"" > config.py
else
    activate
fi
