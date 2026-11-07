# Remediation baseline (pre-remediation)

Measured on 2026-11-08 at commit `c88587db` (tag `archive/pre-remediation`), Windows 11,
Python 3.12.1. Everything deleted during remediation stays recoverable from that tag.

| Metric | Value | How measured |
|---|---|---|
| Python files (repo, excl. `.git`, `node_modules`) | 8,145 | `find . -name '*.py'` |
| Python LOC (repo) | 643,226 | `wc -l` over the above |
| Python files under `app/` | 7,060 | `find app -name '*.py'` |
| Python LOC under `app/` | 511,363 | `wc -l` |
| Modules reachable from `app.main` | 1,469 / 7,058 (20.8%) | `python tooling/reachability.py` |
| LOC reachable from `app.main` | 122,200 / 511,252 (23.9%) | `python tooling/reachability.py` |
| OpenAPI paths | 856 | `python tooling/api_metrics.py` |
| OpenAPI operations | 914 | `python tooling/api_metrics.py` |
| Operations with no auth dependency | 894 | `tooling/api_metrics.py` (static dependency walk) |
| Route modules with unprotected operations | 42 | `tooling/api_metrics.py` |
| Parameter-free GETs returning 200 without a token | 448 / 469 | `tooling/api_metrics.py` (live probe) |
| Tests (default `pytest` collection) | 2,884 passed, 0 failed | `ENVIRONMENT=test python -m pytest -q -o addopts=""` (6m01s) |
| `import app.main` time (cold) | 60.8 s | `tooling/api_metrics.py` |
| Tracked `.pyc` files | 27 | `git ls-files '*.pyc'` |

The passing test count includes tests that assert fabricated fallback behaviour (for
example `tests/test_ai_provider.py::test_gemini_dev_mode_generation`), so "all green" is
not evidence that extraction works.

## `ruff check --isolated --select F821,F841,F811,E722 app`

```
13	F841	[-] unused-variable
 9	F821	[ ] undefined-name
Found 22 errors.

app\platform_verification\api_verification\core\api_ast_analyzer.py:87:57: F821 Undefined name `Tuple`
app\platform_verification\architecture_verification\core\dependency_graph.py:34:33: F821 Undefined name `Tuple`
app\platform_verification\cicd_pipeline\core\pipeline_orchestrator.py:43:37: F821 Undefined name `Any`
app\platform_verification\clean_architecture\core\metrics_calculator.py:25:22: F821 Undefined name `Set`
app\platform_verification\config_versioning\core\feature_flags.py:14:43: F821 Undefined name `Any`
app\platform_verification\evaluation_engine\core\ab_testing.py:16:37: F821 Undefined name `Optional`
app\platform_verification\reporting_audit\core\audit_export_manager.py:73:47: F821 Undefined name `Optional`
app\platform_verification\solid_verification\core\ast_class_analyzer.py:56:16: F821 Undefined name `Optional`
app\platform_verification\solid_verification\core\ast_class_analyzer.py:56:46: F821 Undefined name `Optional`
```

All nine undefined names are in `app/platform_verification/`, which is unreachable from
`app.main` and is scheduled for deletion in Phase 4.

## Reproducing

```bash
python tooling/reachability.py --packages
python tooling/api_metrics.py
ruff check --isolated --select F821,F841,F811,E722 app
```
