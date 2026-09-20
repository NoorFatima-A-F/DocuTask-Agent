"""
Scientific Feature Store - Feature Versioning
Provides cryptographic fingerprinting, schema versioning, and immutable snapshots.
"""

import hashlib
import json
from typing import Dict, Any, List
from datetime import datetime, timezone
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class FeatureSnapshot:
    version: str
    schema_hash: str
    timestamp_utc: str
    raw_features: Dict[str, float]
    normalized_features: Dict[str, float]
    context_id: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class FeatureVersionManager:
    """Manages schema hashing and creates immutable feature snapshots."""

    CURRENT_VERSION = "v1.4.0"

    @classmethod
    def compute_schema_hash(cls, feature_names: List[str]) -> str:
        """Computes SHA-256 fingerprint of feature signature."""
        sorted_names = sorted(feature_names)
        serialized = json.dumps(sorted_names, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()[:16]

    @classmethod
    def create_snapshot(
        cls,
        context_id: str,
        raw_features: Dict[str, float],
        normalized_features: Dict[str, float],
        version: str = CURRENT_VERSION,
    ) -> FeatureSnapshot:
        schema_hash = cls.compute_schema_hash(list(raw_features.keys()))
        return FeatureSnapshot(
            version=version,
            schema_hash=schema_hash,
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            raw_features=dict(raw_features),
            normalized_features=dict(normalized_features),
            context_id=context_id,
        )
