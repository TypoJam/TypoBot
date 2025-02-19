#! /usr/bin/env fish

set VENV_DIR ".venv"
set PYTHON /usr/bin/env python3
set REQUIREMENTS "requirements.txt"
set CONFIG_FILE "bot/config.py"

function activate
    source $VENV_DIR/bin/activate.fish
end

if ! test -e "$CONFIG_FILE"
    # Create example config file
    echo "DISCORD_TOKEN = \"token here\"" >> $CONFIG_FILE
    echo "STORAGE_FILE = \"storage.json\"" >> $CONFIG_FILE
    echo "STARBOARD_CHANNEL_ID = \"0000000000000000000\"" >> $CONFIG_FILE
    echo "STARBOARD_MINIMUM_STARS = 5" >> $CONFIG_FILE
    echo "JOIN_LEAVE_MESSAGE = True" >> $CONFIG_FILE
end

if ! test -d "$VENV_DIR"
    # Create virtual environment and install required packages
    $PYTHON -m venv "$VENV_DIR"
    activate
    pip install --upgrade pip
    pip install -r "$REQUIREMENTS"
else
    activate
end
