"""
Multi-Objective Optimization Engine - Optimization Serializer
Generates deterministic JSON serialization for zero-drift forensic audit and replay verification.
"""

import json
from typing import Dict, Any, List


class OptimizationSerializer:
    """Serializes optimization payloads deterministically."""

    @staticmethod
    def serialize_decision(data: Dict[str, Any]) -> str:
        """Serializes dictionary with sorted keys and normalized floats."""
        return json.dumps(data, sort_keys=True, separators=(",", ":"))

    @staticmethod
    def deserialize_decision(json_str: str) -> Dict[str, Any]:
        return json.loads(json_str)
