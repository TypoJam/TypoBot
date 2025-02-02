#! /usr/bin/env bash

VENV_DIR=".venv"
PYTHON="/usr/bin/env python3"
REQUIREMENTS="requirements.txt"
CONFIG_FILE="bot/config.py"

function activate {
    source $VENV_DIR/bin/activate
}

if [ ! -f "$CONFIG_FILE" ]; then
    # Create example config file
    echo "DISCORD_TOKEN = \"token here\"" >> $CONFIG_FILE
    echo "STORAGE_FILE = \"storage.json\"" >> $CONFIG_FILE
    echo "STARBOARD_CHANNEL_ID = \"0000000000000000000\"" >> $CONFIG_FILE
    echo "STARBOARD_MINIMUM_STARS = 5" >> $CONFIG_FILE
    echo "JOIN_LEAVE_MESSAGE = True" >> $CONFIG_FILE
fi

if [ ! -d "$VENV_DIR" ]; then
    # Create virtual environment and install required packages
    $PYTHON -m venv "$VENV_DIR"
    activate
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS"
else
    activate
fi
