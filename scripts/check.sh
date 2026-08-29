#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

if [ -x ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
else
    PYTHON="python3"
fi

echo "Running compile check..."
"$PYTHON" -m compileall -q app main.py tests

echo "Running unit tests..."
"$PYTHON" -m unittest discover -s tests -v

echo "All checks passed."