"""
Scientific Failure Memory (Phase 84C)
====================================
Tracks execution failures, instability, timeouts, and negative results
to prevent redundant flawed experiments.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional

from research_validation.provenance.hashing import hash_canonical_json


class FailureCategory(str, Enum):
    TIMEOUT = "TIMEOUT"
    OUT_OF_MEMORY = "OUT_OF_MEMORY"
    NUMERICAL_INSTABILITY = "NUMERICAL_INSTABILITY"
    DATASET_CORRUPTION = "DATASET_CORRUPTION"
    VALIDATION_CONFLICT = "VALIDATION_CONFLICT"
    ENVIRONMENT_INCOMPATIBILITY = "ENVIRONMENT_INCOMPATIBILITY"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


@dataclass(frozen=True)
class FailureMemoryEntry:
    """Historical record of an experimental failure."""
    failure_id: str
    experiment_id: str
    category: FailureCategory
    parameters: Dict[str, Any]
    error_message: str
    stack_trace_snippet: str
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    avoidance_weight: float = 1.0
    failure_digest_sha256: str = field(default="")


class FailureMemoryStore:
    """Store for indexing and pattern-matching historical experimental failures."""

    def __init__(self):
        self.failures: Dict[str, FailureMemoryEntry] = {}

    def record_failure(
        self,
        experiment_id: str,
        category: FailureCategory,
        parameters: Dict[str, Any],
        error_message: str,
        stack_trace_snippet: str = "",
        avoidance_weight: float = 1.0,
    ) -> FailureMemoryEntry:
        failure_id = f"fail_{category.value}_{len(self.failures)}"
        payload = {
            "failure_id": failure_id,
            "experiment_id": experiment_id,
            "category": category.value,
            "parameters": parameters,
            "error_message": error_message,
        }
        digest = hash_canonical_json(payload)

        entry = FailureMemoryEntry(
            failure_id=failure_id,
            experiment_id=experiment_id,
            category=category,
            parameters=parameters,
            error_message=error_message,
            stack_trace_snippet=stack_trace_snippet,
            avoidance_weight=avoidance_weight,
            failure_digest_sha256=digest,
        )
        self.failures[failure_id] = entry
        return entry

    def is_known_failure_configuration(self, candidate_parameters: Dict[str, Any]) -> Tuple[bool, Optional[FailureMemoryEntry]]:
        """Checks if a set of candidate parameters matches a known failure pattern."""
        for f in self.failures.values():
            # Check for exact parameter match or subset collision
            if f.parameters and all(candidate_parameters.get(k) == v for k, v in f.parameters.items() if k in candidate_parameters):
                return True, f
        return False, None
