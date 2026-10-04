.PHONY: install lint format test eval run-local clean

install:
	pip install --upgrade pip
	pip install -e ".[dev,evals]" || pip install -r requirements.txt -r requirements-dev.txt

lint:
	ruff check app/ tests/
	ruff format --check app/ tests/
	mypy app/ --ignore-missing-imports

format:
	ruff format app/ tests/
	ruff check --fix app/ tests/

test:
	pytest tests/ -v --cov=app --cov-report=term-missing --ignore=tests/world --ignore=tests/world_model --ignore=tests/platform_verification

eval:
	python -m evals.harness --golden-dataset evals/data/golden_v1.jsonl --threshold 0.90

run-local:
	uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	rm -rf .pytest_cache .ruff_cache .mypy_cache htmlcov coverage.xml artifacts/
	find . -type d -name "__pycache__" -exec rm -rf {} +
