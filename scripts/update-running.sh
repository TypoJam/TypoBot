#! /usr/bin/env bash

BOT_SCRIPT="bot/TypoBot.py"
VENV_SCRIPT="scripts/venv.sh"

# Fetch latest changes
git pull

# Kill running process
pkill -f "$BOT_SCRIPT"

# Run new (updated) instance
source "$VENV_SCRIPT"
nohup python3 "$BOT_SCRIPT" &
