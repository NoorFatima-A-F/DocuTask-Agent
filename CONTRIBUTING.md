# Engineering Contribution Guidelines

## 1. Development Workflow
1. Create a feature branch off `main`: `feature/issue-<id>-<description>`.
2. Ensure strict adherence to repository topology boundaries.
3. Write unit, integration, and contract tests for all new capabilities.
4. Run static governance validation:
   ```bash
   python tooling/governance/repository_validator.py
   python -m pytest tests/platform_verification/ -v
   ```
5. Ensure 0 lint errors, 0 type errors, and 100% test pass rate.

## 2. Code Structure Guidelines
- Place business logic in `app/platform_verification/`.
- Place generic enterprise primitives in `app/shared_kernel/`.
- Place database, cache, storage, and telemetry adapters in `app/infrastructure/`.
- Place ingress endpoints, CLI tools, and API routers in `app/interfaces/`.
- Never commit secrets, raw evidence, or mock payloads into source control.
