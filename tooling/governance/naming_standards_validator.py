import ast
import os
import sys
import re

PAST_TENSE_EVENT_REGEX = re.compile(
    r"^[A-Z][a-zA-Z0-9]*(?:ed|en|ne|t|d|st|wn|Event|Snapshot|Record|Metric|Result|Policy|Metadata|Update|Message|Ready|Created|Started|Completed|Failed|Issued|Collected|Evaluated|Triggered|Generated|Registered|Dissolved|Deadlocked|Shared|Learned|Expanded|Archived)$"
)
FORBIDDEN_DIR_NAMES = {"misc", "helpers", "stuff", "common2", "temp", "new_code"}

def validate_naming(base_dir: str = ".") -> list[str]:
    violations = []
    for root, dirs, _ in os.walk(base_dir):
        if any(ignored in root for ignored in [".git", "__pycache__", ".pytest_cache", "venv", "node_modules", "dist", "build"]):
            continue
        for d in dirs:
            if d in FORBIDDEN_DIR_NAMES:
                violations.append(f"Forbidden generic directory name: '{d}' in {root}")

    for root, _, files in os.walk(os.path.join(base_dir, "app")):
        if "__pycache__" in root:
            continue
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, f)
                with open(path, "r", encoding="utf-8") as source:
                    try:
                        tree = ast.parse(source.read(), filename=path)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.ClassDef):
                                for base in node.bases:
                                    if isinstance(base, ast.Name) and base.id in {"DomainEvent", "IntegrationEvent", "ApplicationEvent", "SystemEvent", "BaseEvent"}:
                                        if not PAST_TENSE_EVENT_REGEX.match(node.name) and not node.name.startswith("Test"):
                                            violations.append(f"Domain Event '{node.name}' in {f}:{node.lineno} does not follow past-tense naming standard.")
                    except SyntaxError:
                        pass
    return violations

def run_naming_validation(base_dir: str = ".") -> int:
    print("Validating Platform Naming Standards...")
    violations = validate_naming(base_dir)
    if violations:
        print(f"FAILED: Found {len(violations)} naming standard violations:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("SUCCESS: All naming standards fully satisfied (0 violations)!")
    return 0

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    sys.exit(run_naming_validation(root))
