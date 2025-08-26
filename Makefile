# Simple Makefile to manage Kanban MVP backend/frontend
# Usage:
#   make help                # Show targets
#   make install             # Install backend and frontend dependencies
#   make backend             # Run backend (watch/reload)
#   make backend-nowatch     # Run backend without reload
#   make frontend            # Run frontend dev server (watch)
#   make frontend-preview    # Build and preview frontend (no watch)
#   make dev                 # Run backend + frontend both in watch mode
#   make run                 # Run backend (no reload) + frontend preview

SHELL := /bin/bash
BACKEND_DIR := backend
FRONTEND_DIR := frontend
HOST := 0.0.0.0
API_PORT := 8000
WEB_PORT := 5173

.PHONY: help install backend backend-nowatch frontend frontend-preview dev run

help:
	@echo "Targets:"
	@echo "  install            Install backend (pip) and frontend (npm) deps"
	@echo "  backend            Start FastAPI with reload on $(HOST):$(API_PORT)"
	@echo "  backend-nowatch    Start FastAPI without reload on $(HOST):$(API_PORT)"
	@echo "  frontend           Start Vite dev server on $(HOST):$(WEB_PORT)"
	@echo "  frontend-preview   Build and preview frontend (no watch) on $(HOST):$(WEB_PORT)"
	@echo "  dev                Run backend + frontend (watch mode both)"
	@echo "  run                Run backend (no reload) + frontend preview"

install:
	@set -euo pipefail; \
	cd $(BACKEND_DIR) && pip install -r requirements.txt; \
	cd ../$(FRONTEND_DIR) && npm install

backend:
	@set -euo pipefail; \
	cd $(BACKEND_DIR) && bash run.sh

backend-nowatch:
	@set -euo pipefail; \
	cd $(BACKEND_DIR) && DATA_FILE=./data/data.json python -m uvicorn app.main:app --host $(HOST) --port $(API_PORT)

frontend:
	@set -euo pipefail; \
	cd $(FRONTEND_DIR) && npm run dev -- --host $(HOST) --port $(WEB_PORT)

frontend-preview:
	@set -euo pipefail; \
	cd $(FRONTEND_DIR) && npm run build; \
	npm run preview -- --host $(HOST) --port $(WEB_PORT)

# Run both backend and frontend in watch mode; exits when either stops
# Use ctrl+c to stop both
dev:
	@set -euo pipefail; \
	( cd $(BACKEND_DIR) && bash run.sh ) & \
	B=$$!; \
	( cd $(FRONTEND_DIR) && npm run dev -- --host $(HOST) --port $(WEB_PORT) ) & \
	F=$$!; \
	trap 'kill $$B $$F 2>/dev/null || true' INT TERM; \
	wait $$B $$F

# Run both without watch: backend no-reload + frontend preview
run:
	@set -euo pipefail; \
	( cd $(FRONTEND_DIR) && npm run build ) ; \
	( cd $(BACKEND_DIR) && DATA_FILE=./data/data.json python -m uvicorn app.main:app --host $(HOST) --port $(API_PORT) ) & \
	B=$$!; \
	( cd $(FRONTEND_DIR) && npm run preview -- --host $(HOST) --port $(WEB_PORT) ) & \
	F=$$!; \
	trap 'kill $$B $$F 2>/dev/null || true' INT TERM; \
	wait $$B $$F
