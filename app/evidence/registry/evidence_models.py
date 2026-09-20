"""
Strongly Typed Evidence Registry Models for Zero-Trust AAOS.
Defines immutable evidence items, supported evidence types, verification statuses,
and cryptographic provenance metadata.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class EvidenceType(str, Enum):
    UNIT_TEST = "UNIT_TEST"
    INTEGRATION_TEST = "INTEGRATION_TEST"
    BENCHMARK = "BENCHMARK"
    STRESS_TEST = "STRESS_TEST"
    CHAOS_TEST = "CHAOS_TEST"
    PERFORMANCE_TEST = "PERFORMANCE_TEST"
    TELEMETRY = "TELEMETRY"
    RECOVERY_TEST = "RECOVERY_TEST"
    SECURITY_SCAN = "SECURITY_SCAN"
    MUTATION_TEST = "MUTATION_TEST"
    COVERAGE_REPORT = "COVERAGE_REPORT"
    LOAD_TEST = "LOAD_TEST"
    ARCHITECTURE_ANALYSIS = "ARCHITECTURE_ANALYSIS"
    RUNTIME_TRACE = "RUNTIME_TRACE"
    SCREENSHOT = "SCREENSHOT"
    DASHBOARD = "DASHBOARD"
    LOG_EVIDENCE = "LOG_EVIDENCE"
    DATASET = "DATASET"
    EVALUATION_RESULT = "EVALUATION_RESULT"
    HUMAN_VERIFICATION = "HUMAN_VERIFICATION"


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PENDING_VERIFICATION = "PENDING_VERIFICATION"
    FAILED_VERIFICATION = "FAILED_VERIFICATION"
    HASH_MISMATCH = "HASH_MISMATCH"
    SOURCE_UNAVAILABLE = "SOURCE_UNAVAILABLE"


@dataclass
class EvidenceItem:
    """
    An immutable, cryptographically verifiable piece of engineering evidence.
    Every claim in reports must trace directly to one or more EvidenceItem IDs.
    """

    evidence_id: str
    title: str
    description: str
    evidence_type: EvidenceType
    source: str
    generated_by: str
    timestamp: float = field(default_factory=time.time)
    git_commit: str = "HEAD"
    artifact_location: Optional[str] = None
    verification_status: VerificationStatus = VerificationStatus.VERIFIED
    confidence: float = 1.0
    reproducibility: str = "DETERMINISTIC"  # DETERMINISTIC, STATISTICAL, EMPIRICAL
    dependencies: List[str] = field(default_factory=list)
    raw_payload: Dict[str, Any] = field(default_factory=dict)
    item_hash: str = ""

    def __post_init__(self) -> None:
        if not self.item_hash:
            self.item_hash = self.compute_hash()

    def compute_hash(self) -> str:
        """Computes SHA-256 hash across core fields for tamper-evident provenance."""
        payload_str = json.dumps(self.raw_payload, sort_keys=True)
        content = (
            f"{self.evidence_id}:{self.title}:{self.evidence_type.value}:"
            f"{self.source}:{self.generated_by}:{self.timestamp}:{payload_str}"
        )
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Serializes evidence item to dictionary."""
        return {
            "evidence_id": self.evidence_id,
            "title": self.title,
            "description": self.description,
            "evidence_type": self.evidence_type.value,
            "source": self.source,
            "generated_by": self.generated_by,
            "timestamp": self.timestamp,
            "git_commit": self.git_commit,
            "artifact_location": self.artifact_location,
            "verification_status": self.verification_status.value,
            "confidence": self.confidence,
            "reproducibility": self.reproducibility,
            "dependencies": self.dependencies,
            "raw_payload": self.raw_payload,
            "item_hash": self.item_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> EvidenceItem:
        """Deserializes evidence item from dictionary."""
        data_copy = dict(data)
        data_copy["evidence_type"] = EvidenceType(data_copy["evidence_type"])
        data_copy["verification_status"] = VerificationStatus(data_copy["verification_status"])
        return cls(**data_copy)
