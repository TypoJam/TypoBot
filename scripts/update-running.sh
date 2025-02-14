#! /usr/bin/env bash

BOT_SCRIPT="bot.TypoBot"
VENV_SCRIPT="scripts/venv.sh"

# Fetch latest changes
git pull

# Kill running process
pkill "$BOT_SCRIPT"

# Run new (updated) instance
source "$VENV_SCRIPT"
nohup python3 -m "$BOT_SCRIPT" &
