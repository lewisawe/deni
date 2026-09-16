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

# AI features use AWS Bedrock. Set AWS_PROFILE / AWS_REGION in your environment
# (or a .env) to enable them. If unset, the deterministic core still runs and the
# AI parse/explain features degrade gracefully.
export AWS_REGION="${AWS_REGION:-us-east-1}"

echo "Starting Deni on http://127.0.0.1:8000"
exec uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
