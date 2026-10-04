# Contributing to DocuTask-Agent

Thank you for contributing to DocuTask-Agent. This project follows strict enterprise engineering practices, architectural boundaries, and deterministic quality gates.

---

## 1. Branching & PR Discipline

1. **Trunk-Based Feature Branches**:
   - Create focused branches off `main`: `feature/short-description` or `fix/issue-id`.
   - Never commit directly to `main` without PR review and passing CI gates.

2. **Pull Request Verification Matrix**:
   All PRs must satisfy the local validation suite before merge:
   ```bash
   # 1. Linting & Formatting
   ruff check app/ tests/ cli/ evals/ tooling/

   # 2. Static Type Checking
   mypy app/ --ignore-missing-imports

   # 3. Security AST & Dependency Auditing
   bandit -r app/ -ll -q
   pip-audit -r requirements.txt --ignore-vuln PYSEC-2026-1325

   # 4. Pytest Test Matrix
   pytest tests/ -v

   # 5. Autonomous Evaluation Matrix
   python -m cli.agent_cli evaluate --suite all
   ```

---

## 2. Architecture & Design Standards

- **Deterministic Contracts**: Always enforce Pydantic v2 validation for model and agent input/output boundaries (`app/schemas/`).
- **Telemetry & Tracing**: Instrument non-deterministic LLM operations with `AgentSpan` and structured JSON logs (`app/core/telemetry.py`).
- **Architecture Decision Records (ADRs)**: If you introduce structural changes, database migrations, or model selections, submit an ADR under `docs/adr/`.
- **Fault-Tolerant Async Tasks**: Asynchronous tasks must define retry backoff, jitter, and route terminal failures to Dead-Letter Queues (DLQ) (`app/workers/tasks.py`).
- **Path Portability**: Always resolve file and configuration paths dynamically using `REPO_ROOT` and `CONFIG_DIR` (`app/core/config.py`). Never use hardcoded absolute paths.

---

## 3. Release & Tagging Hygiene

Releases follow [Semantic Versioning 2.0.0](https://semver.org/):
- **Major (`v1.0.0`)**: Breaking API or schema changes.
- **Minor (`v1.1.0`)**: Backwards-compatible features and new agent capabilities.
- **Patch (`v1.0.1`)**: Bug fixes and security patches.
