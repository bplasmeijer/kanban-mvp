#!/usr/bin/env bash
set -euo pipefail
export $(grep -v '^#' .env 2>/dev/null | xargs -d '\n' -r) || true
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
DATA_FILE=${DATA_FILE:-./data/data.json}
export DATA_FILE

# Ensure data file exists
mkdir -p ./data
if [ ! -f "$DATA_FILE" ]; then
  echo '{"board":{"id":"board-1","name":"Kanban"},"columns":[{"id":"todo","name":"Todo","position":0},{"id":"inprogress","name":"In Progress","position":1},{"id":"done","name":"Done","position":2}],"tasks":[]}' > "$DATA_FILE"
fi

python -m uvicorn app.main:app --host "$HOST" --port "$PORT" --reload
