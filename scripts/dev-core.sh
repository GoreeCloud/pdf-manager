#!/usr/bin/env bash
# GoreeCloud PDF Manager: MIT-only development helper (no installs or deployments).
set -euo pipefail

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="${1:-help}"
BACKEND_PORT="${BACKEND_PORT:-8080}"
FRONTEND_PORT="${FRONTEND_PORT:-5173}"

usage() {
  cat <<'TEXT'
GoreeCloud PDF Manager - core-only development
  ./scripts/dev-core.sh backend    Start API on 127.0.0.1:8080
  ./scripts/dev-core.sh frontend   Start UI on 127.0.0.1:5173
  ./scripts/dev-core.sh both       Start API and UI; stop API when UI exits
  ./scripts/dev-core.sh verify     Verify sanitized import source

Prerequisites: JDK 25, Gradle 9.7.1, Node.js 24, and
  (cd frontend && npm ci --ignore-scripts --no-audit --no-fund)
This helper does not install software, expose a LAN port, or deploy a service.
TEXT
}

verify_core() {
  command -v python3 >/dev/null || { echo "Python 3 required" >&2; exit 2; }
  (cd "$ROOT" && python3 scripts/verify_import.py)
}

start_backend() {
  command -v gradle >/dev/null || {
    echo "Gradle 9.7.1 not found on PATH; install it and JDK 25 first." >&2
    exit 2
  }
  (cd "$ROOT" && \
    SERVER_ADDRESS=127.0.0.1 SERVER_PORT="$BACKEND_PORT" \
    STIRLING_FLAVOR=core ENABLE_SAAS=false DISABLE_ADDITIONAL_FEATURES=true \
    gradle :stirling-pdf:bootRun -PbuildWithFrontend=false --no-daemon)
}

start_frontend() {
  command -v node >/dev/null || { echo "Node.js 24 required" >&2; exit 2; }
  [[ -d "$ROOT/frontend/node_modules" ]] || {
    echo "Install locked frontend dependencies first: cd frontend && npm ci --ignore-scripts --no-audit --no-fund" >&2
    exit 2
  }
  (cd "$ROOT/frontend" && \
    BACKEND_URL="http://127.0.0.1:$BACKEND_PORT" \
    STIRLING_FLAVOR=core ENABLE_SAAS=false \
    ./node_modules/.bin/vite --mode core --host 127.0.0.1 --port "$FRONTEND_PORT" --strictPort)
}

case "$MODE" in
  help|-h|--help) usage ;;
  verify) verify_core ;;
  backend) verify_core; start_backend ;;
  frontend) verify_core; start_frontend ;;
  both)
    verify_core
    start_backend &
    backend_pid="$!"
    trap 'kill "$backend_pid" 2>/dev/null || true' EXIT INT TERM
    start_frontend
    ;;
  *) usage >&2; exit 2 ;;
esac
