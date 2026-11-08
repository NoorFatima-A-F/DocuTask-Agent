.PHONY: install migrate lint format test test-frontend check run worker docker-build docker-up

install:
	pip install -r requirements-dev.txt
	cd frontend && npm ci

migrate:
	alembic upgrade head

lint:
	ruff check app tests tooling migrations evals
	ruff format --check app tests tooling migrations evals
	mypy app tests evals

format:
	ruff check --fix app tests tooling migrations evals
	ruff format app tests tooling migrations evals

test:
	ENVIRONMENT=test pytest --cov=app --cov-report=term-missing --cov-fail-under=80

test-frontend:
	cd frontend && npm run build && npm test && npm run test:e2e

check: lint test test-frontend
	bandit -r app -q
	pip-audit -r requirements.txt

run: migrate
	uvicorn app.main:app --reload --port 8000

worker:
	celery -A app.jobs.celery_app worker --loglevel=info

docker-build:
	docker build -t docutask-agent:local .

docker-up:
	docker compose up --build
