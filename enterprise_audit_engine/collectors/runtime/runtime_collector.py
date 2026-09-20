"""Runtime & Container Specification Collector."""

from pathlib import Path
from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.collectors.base import BaseCollector


class RuntimeCollector(BaseCollector):
    """Inspects Dockerfile and docker-compose.yml for production container patterns."""

    @property
    def name(self) -> str:
        return "RuntimeCollector"

    @property
    def category(self) -> str:
        return "RuntimeAndContainerization"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []
        dockerfile = self.repo_root / "Dockerfile"
        compose_file = self.repo_root / "docker-compose.yml"

        has_non_root = False
        has_multi_stage = False
        has_healthcheck = False

        if dockerfile.exists():
            with open(dockerfile, "r", encoding="utf-8") as fp:
                content = fp.read()
                has_non_root = "USER docutask" in content or "USER 10001" in content or "useradd" in content
                has_multi_stage = "AS builder" in content or "as builder" in content
                has_healthcheck = "HEALTHCHECK" in content

        has_compose = compose_file.exists()

        payload: Dict[str, Any] = {
            "dockerfile_exists": dockerfile.exists(),
            "has_non_root_user": has_non_root,
            "has_multi_stage_build": has_multi_stage,
            "has_dockerfile_healthcheck": has_healthcheck,
            "has_docker_compose": has_compose,
        }

        classification = (
            EvidenceClassification.VERIFIED_BY_CONFIGURATION
            if dockerfile.exists() and has_non_root and has_compose
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.CONFIGURATION_FILE,
            raw_payload=payload,
            summary=f"Container configuration verified: multi-stage ({has_multi_stage}), non-root user ({has_non_root}), healthcheck ({has_healthcheck}), compose orchestration ({has_compose}).",
            confidence=EvidenceConfidence.LOW,
            classification=classification,
        )
        records.append(record)
        return records
