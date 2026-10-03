"""
Phase 3Q: Source Control Change Impact Analyzer.
"""

from datetime import datetime, timezone
from typing import List, Optional

from ..domain.interfaces import IChangeImpactAnalyzer
from ..domain.models import ChangeImpactReport


class ChangeImpactAnalyzer(IChangeImpactAnalyzer):
    """
    Analyzes modified file paths in PR/commit to intelligently determine
    impacted architectural components and required verification test suites.
    """

    DEFAULT_FILES = [
        "docker-compose.yml",
        "Dockerfile",
        "requirements.txt",
        "app/api/v1/documents.py",
        "app/workers/celery_app.py",
        "app/platform_verification/enterprise_infrastructure_security/",
    ]

    def analyze_changes(self, modified_files: Optional[List[str]] = None) -> ChangeImpactReport:
        files = modified_files if modified_files is not None else self.DEFAULT_FILES
        changed_components = set()
        required_suites = set()

        for f in files:
            f_lower = f.lower()
            if "docker" in f_lower or "compose" in f_lower:
                changed_components.add("Container Runtime")
                required_suites.add("container_verification")
                required_suites.add("deployment_verification")
            if "requirement" in f_lower or "pyproject" in f_lower or "poetry" in f_lower:
                changed_components.add("Dependencies & Supply Chain")
                required_suites.add("security_scan")
                required_suites.add("vulnerability_verification")
            if "worker" in f_lower or "celery" in f_lower or "queue" in f_lower:
                changed_components.add("Task Queue & Worker Engine")
                required_suites.add("worker_resilience")
                required_suites.add("chaos_test")
            if "api" in f_lower or "router" in f_lower or "gateway" in f_lower:
                changed_components.add("FastAPI Gateway")
                required_suites.add("performance_test")
                required_suites.add("security_scan")
            if "security" in f_lower or "auth" in f_lower:
                changed_components.add("IAM & Zero-Trust Engine")
                required_suites.add("security_scan")

        if not changed_components:
            changed_components.add("General Codebase")
            required_suites.add("smoke_verification")

        return ChangeImpactReport(
            changed_components=sorted(list(changed_components)),
            files_modified=files,
            required_test_suites=sorted(list(required_suites)),
            trigger_reason=f"Detected changes across {len(changed_components)} subsystem(s)",
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
