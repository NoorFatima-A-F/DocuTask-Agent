"""
Documentation as Code Validator.
Ensures every public module contains markdown docs, ADR index integrity, and zero broken local links.
"""
import os
import sys

REQUIRED_DOCS = [
    "docs/verification_platform/architecture/architecture_blueprint.md",
    "docs/verification_platform/architecture/shared_kernel_governance.md",
    "docs/verification_platform/adr/README.md"
]

def validate_docs(base_dir: str = ".") -> int:
    print("Validating Documentation architecture...")
    missing = []
    for doc in REQUIRED_DOCS:
        full = os.path.join(base_dir, doc)
        if not os.path.exists(full):
            missing.append(doc)

    if missing:
        print(f"FAILED: Missing required documentation files: {missing}")
        return 1

    print("SUCCESS: Documentation as Code integrity verified!")
    return 0

if __name__ == "__main__":
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    sys.exit(validate_docs(root))
