"""Dependency and Supply Chain Package Collector."""

from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class DependencyCollector(BaseCollector):
    """Parses declared dependencies, version pins, and Dependabot monitoring rules."""

    @property
    def name(self) -> str:
        return "DependencyCollector"

    @property
    def category(self) -> str:
        return "DependencyHygiene"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        req_file = self.repo_root / "requirements.txt"
        pyproject_file = self.repo_root / "pyproject.toml"
        dependabot_file = self.repo_root / ".github" / "dependabot.yml"

        dependencies: List[str] = []
        unpinned_dependencies: List[str] = []

        if req_file.exists():
            with open(req_file, "r", encoding="utf-8") as fp:
                for line in fp:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        dependencies.append(line)
                        if "==" not in line and ">=" not in line and "<=" not in line:
                            unpinned_dependencies.append(line)

        dependabot_present = dependabot_file.exists()

        payload: Dict[str, Any] = {
            "total_dependencies": len(dependencies),
            "dependencies": dependencies,
            "unpinned_dependencies_count": len(unpinned_dependencies),
            "unpinned_dependencies": unpinned_dependencies,
            "pyproject_exists": pyproject_file.exists(),
            "dependabot_configured": dependabot_present,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_CONFIGURATION
            if len(unpinned_dependencies) == 0 and dependabot_present
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.CONFIGURATION_FILE,
            raw_payload=payload,
            summary=f"Parsed {len(dependencies)} declared dependencies. Unpinned: {len(unpinned_dependencies)}. Dependabot configured: {dependabot_present}.",
            confidence=EvidenceConfidence.LOW,
            classification=classification,
        )
        records.append(record)
        return records
