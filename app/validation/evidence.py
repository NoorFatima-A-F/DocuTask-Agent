"""
Evidence Logger & Artifact Persistence Module.
Logs structured, verifiable audit evidence with SHA-256 cryptographic hash chaining.
"""

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict
from app.core.logging import logger
from app.validation.schemas import EvidenceRecord, MetricEvaluationResult


class EvidenceLogger:
    """Logger creating persistent, auditable, and cryptographically tamper-evident evidence artifacts."""

    EVIDENCE_DIR = Path("docs/audits/evidence")
    _last_hash: str = "GENESIS_HASH"

    @classmethod
    def compute_record_hash(cls, payload_dict: Dict[str, Any], prev_hash: str) -> str:
        """Computes SHA-256 digest over payload content and previous hash in chain."""
        canonical_json = json.dumps(payload_dict, sort_keys=True, default=str)
        hash_input = f"{prev_hash}:{canonical_json}"
        return hashlib.sha256(hash_input.encode("utf-8")).hexdigest()

    @classmethod
    def log_evidence(
        cls,
        input_artifact: str,
        expected_behavior: Dict[str, Any],
        actual_behavior: Dict[str, Any],
        metrics: MetricEvaluationResult,
        model_version: str = "gemini-1.5-flash",
        test_id_prefix: str = "val"
    ) -> EvidenceRecord:
        """
        Creates and persists a structured evidence record to disk with SHA-256 hash chaining.
        """
        cls.EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

        pass_fail = "PASS" if metrics.field_accuracy >= 0.80 else "FAIL"
        evidence_filename = f"{test_id_prefix}_{metrics.total_fields}f_{int(metrics.field_accuracy * 100)}acc.json"
        evidence_path = cls.EVIDENCE_DIR / evidence_filename

        payload = {
            "input_artifact": input_artifact,
            "expected_behavior": expected_behavior,
            "actual_behavior": actual_behavior,
            "metrics": metrics.model_dump(),
            "pass_fail": pass_fail,
            "model_version": model_version
        }

        # Compute SHA-256 Hash Chain
        curr_hash = cls.compute_record_hash(payload, cls._last_hash)

        record = EvidenceRecord(
            model_version=model_version,
            input_artifact=input_artifact,
            expected_behavior=expected_behavior,
            actual_behavior=actual_behavior,
            metrics=metrics,
            pass_fail=pass_fail,
            evidence_location=str(evidence_path),
            result_hash=curr_hash,
            previous_hash=cls._last_hash
        )

        cls._last_hash = curr_hash

        # Persist JSON evidence artifact
        try:
            with open(evidence_path, "w", encoding="utf-8") as f:
                f.write(record.model_dump_json(indent=2))
            logger.info(f"Logged validation evidence artifact to '{evidence_path}' (Hash={curr_hash[:10]}...)")
        except Exception as exc:
            logger.error(f"Failed to write evidence artifact: {str(exc)}")

        return record
