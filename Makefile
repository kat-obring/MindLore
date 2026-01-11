PYTHON := python3
PIP := $(PYTHON) -m pip
BACKEND_DIR := backend
FRONTEND_DIR := frontend

.PHONY: help backend-install backend-lint backend-format backend-test frontend-install frontend-lint frontend-test frontend-build lint test install

help:
	@echo "Available targets:"
	@echo "  install            Install backend and frontend deps"
	@echo "  backend-install    Install backend deps (including dev)"
	@echo "  backend-lint       Run ruff lint on backend"
	@echo "  backend-format     Run black on backend"
	@echo "  backend-test       Run pytest on backend"
	@echo "  frontend-install   Install frontend deps"
	@echo "  frontend-lint      Run eslint on frontend"
	@echo "  frontend-test      Run vitest on frontend"
	@echo "  frontend-build     Run vite build on frontend"
	@echo "  lint               Run all lint tasks"
	@echo "  test               Run all tests"

install: backend-install frontend-install

backend-install:
	cd $(BACKEND_DIR) && $(PIP) install -e ".[dev]"

backend-lint:
	cd $(BACKEND_DIR) && ruff check .

backend-format:
	cd $(BACKEND_DIR) && black .

backend-test:
	cd $(BACKEND_DIR) && pytest

frontend-install:
	cd $(FRONTEND_DIR) && npm install

frontend-lint:
	cd $(FRONTEND_DIR) && npm run lint

frontend-test:
	cd $(FRONTEND_DIR) && npm test -- --run

frontend-build:
	cd $(FRONTEND_DIR) && npm run build

lint: backend-lint frontend-lint

test: backend-test frontend-test
