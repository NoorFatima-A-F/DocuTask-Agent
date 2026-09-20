"""
Bounded Context & Module Scaffolder CLI.
Generates complete 4-layer Hexagonal architecture layout for new verification domains.
"""
import os
import sys

TEMPLATE_FILES = {
    "domain/__init__.py": "# Domain Layer\n",
    "application/__init__.py": "# Application Layer\n",
    "infrastructure/__init__.py": "# Infrastructure Layer\n",
    "interfaces/__init__.py": "# Interfaces Layer\n",
    "contracts.py": "# Published contracts and integration schemas\n",
    "__init__.py": "# Context entrypoint\n"
}

def scaffold_bounded_context(context_name: str, base_path: str = "app/contexts") -> str:
    target_dir = os.path.join(base_path, context_name.lower())
    for rel_path, content in TEMPLATE_FILES.items():
        full_path = os.path.join(target_dir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        if not os.path.exists(full_path):
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
    return target_dir

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "sample_domain"
    out = scaffold_bounded_context(name)
    print(f"Scaffolded bounded context '{name}' at {out}")
