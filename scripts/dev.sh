#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-"$ROOT_DIR/venv/bin/python"}"
BACKEND_HOST="${BACKEND_HOST:-127.0.0.1}"
BACKEND_PORT="${BACKEND_PORT:-8000}"
FRONTEND_HOST="${FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT="${FRONTEND_PORT:-8501}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "Could not find Python at: $PYTHON_BIN"
  echo "Run: python -m venv venv && ./venv/bin/python -m pip install -r requirements.txt"
  exit 1
fi

if command -v redis-cli >/dev/null 2>&1; then
  if ! redis-cli ping >/dev/null 2>&1; then
    echo "Warning: Redis/FalkorDB is not responding on localhost:6379."
    echo "Start it with: redis-server"
    echo
  fi
fi

pids=()

cleanup() {
  trap - EXIT INT TERM
  if ((${#pids[@]})); then
    echo
    echo "Stopping backend and frontend..."
    kill "${pids[@]}" >/dev/null 2>&1 || true
    wait "${pids[@]}" >/dev/null 2>&1 || true
  fi
}

trap cleanup EXIT INT TERM

echo "Starting backend:  http://$BACKEND_HOST:$BACKEND_PORT"
(
  cd "$ROOT_DIR"
  PYTHONPATH=. "$PYTHON_BIN" -m uvicorn backend.main:app \
    --reload \
    --host "$BACKEND_HOST" \
    --port "$BACKEND_PORT"
) &
pids+=("$!")

echo "Starting frontend: http://$FRONTEND_HOST:$FRONTEND_PORT"
(
  cd "$ROOT_DIR"
  "$PYTHON_BIN" -m streamlit run frontend/app.py \
    --server.address "$FRONTEND_HOST" \
    --server.port "$FRONTEND_PORT"
) &
pids+=("$!")

echo
echo "App is starting. Open: http://$FRONTEND_HOST:$FRONTEND_PORT"
echo "Press Ctrl+C to stop both services."

while true; do
  for pid in "${pids[@]}"; do
    if ! kill -0 "$pid" >/dev/null 2>&1; then
      wait "$pid" || exit $?
      exit 0
    fi
  done
  sleep 1
done
