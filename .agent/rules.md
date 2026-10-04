# Antigravity Agent Engineering Directives & Operational Rules

## 1. Architectural Integrity & Repository Hygiene
- **Zero Root Pollution**: Never create arbitrary scripts, markdown dumps, or temporary directories in the repository root. All application code belongs in `app/`, tests in `tests/`, benchmarks in `evals/`, configuration in `config/`, and infrastructure in `docker/` or `.github/`.
- **Encapsulated Modularity**: Maintain clear package boundaries. Service dependencies must be injected or configured via structured settings (`config/settings.py` or `config/health/`).

## 2. CI/CD & Development Discipline
- **Canonical Pipelines**: The repository maintains strictly three core GitHub Actions workflows:
  1. `ci.yml`: Ruff linting, Ruff formatting check, Mypy static typing, Pytest test suite with coverage enforcement.
  2. `security.yml`: Secret scanning, Bandit SAST security audit, Dependency vulnerability checks.
  3. `agent-eval.yml`: Golden benchmark evaluation harness, OCR fuzzer resilience, schema conformity.
- **Zero Direct-to-Main Pushing**: All engineering modifications must be developed on feature branches (`feat/`, `fix/`, `chore/`) and validated via local pre-flight checks before merging into `main`.
- **Deterministic Pre-Flight Checks**: Prior to pushing, execute:
  ```bash
  ruff check . --fix
  ruff format .
  mypy app/ --ignore-missing-imports
  pytest tests/ -q
  python -m evals.harness --golden-dataset evals/data/golden_v1.jsonl
  ```

## 3. Evaluation & Benchmarking Standards
- **Golden Evaluation Datasets**: Benchmarks reside under `evals/data/` (`golden_v1.jsonl`) and `evals/datasets/`.
- **Offline Mock Execution**: Automated CI testing must execute deterministically with offline mock inference (`--mock-llm`) to prevent rate-limiting, flakiness, or secret leaks.
- **Regression Gates**: Evaluation metrics (schema conformity, tool selection F1, OCR character error rate) must pass configured thresholds (>= 0.90) for all release candidates.

## 4. Security & Compliance
- **Zero Hardcoded Secrets**: Secrets and API keys must be loaded exclusively via environment variables or secret managers.
- **Vulnerability Remediation**: All critical/high CVEs in third-party dependencies must be remediated or pinned to secure releases immediately.
