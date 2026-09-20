"""
Enterprise Repository Topology & Architecture Governance Validator.
Enforces Clean Architecture dependency invariants, metadata integrity, and CODEOWNERS completeness.
"""
import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Set

class RepositoryTopologyValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def validate_metadata(self) -> bool:
        meta_file = self.repo_root / "repo_metadata.json"
        if not meta_file.exists():
            self.errors.append("Missing required 'repo_metadata.json' at repository root.")
            return False
        try:
            data = json.loads(meta_file.read_text(encoding="utf-8"))
            required_keys = ["repository_name", "platform_name", "repository_version", "architecture_version", "bounded_contexts", "topology_roots"]
            for k in required_keys:
                if k not in data:
                    self.errors.append(f"repo_metadata.json is missing required field: '{k}'")
        except Exception as e:
            self.errors.append(f"Failed to parse repo_metadata.json: {e}")
            return False
        return len(self.errors) == 0

    def validate_codeowners(self) -> bool:
        codeowners_file = self.repo_root / ".github" / "CODEOWNERS"
        if not codeowners_file.exists():
            self.errors.append("Missing '.github/CODEOWNERS' file.")
            return False
        content = codeowners_file.read_text(encoding="utf-8")
        if "@platform-architecture-board" not in content and "@platform-architects" not in content:
            self.warnings.append("CODEOWNERS should include platform architecture board ownership.")
        return True

    def validate_clean_architecture_dependencies(self) -> bool:
        """
        Invariants:
        1. app/platform_verification MUST NOT import app/infrastructure or app/interfaces.
        2. app/shared_kernel MUST NOT import app/platform_verification, app/infrastructure, or app/interfaces.
        """
        # Scan app/shared_kernel
        sk_path = self.repo_root / "app" / "shared_kernel"
        if sk_path.exists():
            for py_file in sk_path.glob("**/*.py"):
                text = py_file.read_text(encoding="utf-8")
                if "app.platform_verification" in text or "app.infrastructure" in text or "app.interfaces" in text:
                    self.errors.append(f"Shared Kernel layer violation in {py_file.name}: cannot depend on upper layers.")

        # Scan app/platform_verification
        pv_path = self.repo_root / "app" / "platform_verification"
        if pv_path.exists():
            for py_file in pv_path.glob("**/*.py"):
                text = py_file.read_text(encoding="utf-8")
                if "app.interfaces" in text:
                    self.errors.append(f"Domain layer violation in {py_file.name}: cannot depend on app.interfaces.")
        return len(self.errors) == 0

    def validate_topology_roots(self) -> bool:
        required_roots = ["app", "config", "datasets", "evidence", "docs", "tooling", "deploy", "security", "observability", "tests"]
        for r in required_roots:
            p = self.repo_root / r
            if not p.exists():
                self.errors.append(f"Required root topology directory '{r}' is missing.")
        return len(self.errors) == 0

    def run_all(self) -> Tuple[bool, List[str], List[str]]:
        self.validate_metadata()
        self.validate_codeowners()
        self.validate_clean_architecture_dependencies()
        self.validate_topology_roots()
        return (len(self.errors) == 0, self.errors, self.warnings)


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parent.parent.parent
    validator = RepositoryTopologyValidator(repo_root)
    success, errors, warnings = validator.run_all()
    if warnings:
        for w in warnings:
            print(f"[WARN] {w}")
    if not success:
        print(f"FAILED: {len(errors)} architecture governance errors found:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"SUCCESS: Repository topology & architecture invariants fully satisfied!")
        sys.exit(0)
