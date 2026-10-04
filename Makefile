.PHONY: install lint format test test-fast eval eval-smoke eval-all docker-up docker-down clean

install:
	pip install --upgrade pip
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	ruff check .
	ruff format --check .
	mypy app/ --ignore-missing-imports

format:
	ruff format .
	ruff check --fix .

test:
	pytest tests/ -v --import-mode=importlib --cov=app --cov-report=term-missing

test-fast:
	pytest tests/ -q --import-mode=importlib

eval:
	python -m evals.harness --golden-dataset evals/data/golden_v1.jsonl --threshold 0.90

eval-smoke:
	python -m evals.runner --dataset-tier smoke

eval-all:
	python -m evals.runner --dataset-tier regression-gold

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down --remove-orphans

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov coverage.xml artifacts/
	find . -type d -name "__pycache__" -exec rm -rf {} +
