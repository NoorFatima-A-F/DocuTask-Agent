"""
Experience Extractor for Phase 10 (AISLCOP).

Synthesizes execution DAG events, reflection logs, and telemetry into cryptographically
verifiable ExperienceRecords.
"""

from __future__ import annotations

import hashlib
import time
import uuid
from typing import Any, Dict, List, Optional

from app.runtime.intelligence.experience.experience_record import (
    ExperienceRecord,
    ExperienceStore,
    ToolTraceRecord,
)


class ExperienceExtractor:
    """
    Extracts structured operational experience from runtime telemetry and execution DAGs.
    """

    def __init__(self, store: Optional[ExperienceStore] = None):
        self.store = store or ExperienceStore()

    def extract_from_mission(
        self,
        mission_id: str,
        document_type: str,
        task_type: str,
        telemetry: Dict[str, Any],
        dag_info: Optional[Dict[str, Any]] = None,
        tool_traces: Optional[List[Dict[str, Any]]] = None,
        evidence_root_hash: str = "",
        status: str = "SUCCESS",
    ) -> ExperienceRecord:
        """
        Synthesizes a completed mission into a formal ExperienceRecord.
        """
        dag = dag_info or {}
        traces: List[ToolTraceRecord] = []
        for t in tool_traces or []:
            traces.append(
                ToolTraceRecord(
                    tool_name=t.get("tool_name", "unknown_tool"),
                    invocations=t.get("invocations", 1),
                    total_latency_ms=t.get("total_latency_ms", 100.0),
                    total_cost_usd=t.get("total_cost_usd", 0.001),
                    success_rate=t.get("success_rate", 1.0),
                    error_count=t.get("error_count", 0),
                )
            )

        experience_id = f"exp_{uuid.uuid4().hex[:12]}"
        
        # Calculate DAG topology hash if available
        dag_nodes = dag.get("nodes", ["plan", "execute", "validate"])
        dag_topology_hash = hashlib.sha256(str(dag_nodes).encode("utf-8")).hexdigest()

        init_conf = telemetry.get("initial_confidence", 0.85)
        final_conf = telemetry.get("final_confidence", 0.95)

        record = ExperienceRecord(
            experience_id=experience_id,
            mission_id=mission_id,
            document_type=document_type,
            task_type=task_type,
            timestamp=time.time(),
            status=status,
            planner_version=telemetry.get("planner_version", "v1.0.0"),
            dag_depth=dag.get("depth", len(dag_nodes)),
            dag_node_count=dag.get("node_count", len(dag_nodes)),
            dag_topology_hash=dag_topology_hash,
            total_latency_ms=telemetry.get("total_latency_ms", 1150.0),
            total_cost_usd=telemetry.get("total_cost_usd", 0.015),
            energy_joules=telemetry.get("energy_joules", 3.8),
            retries_count=telemetry.get("retries_count", 0),
            validation_failures_count=telemetry.get("validation_failures_count", 0),
            recovery_paths_used=telemetry.get("recovery_paths_used", []),
            human_corrections_count=telemetry.get("human_corrections_count", 0),
            initial_confidence=init_conf,
            final_confidence=final_conf,
            confidence_delta=round(final_conf - init_conf, 4),
            tool_traces=traces,
            memory_retrievals=telemetry.get("memory_retrievals", 3),
            memory_cache_hit_rate=telemetry.get("memory_cache_hit_rate", 0.80),
            organizational_department=telemetry.get("department", "Financial Operations"),
            participating_agents=telemetry.get("agents", ["ChiefPlanner", "WorkerAgent", "QualityAssurance"]),
            evidence_root_hash=evidence_root_hash or hashlib.sha256(mission_id.encode("utf-8")).hexdigest(),
        )

        self.store.append(record)
        return record
