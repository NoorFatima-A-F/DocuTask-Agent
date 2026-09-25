"""
Outcome Verification Engine - Outcome Serializer
Generates deterministic JSON serialization for audit logs and forensic verification.
"""

import json
from typing import Dict, Any
from app.runtime.outcomes.outcome_collector import MissionOutcomeRecord


class OutcomeSerializer:
    """Serializes outcome records deterministically."""

    @staticmethod
    def serialize(record: MissionOutcomeRecord) -> str:
        return json.dumps(record.to_dict(), sort_keys=True, separators=(",", ":"))

    @staticmethod
    def deserialize(json_str: str) -> Dict[str, Any]:
        return json.loads(json_str)
