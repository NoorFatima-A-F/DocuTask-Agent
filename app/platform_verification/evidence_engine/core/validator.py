"""
Evidence Validation Engine checking completeness, integrity, consistency, authenticity, and security.
"""
from __future__ import annotations
import hashlib
from typing import Any, Dict, List
from app.platform_verification.evidence_engine.domain.models import (
    EvidenceArtifact,
    ValidationReport,
)
from app.platform_verification.evidence_engine.domain.interfaces import IEvidenceValidator


class EvidenceValidationEngine(IEvidenceValidator):
    """Performs rigorous multi-facet validation on evidence artifacts before certification storage."""

    def validate_artifact(self, artifact: EvidenceArtifact, content: bytes) -> ValidationReport:
        issues: List[str] = []

        # 1. Integrity Check (SHA-256 Checksum)
        actual_hash = hashlib.sha256(content).hexdigest()
        integrity_verified = (actual_hash == artifact.checksum_sha256)
        if not integrity_verified:
            issues.append(f"Integrity check failed: expected checksum {artifact.checksum_sha256}, got {actual_hash}")

        # 2. Completeness Check
        completeness = bool(artifact.artifact_id and artifact.execution_id and artifact.category)
        if not completeness:
            issues.append("Artifact missing essential metadata attributes")

        # 3. Consistency Check
        consistency = bool(artifact.storage_uri.startswith("cas://sha256/"))
        if not consistency:
            issues.append("Storage URI format does not conform to CAS address scheme")

        # 4. Authenticity Check
        authenticity = bool(artifact.producer)
        if not authenticity:
            issues.append("Artifact producer is undefined")

        # 5. Security Scan (check for unencrypted private credentials in metadata)
        security_passed = True
        for k, v in artifact.metadata.items():
            if any(term in str(k).lower() or term in str(v).lower() for term in ["private_key", "password", "secret_token"]):
                security_passed = False
                issues.append(f"Security violation: unmasked secret detected in metadata key '{k}'")

        is_valid = integrity_verified and completeness and consistency and authenticity and security_passed

        return ValidationReport(
            is_valid=is_valid,
            completeness=completeness,
            integrity_verified=integrity_verified,
            consistency=consistency,
            authenticity=authenticity,
            security_passed=security_passed,
            issues=issues,
        )
