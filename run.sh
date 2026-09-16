#!/usr/bin/env bash
# Deni: one-command local run. Clones-and-runs in under a minute.
set -euo pipefail

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  echo "Creating virtualenv..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

export AWS_PROFILE="${AWS_PROFILE:-simi-ops}"
export AWS_REGION="${AWS_REGION:-us-east-1}"

echo "Starting Deni on http://127.0.0.1:8000"
exec uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
