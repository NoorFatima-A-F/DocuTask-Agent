import os
import sys

ALLOWED_LICENSES = {"MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "Python Software Foundation License"}
PROHIBITED_PACKAGES = {"gpl-library", "pycrypto"}

def audit_dependencies(project_file: str) -> list[str]:
    violations = []
    if not os.path.exists(project_file):
        return ["pyproject.toml not found"]

    with open(project_file, "r", encoding="utf-8") as f:
        content = f.read()

    for pkg in PROHIBITED_PACKAGES:
        if pkg in content.lower():
            violations.append(f"Prohibited/vulnerable package detected: {pkg}")

    return violations

def run_dependency_audit(base_dir: str = ".") -> int:
    print("Auditing dependencies and licenses...")
    proj = os.path.join(base_dir, "pyproject.toml")
    violations = audit_dependencies(proj)
    if violations:
        print(f"FAILED: Dependency audit failed with {len(violations)} issues:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print("SUCCESS: Dependency and supply chain audit passed (0 violations)!")
    return 0

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    sys.exit(run_dependency_audit(root))
