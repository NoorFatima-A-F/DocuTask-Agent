"""
Shared Kernel Architecture & Invariant Validator.
Statically parses all files in app/shared_kernel using AST to ensure:
1. Zero forbidden imports (FastAPI, SQLAlchemy, Redis, Celery, Temporal, Docker, OpenAI, Gemini SDK, Cloud SDKs).
2. Zero imports from app.contexts, app.models, app.api, or app.infrastructure.
3. Strict adherence to Clean / DDD Shared Kernel principles.
"""
import ast
import os
import sys

SHARED_KERNEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../app/shared_kernel"))

FORBIDDEN_EXTERNAL_MODULES = {
    "fastapi", "starlette", "pydantic_settings",
    "sqlalchemy", "alembic", "psycopg2", "asyncpg",
    "redis", "celery", "temporalio", "docker",
    "google.genai", "google.cloud", "openai", "opentelemetry"
}

FORBIDDEN_INTERNAL_MODULES = {
    "app.contexts", "app.models", "app.api", "app.infrastructure", "app.services"
}

def validate_file(filepath: str) -> list[str]:
    violations = []
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError as e:
            return [f"SyntaxError in {filepath}: {e}"]

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                for forbidden in FORBIDDEN_EXTERNAL_MODULES:
                    if alias.name.startswith(forbidden):
                        violations.append(f"Forbidden external import '{alias.name}' in {os.path.basename(filepath)}:{node.lineno}")
                for forbidden in FORBIDDEN_INTERNAL_MODULES:
                    if alias.name.startswith(forbidden):
                        violations.append(f"Forbidden internal cross-layer import '{alias.name}' in {os.path.basename(filepath)}:{node.lineno}")

        elif isinstance(node, ast.ImportFrom):
            if node.module:
                for forbidden in FORBIDDEN_EXTERNAL_MODULES:
                    if node.module.startswith(forbidden):
                        violations.append(f"Forbidden external from-import '{node.module}' in {os.path.basename(filepath)}:{node.lineno}")
                for forbidden in FORBIDDEN_INTERNAL_MODULES:
                    if node.module.startswith(forbidden):
                        violations.append(f"Forbidden internal from-import '{node.module}' in {os.path.basename(filepath)}:{node.lineno}")

    return violations

def validate_shared_kernel() -> int:
    print(f"Validating Shared Kernel in: {SHARED_KERNEL_DIR}")
    all_violations = []

    for root, _, files in os.walk(SHARED_KERNEL_DIR):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                violations = validate_file(full_path)
                all_violations.extend(violations)

    if all_violations:
        print(f"FAILED: Found {len(all_violations)} Shared Kernel architectural violations:")
        for v in all_violations:
            print(f"  - {v}")
        return 1

    print("SUCCESS: Shared Kernel architectural invariants and dependency rules fully satisfied (0 violations)!")
    return 0

if __name__ == "__main__":
    sys.exit(validate_shared_kernel())
