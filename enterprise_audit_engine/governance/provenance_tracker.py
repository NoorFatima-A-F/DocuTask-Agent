"""Audit Provenance & Chain of Custody Tracker."""

import hashlib
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from ..domain.evidence.models import EvidenceRecord, AuditRunMetadata


class ProvenanceTracker:
    """Maintains immutable lineage from raw execution traces to finalized audit reports."""

    def __init__(self, run_metadata: AuditRunMetadata):
        self.run_metadata = run_metadata
        self.lineage_graph: List[Dict[str, Any]] = []

    def record_step(
        self,
        step_name: str,
        input_artifact: Optional[str],
        output_evidence_id: str,
        command_executed: Optional[str] = None,
        duration_ms: float = 0.0,
    ) -> Dict[str, Any]:
        """Records an immutable step in the evidence chain of custody."""
        step_entry = {
            "step_id": f"STEP-{len(self.lineage_graph) + 1:04d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step_name": step_name,
            "input_artifact": input_artifact,
            "output_evidence_id": output_evidence_id,
            "command_executed": command_executed,
            "duration_ms": duration_ms,
            "git_commit": self.run_metadata.git_commit_hash,
        }
        self.lineage_graph.append(step_entry)
        return step_entry

    def export_provenance_manifest(self) -> Dict[str, Any]:
        """Exports the complete verified provenance manifest."""
        serialized = json.dumps(self.lineage_graph, sort_keys=True)
        manifest_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
        return {
            "run_id": self.run_metadata.run_id,
            "metadata": self.run_metadata.model_dump(),
            "lineage_steps_count": len(self.lineage_graph),
            "lineage_steps": self.lineage_graph,
            "provenance_chain_hash": manifest_hash,
        }
