# Remediation metrics after Phase 4

Measured on 2026-11-08 on branch `remediation/phase-4-delete-scaffolding`, Windows 11,
Python 3.12.1, with the same commands as [baseline.md](baseline.md).

| Metric | Baseline | After Phase 4 | How measured |
|---|---:|---:|---|
| Python files (repo, excl. `.git`, `node_modules`) | 8,145 | 182 | `find . -name '*.py'` |
| Python files under `app/` | 7,060 | 98 | `find app -name '*.py'` |
| Python LOC under `app/` | 511,363 | 7,554 | `wc -l` |
| Modules reachable from `app.main` | 1,469 / 7,058 (20.8%) | 98 / 98 (100%) | `python tooling/reachability.py` |
| LOC reachable from `app.main` | 122,200 / 511,252 (23.9%) | 7,554 / 7,554 (100%) | `python tooling/reachability.py` |
| OpenAPI paths | 856 | 33 | `python tooling/api_metrics.py` |
| OpenAPI operations | 914 | 36 | `python tooling/api_metrics.py` |
| Operations with no auth dependency | 894 | 5 (`/healthz`, `/readyz`, auth login/register/refresh) | `tooling/api_metrics.py --list` |
| Parameter-free GETs returning 200 without a token | 448 / 469 | 1 / 8 (`/healthz`) | `tooling/api_metrics.py` (live probe) |
| Tests (default collection) | 2,884 passed | 271 passed, 0 failed | `ENVIRONMENT=test python -m pytest -q -o addopts=""` (37 s) |
| `import app.main` time | 60.8 s | 4.65 s | `tooling/api_metrics.py` |
| Tracked `.pyc` files | 27 | 0 | `git ls-files '*.pyc'` |
| `ruff check --isolated --select F821,F841,F811,E722 app` | 13 findings | 0 | |
| `ruff check app tests tooling` (project config) | — | All checks passed | |

The test count fell because tests for deleted packages were deleted with them. Every remaining
test exercises code on the document path, and the fabrication tests from Phases 1–3 still pass.

Enforced by `tests/test_api_surface_guard.py`: at most 40 operations, every non-public route
returns 401 without a token, and `app/` stays under 10,000 lines.

Deleted paths and the reason for each are in [deletions.md](deletions.md).
