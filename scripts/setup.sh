#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Please edit it before running the bot."
fi

echo "Setup complete."