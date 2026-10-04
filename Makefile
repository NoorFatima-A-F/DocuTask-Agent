.PHONY: install check lint format test eval run-local docker-build docker-run clean

install:
	pip install --upgrade pip
	pip install -e ".[dev,evals]" || pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

lint:
	ruff check app/ tests/
	ruff format --check app/ tests/
	mypy app/ tests/ --ignore-missing-imports

format:
	ruff check --fix app/ tests/
	ruff format app/ tests/

test:
	pytest tests/ -v --cov=app --cov-report=term-missing --cov-fail-under=80 --ignore=tests/world --ignore=tests/world_model --ignore=tests/platform_verification

eval:
	python -m evals.harness --golden-dataset evals/data/golden_v1.jsonl --threshold 0.90

check: lint test eval
	@echo "All enterprise gates passed locally."

run-local:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

docker-build:
	docker build -t docutask-agent:latest .

docker-run:
	docker run -d --name docutask-agent -p 8000:8000 docutask-agent:latest
	@sleep 3
	curl -f http://localhost:8000/healthz || (docker logs docutask-agent && exit 1)

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov coverage.xml artifacts/
	find . -type d -name "__pycache__" -exec rm -rf {} +
