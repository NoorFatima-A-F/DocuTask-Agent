"""
Evidence Capture Middleware automatically attaching evidence to execution contexts.
"""
from __future__ import annotations
from typing import Any, Dict, Optional
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceContext,
    EvidenceCategory,
    EvidenceArtifact,
)
from app.platform_verification.evidence_engine.core.collector import EvidenceCollector


class EvidenceCaptureMiddleware:
    """Middleware that intercepts verification execution steps and records evidence."""

    def __init__(self, collector: EvidenceCollector) -> None:
        self.collector = collector

    def capture_input(self, context: EvidenceContext, payload: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> EvidenceArtifact:
        art = self.collector.collect(
            execution_id=context.execution_id,
            category=EvidenceCategory.INPUT_EVIDENCE,
            data=payload,
            metadata=metadata or {"test_id": context.test_id, "environment": context.environment},
        )
        context.artifact_registry.append(art.artifact_id)
        return art

    def capture_runtime(self, context: EvidenceContext, logs: str, metadata: Optional[Dict[str, Any]] = None) -> EvidenceArtifact:
        art = self.collector.collect(
            execution_id=context.execution_id,
            category=EvidenceCategory.RUNTIME_EVIDENCE,
            data={"logs": logs},
            metadata=metadata or {"test_id": context.test_id},
        )
        context.artifact_registry.append(art.artifact_id)
        return art

    def capture_output(self, context: EvidenceContext, output: Dict[str, Any], metadata: Optional[Dict[str, Any]] = None) -> EvidenceArtifact:
        art = self.collector.collect(
            execution_id=context.execution_id,
            category=EvidenceCategory.OUTPUT_EVIDENCE,
            data=output,
            metadata=metadata or {"test_id": context.test_id},
        )
        context.artifact_registry.append(art.artifact_id)
        return art
