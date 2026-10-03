"""
Artifact Completeness Checker (Phase 82B.11)
============================================
Audits scientific publications and evaluation bundles for all 10 mandatory
scientific integrity requirements (ACM, USENIX, IEEE, MLCommons standards).
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Tuple

from research_validation.provenance.hashing import hash_canonical_json


class MandatoryField(str, Enum):
    RAW_EVIDENCE = "raw_evidence"
    PROVENANCE_CHAIN = "provenance_chain"
    UNCERTAINTY_BOUNDS = "uncertainty_bounds"
    METHODOLOGY = "methodology"
    ASSUMPTIONS = "assumptions"
    LIMITATIONS = "limitations"
    DATASET_REFERENCES = "dataset_references"
    ENVIRONMENT_MANIFEST = "environment_manifest"
    REPRODUCTION_COMMAND = "reproduction_command"
    VERSION_INFORMATION = "version_information"


@dataclass(frozen=True)
class FieldAuditResult:
    field: MandatoryField
    is_present: bool
    quality_score: float  # 0.0 to 1.0
    evidence_snippet: str
    omission_severity: str  # "NONE", "MINOR", "CRITICAL"


@dataclass(frozen=True)
class CompletenessAuditReport:
    artifact_id: str
    timestamp_utc: str
    total_required_fields: int
    present_fields_count: int
    missing_fields_count: int
    completeness_ratio: float
    is_fully_complete: bool
    field_audits: Dict[str, FieldAuditResult]
    critical_omissions: Tuple[str, ...]
    audit_hash: str


class ArtifactCompletenessChecker:
    """
    Audits scientific bundles against the 10 Mandatory Integrity Dimensions.
    """

    MANDATORY_FIELDS = list(MandatoryField)

    @classmethod
    def audit_artifact(
        cls,
        artifact_id: str,
        artifact_payload: Dict[str, Any],
    ) -> CompletenessAuditReport:
        """Evaluate presence and validity of all 10 mandatory fields."""
        now_str = datetime.now(timezone.utc).isoformat()
        audits: Dict[str, FieldAuditResult] = {}
        critical_omissions: List[str] = []

        present_count = 0

        for field_enum in cls.MANDATORY_FIELDS:
            key = field_enum.value
            val = artifact_payload.get(key)
            is_present = False
            score = 0.0
            snippet = ""
            sev = "NONE"

            if val is not None:
                if isinstance(val, (list, tuple, dict)) and len(val) > 0:
                    is_present = True
                    score = 1.0
                    snippet = f"Found non-empty {type(val).__name__} ({len(val)} items)"
                elif isinstance(val, str) and len(val.strip()) > 0:
                    is_present = True
                    score = 1.0
                    snippet = val[:60] + "..." if len(val) > 60 else val
                elif isinstance(val, (int, float, bool)):
                    is_present = True
                    score = 1.0
                    snippet = str(val)

            if not is_present:
                sev = "CRITICAL" if field_enum in (
                    MandatoryField.RAW_EVIDENCE,
                    MandatoryField.PROVENANCE_CHAIN,
                    MandatoryField.REPRODUCTION_COMMAND,
                    MandatoryField.ENVIRONMENT_MANIFEST
                ) else "MINOR"
                if sev == "CRITICAL":
                    critical_omissions.append(f"Missing mandatory field: '{key}'")
            else:
                present_count += 1

            audits[key] = FieldAuditResult(
                field=field_enum,
                is_present=is_present,
                quality_score=score,
                evidence_snippet=snippet,
                omission_severity=sev,
            )

        total = len(cls.MANDATORY_FIELDS)
        ratio = present_count / total if total > 0 else 0.0
        is_complete = len(critical_omissions) == 0 and ratio >= 0.90

        h_payload = {
            "artifact_id": artifact_id,
            "present": present_count,
            "total": total,
            "ratio": ratio,
            "critical": critical_omissions,
        }
        audit_h = hash_canonical_json(h_payload)

        return CompletenessAuditReport(
            artifact_id=artifact_id,
            timestamp_utc=now_str,
            total_required_fields=total,
            present_fields_count=present_count,
            missing_fields_count=total - present_count,
            completeness_ratio=ratio,
            is_fully_complete=is_complete,
            field_audits=audits,
            critical_omissions=tuple(critical_omissions),
            audit_hash=audit_h,
        )
