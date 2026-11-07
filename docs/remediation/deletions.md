# Phase 4 deletion manifest

Everything listed here is recoverable from the tag `archive/pre-remediation`
(`git checkout archive/pre-remediation -- <path>`).

**Method.** `tooling/reachability.py` walks the static import graph from `app.main`. After
trimming `app/api/v1/router.py` to the document-path routers (auth, documents, ocr, ai,
jobs, reviews), every tracked file under `app/` that is not reachable was deleted (keeping
`__init__.py` of kept packages). Reachable modules were all inside the allowlisted packages,
so no helper had to be inlined. Tests were deleted when they only exercised deleted code;
tests mixing kept and deleted code were trimmed (`tests/security/test_url_validation.py`,
`tests/test_refactoring.py` -> `tests/test_secret_strength.py`).

Also removed in this phase (not file deletions):
- 39 routers from `app/api/v1/router.py`, the duplicate `/api/v1/health` endpoint, the
  `/api/v1` mount of the health router, and the hidden `/health/live` and `/health/ready` aliases.
- The PBKDF2 password-hash fallback with a static salt in `app/core/security.py`.
- Unused dependencies: `google-genai`, `numpy`, `rsa`, `cryptography`, `passlib`, `pyyaml`,
  `pytest-mock`, `pre-commit`, and the `evals`/`resilience`/`test` extras.

**Total: 8931 tracked files deleted.**

| Path | Files | Why |
|---|---:|---|
| `.audit_registry` | 3 | self-issued "certification" records |
| `app/agents` | 824 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/api` | 43 | unreachable modules inside a kept package (not imported from `app.main`) |
| `app/audit` | 47 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/business_validation` | 26 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/business_value_verification` | 21 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/certification` | 17 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/cli` | 3 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/cognitive_intelligence_verification` | 44 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/connectors` | 53 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/contexts` | 122 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/core` | 36 | unreachable modules inside a kept package (not imported from `app.main`) |
| `app/customer_experience` | 28 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/data_governance` | 33 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/deployment` | 42 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/document_intelligence_verification` | 42 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/evaluation` | 34 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/events` | 5 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/evidence` | 61 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/governance` | 90 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/infrastructure` | 280 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/interfaces` | 3 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/jobs` | 4 | unreachable modules inside a kept package (not imported from `app.main`) |
| `app/knowledge` | 39 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/knowledge_platform_verification` | 42 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/model_governance` | 31 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/models` | 3 | unreachable modules inside a kept package (not imported from `app.main`) |
| `app/networking` | 38 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/observability` | 57 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/oversight` | 38 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/performance_validation` | 30 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/performance_verification` | 32 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform` | 96 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_ai_lifecycle` | 29 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_certification` | 1 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_cognitive` | 27 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_core_verification` | 34 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_delivery` | 80 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_knowledge` | 27 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_saas` | 34 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_verification` | 3006 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/platform_workforce` | 35 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/prompts` | 38 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/runtime` | 1066 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/safety` | 50 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/sdk` | 11 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/security_validation` | 32 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/security_verification` | 41 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/shared_kernel` | 25 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/tenancy` | 35 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/verification` | 23 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/workers` | 1 | unreachable modules inside a kept package (not imported from `app.main`) |
| `app/workflows` | 52 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `app/workforce_verification` | 46 | package unreachable from `app.main` (scaffolding / simulated platform) |
| `cli` | 3 | CLI for the deleted agent platform |
| `config` | 8 | YAML policies read only by the removed health/metrics code |
| `datasets` | 15 | datasets for deleted evaluation scaffolding |
| `docs` | 65 | test-generated or unused file |
| `docs/adr` | 64 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/api` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/architecture` | 208 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/assets` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/audit` | 2 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/audit-engine` | 23 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/audits` | 373 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/deployment` | 3 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/examples` | 3 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/governance` | 13 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/infrastructure` | 50 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/networking` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/observability` | 2 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/phase25` | 8 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/platform-delivery` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/product` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/resilience_governance` | 15 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/runbooks` | 17 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/runtime_verification` | 12 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/security` | 14 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/standards` | 1 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/verification_architecture` | 9 | generated audit / certification / phase reports describing systems that do not exist |
| `docs/verification_platform` | 11 | generated audit / certification / phase reports describing systems that do not exist |
| `enterprise_audit_engine` | 146 | self-audit engine; not part of the product |
| `frontend` | 1 | built asset (`frontend/dist`) must not be committed; built in Docker |
| `infra` | 18 | k8s/terraform/grafana for components that do not exist; deployment is Docker/compose/HF/Render |
| `research_validation` | 219 | "research validation" scaffolding |
| `scripts` | 12 | one-off code generators |
| `src` | 4 | second, unused application entry point |
| `tests` | 31 | test-generated or unused file |
| `tests/agents` | 35 | tests for deleted `app/` packages |
| `tests/ai_lifecycle` | 2 | tests for deleted `app/` packages |
| `tests/ai_operations` | 2 | tests for deleted `app/` packages |
| `tests/audit` | 10 | tests for deleted `app/` packages |
| `tests/business` | 2 | tests for deleted `app/` packages |
| `tests/confidence` | 1 | tests for deleted `app/` packages |
| `tests/connectors` | 8 | tests for deleted `app/` packages |
| `tests/data_governance` | 10 | tests for deleted `app/` packages |
| `tests/deployment` | 11 | tests for deleted `app/` packages |
| `tests/distributed` | 2 | tests for deleted `app/` packages |
| `tests/events` | 1 | tests for deleted `app/` packages |
| `tests/execution` | 2 | tests for deleted `app/` packages |
| `tests/governance_analytics` | 10 | tests for deleted `app/` packages |
| `tests/governance_platform` | 8 | tests for deleted `app/` packages |
| `tests/infrastructure` | 60 | tests for deleted `app/` packages |
| `tests/intelligence` | 5 | tests for deleted `app/` packages |
| `tests/knowledge` | 8 | tests for deleted `app/` packages |
| `tests/learning` | 1 | tests for deleted `app/` packages |
| `tests/liveness` | 7 | tests for deleted `app/` packages |
| `tests/meta` | 1 | tests for deleted `app/` packages |
| `tests/model_governance` | 9 | tests for deleted `app/` packages |
| `tests/networking` | 10 | tests for deleted `app/` packages |
| `tests/observability` | 14 | tests for deleted `app/` packages |
| `tests/operations` | 1 | tests for deleted `app/` packages |
| `tests/optimization` | 1 | tests for deleted `app/` packages |
| `tests/organization` | 2 | tests for deleted `app/` packages |
| `tests/oversight` | 10 | tests for deleted `app/` packages |
| `tests/planner` | 1 | tests for deleted `app/` packages |
| `tests/platform` | 19 | tests for deleted `app/` packages |
| `tests/platform_cognitive` | 2 | tests for deleted `app/` packages |
| `tests/platform_delivery` | 1 | tests for deleted `app/` packages |
| `tests/platform_knowledge` | 2 | tests for deleted `app/` packages |
| `tests/platform_saas` | 2 | tests for deleted `app/` packages |
| `tests/platform_verification` | 123 | tests for deleted `app/` packages |
| `tests/platform_workforce` | 2 | tests for deleted `app/` packages |
| `tests/prompts` | 8 | tests for deleted `app/` packages |
| `tests/replay` | 1 | tests for deleted `app/` packages |
| `tests/resilience` | 1 | tests for deleted `app/` packages |
| `tests/runtime` | 129 | tests for deleted `app/` packages |
| `tests/safety` | 10 | tests for deleted `app/` packages |
| `tests/science` | 1 | tests for deleted `app/` packages |
| `tests/strategy` | 1 | tests for deleted `app/` packages |
| `tests/swarm` | 1 | tests for deleted `app/` packages |
| `tests/tenancy` | 9 | tests for deleted `app/` packages |
| `tests/truth` | 4 | tests for deleted `app/` packages |
| `tests/ui` | 12 | tests for deleted `app/` packages |
| `tests/workflows` | 7 | tests for deleted `app/` packages |
| `tests/world` | 1 | tests for deleted `app/` packages |
| `tests/world_model` | 2 | tests for deleted `app/` packages |
| `tooling/benchmarks` | 1 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `tooling/datasets` | 1 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `tooling/governance` | 9 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `tooling/migrations` | 1 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `tooling/scaffolding` | 2 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `tooling/verification` | 3 | scaffolding generators and governance validators; not used by build, CI or the document path |
| `verification` | 27 | verification/scoring scaffolding |
