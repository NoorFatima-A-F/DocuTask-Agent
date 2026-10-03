"""
Bounded Context & Module Scaffolder CLI.
Generates complete 4-layer Hexagonal architecture layout for new verification domains.
"""
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
    import re
    from pathlib import Path
    sanitized_name = re.sub(r'[^a-zA-Z0-9_]', '_', context_name.lower())
    base = Path(base_path).resolve()
    target = (base / sanitized_name).resolve()
    if not (target == base or target.is_relative_to(base)):
        raise ValueError(f"Invalid context name: '{context_name}'")
    for rel_path, content in TEMPLATE_FILES.items():
        full_path = (target / rel_path).resolve()
        if not full_path.is_relative_to(target):
            continue
        full_path.parent.mkdir(parents=True, exist_ok=True)
        if not full_path.exists():
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
    return str(target)

if __name__ == "__main__":
    name = sys.argv[1] if len(sys.argv) > 1 else "sample_domain"
    out = scaffold_bounded_context(name)
    print(f"Scaffolded bounded context '{name}' at {out}")
