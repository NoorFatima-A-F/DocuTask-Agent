"""Validation Registry for External Reality Checks and Verification Proofs."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ValidationAssertionRecord(BaseModel):
    """Immutable validation record stored in the registry."""
    record_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_system: str
    target_version: str
    assertion_type: str  # REALITY_CHECK, CONTRADICTION_ANALYSIS, AUDITOR_SIMULATION, DRIFT_CHECK, ERI_CALCULATION
    passed: bool
    score: Optional[float] = None
    summary: str
    payload: Dict[str, Any] = Field(default_factory=dict)


class ValidationRegistry:
    """Manages the persistence and retrieval of external validation records."""

    def __init__(self, registry_dir: Path):
        self.registry_dir = Path(registry_dir).resolve()
        self.registry_dir.mkdir(parents=True, exist_ok=True)
        self.registry_file = self.registry_dir / "validation_records.jsonl"

    def record_assertion(
        self,
        target_system: str,
        target_version: str,
        assertion_type: str,
        passed: bool,
        summary: str,
        score: Optional[float] = None,
        payload: Optional[Dict[str, Any]] = None,
    ) -> ValidationAssertionRecord:
        payload = payload or {}
        rec_id = f"VAL-{assertion_type[:4].upper()}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')[:17]}"
        rec = ValidationAssertionRecord(
            record_id=rec_id,
            target_system=target_system,
            target_version=target_version,
            assertion_type=assertion_type,
            passed=passed,
            score=score,
            summary=summary,
            payload=payload,
        )

        with open(self.registry_file, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(rec.model_dump(), sort_keys=True) + "\n")

        return rec

    def load_all_records(self) -> List[ValidationAssertionRecord]:
        if not self.registry_file.exists():
            return []
        records = []
        with open(self.registry_file, "r", encoding="utf-8") as fp:
            for line in fp:
                line = line.strip()
                if line:
                    records.append(ValidationAssertionRecord.model_validate(json.loads(line)))
        return records
