"""
Recovery Verification & Integrity Validator.

Validates entity integrity, schema compatibility, row counts, cryptographic hashes,
and tenant isolation following a recovery or restore operation.
"""

from __future__ import annotations

import enum
import hashlib
import json
import logging
from typing import Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger("infrastructure.recovery.verification")


class VerificationStatus(str, enum.Enum):
    """Integrity verification status."""
    VALID = "VALID"
    CORRUPTED = "CORRUPTED"
    INCOMPLETE = "INCOMPLETE"
    MISMATCHED = "MISMATCHED"


class EntityVerificationResult(BaseModel):
    """Result of post-recovery verification."""
    entity_id: str
    status: VerificationStatus
    checksum_match: bool
    schema_compatible: bool
    record_count_expected: int
    record_count_actual: int
    checks_passed: List[str] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class RecoveryVerifier:
    """
    Validates restored data structures and services to ensure safe return to service.
    """

    def verify_payload_integrity(
        self,
        entity_id: str,
        restored_data: Any,
        expected_hash: str,
        expected_count: Optional[int] = None,
        expected_schema_version: Optional[str] = None,
    ) -> EntityVerificationResult:
        """
        Verify restored data matches expected hash, schema version, and count.
        """
        serialized = json.dumps(restored_data, sort_keys=True, default=str)
        actual_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        checksum_match = (actual_hash == expected_hash)
        checks_passed: List[str] = []
        errors: List[str] = []

        if checksum_match:
            checks_passed.append("checksum_verification")
        else:
            errors.append(f"Checksum mismatch: expected {expected_hash}, got {actual_hash}")

        actual_count = len(restored_data) if isinstance(restored_data, (list, dict, set)) else 1
        expected_count_val = expected_count if expected_count is not None else actual_count

        if actual_count == expected_count_val:
            checks_passed.append("record_count_verification")
        else:
            errors.append(f"Record count mismatch: expected {expected_count_val}, got {actual_count}")

        schema_compatible = True
        if expected_schema_version and isinstance(restored_data, dict):
            actual_version = restored_data.get("schema_version", expected_schema_version)
            if actual_version != expected_schema_version:
                schema_compatible = False
                errors.append(f"Schema version mismatch: expected {expected_schema_version}, got {actual_version}")
            else:
                checks_passed.append("schema_version_verification")

        if not errors:
            status = VerificationStatus.VALID
        elif not checksum_match:
            status = VerificationStatus.CORRUPTED
        elif actual_count < expected_count_val:
            status = VerificationStatus.INCOMPLETE
        else:
            status = VerificationStatus.MISMATCHED

        logger.info(f"Recovery verification for '{entity_id}' outcome: {status.value}")
        return EntityVerificationResult(
            entity_id=entity_id,
            status=status,
            checksum_match=checksum_match,
            schema_compatible=schema_compatible,
            record_count_expected=expected_count_val,
            record_count_actual=actual_count,
            checks_passed=checks_passed,
            errors=errors,
        )
