"""Runtime Execution Snapshot.

Captures complete deterministic state snapshots of execution tasks, RNG seeds,
DAG topologies, parameter configurations, and memory states.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from app.runtime.reproducibility.environment_capture import (
    EnvironmentCapture,
    EnvironmentFingerprint,
)


@dataclass
class RuntimeSnapshot:
    snapshot_id: str
    mission_id: str
    step_index: int
    random_seed: int
    environment_fingerprint: EnvironmentFingerprint
    model_configurations: Dict[str, Any]
    dag_topology: Dict[str, Any]
    memory_state_digest: str
    input_payload_digest: str
    recorded_output_digest: str
    snapshot_hash: str = ""
    timestamp: float = field(default_factory=time.time)

    def compute_hash(self) -> str:
        payload = {
            "snapshot_id": self.snapshot_id,
            "mission_id": self.mission_id,
            "step_index": self.step_index,
            "random_seed": self.random_seed,
            "environment_hash": self.environment_fingerprint.environment_hash,
            "model_configurations": self.model_configurations,
            "dag_topology": self.dag_topology,
            "memory_state_digest": self.memory_state_digest,
            "input_payload_digest": self.input_payload_digest,
            "recorded_output_digest": self.recorded_output_digest,
        }
        serialized = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def seal(self) -> RuntimeSnapshot:
        self.snapshot_hash = self.compute_hash()
        return self

    def to_dict(self) -> Dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "mission_id": self.mission_id,
            "step_index": self.step_index,
            "random_seed": self.random_seed,
            "environment_fingerprint": self.environment_fingerprint.to_dict(),
            "model_configurations": self.model_configurations,
            "dag_topology": self.dag_topology,
            "memory_state_digest": self.memory_state_digest,
            "input_payload_digest": self.input_payload_digest,
            "recorded_output_digest": self.recorded_output_digest,
            "snapshot_hash": self.snapshot_hash,
            "timestamp_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(self.timestamp)),
        }
