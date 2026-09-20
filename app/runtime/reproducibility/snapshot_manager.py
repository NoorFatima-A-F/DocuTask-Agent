"""Runtime Snapshot Manager.

Stores, retrieves, and diffs execution snapshots to verify environmental consistency.
"""

from __future__ import annotations

import collections
import time
from typing import Any, Dict, List, Optional

from app.runtime.reproducibility.environment_capture import EnvironmentCapture
from app.runtime.reproducibility.runtime_snapshot import RuntimeSnapshot


class SnapshotManager:
    def __init__(self):
        self._snapshots: Dict[str, RuntimeSnapshot] = {}
        self._snapshots_by_mission: Dict[str, List[str]] = collections.defaultdict(list)

    def create_snapshot(
        self,
        snapshot_id: str,
        mission_id: str,
        step_index: int,
        random_seed: int,
        model_configs: Dict[str, Any],
        dag_topology: Dict[str, Any],
        memory_state_digest: str,
        input_digest: str,
        output_digest: str,
    ) -> RuntimeSnapshot:
        env = EnvironmentCapture.capture_current()
        snap = RuntimeSnapshot(
            snapshot_id=snapshot_id,
            mission_id=mission_id,
            step_index=step_index,
            random_seed=random_seed,
            environment_fingerprint=env,
            model_configurations=model_configs,
            dag_topology=dag_topology,
            memory_state_digest=memory_state_digest,
            input_payload_digest=input_digest,
            recorded_output_digest=output_digest,
        )
        snap.seal()
        self._snapshots[snap.snapshot_id] = snap
        self._snapshots_by_mission[mission_id].append(snap.snapshot_id)
        return snap

    def get_snapshot(self, snapshot_id: str) -> Optional[RuntimeSnapshot]:
        return self._snapshots.get(snapshot_id)

    def list_snapshots(self) -> List[Dict[str, Any]]:
        return [s.to_dict() for s in self._snapshots.values()]

    def get_mission_snapshots(self, mission_id: str) -> List[RuntimeSnapshot]:
        s_ids = self._snapshots_by_mission.get(mission_id, [])
        return [self._snapshots[sid] for sid in s_ids if sid in self._snapshots]

    def diff_snapshots(self, snap_id_a: str, snap_id_b: str) -> Dict[str, Any]:
        a = self.get_snapshot(snap_id_a)
        b = self.get_snapshot(snap_id_b)
        if not a or not b:
            return {"error": "One or both snapshots not found"}

        return {
            "snapshot_a": snap_id_a,
            "snapshot_b": snap_id_b,
            "seed_match": a.random_seed == b.random_seed,
            "env_match": a.environment_fingerprint.environment_hash == b.environment_fingerprint.environment_hash,
            "input_match": a.input_payload_digest == b.input_payload_digest,
            "memory_match": a.memory_state_digest == b.memory_state_digest,
            "output_match": a.recorded_output_digest == b.recorded_output_digest,
            "model_configs_match": a.model_configurations == b.model_configurations,
            "is_identical": a.snapshot_hash == b.snapshot_hash,
        }

    def count(self) -> int:
        return len(self._snapshots)

    def clear(self) -> None:
        self._snapshots.clear()
        self._snapshots_by_mission.clear()


global_snapshot_manager = SnapshotManager()
