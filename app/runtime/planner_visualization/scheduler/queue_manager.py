"""
Queue Manager for Phase 13.2.
Manages multi-state runtime queues (WAITING, RUNNING, BLOCKED, RETRY, RECOVERY, COMPLETED, FAILED).
"""

from __future__ import annotations

from typing import Any, Dict, List
from app.runtime.planner_visualization.ui_models.models import TaskExecutionState


class RuntimeQueueManager:
    """
    Categorizes tasks across the 7 execution queue states.
    """

    def __init__(self, mission_id: str = "mission-001"):
        self.mission_id = mission_id

    def get_queues(self) -> Dict[str, Any]:
        queues = {
            "WAITING": [
                {"task_id": "node_extract_schema", "name": "Extract Financial Schema", "priority": 1, "queue_duration_ms": 12.0},
                {"task_id": "node_validate_invariants", "name": "Scientific Validation Check", "priority": 1, "queue_duration_ms": 5.0},
                {"task_id": "node_barrier_governance", "name": "Governance Sync Barrier", "priority": 2, "queue_duration_ms": 0.0},
                {"task_id": "node_join_finalize", "name": "Join & Truth Ledger Commit", "priority": 3, "queue_duration_ms": 0.0},
            ],
            "RUNNING": [
                {"task_id": "node_merge_ocr", "name": "Merge OCR Texts", "worker_id": "worker-extract-01", "elapsed_ms": 35.0},
            ],
            "BLOCKED": [],
            "RETRY": [],
            "RECOVERY": [],
            "COMPLETED": [
                {"task_id": "node_goal_ingress", "name": "Mission Goal Ingress", "duration_ms": 42.0},
                {"task_id": "node_split_ocr", "name": "Split OCR Chunks", "duration_ms": 28.0},
                {"task_id": "node_ocr_chunk_1", "name": "OCR Page 1-2 (Raster)", "duration_ms": 175.0},
                {"task_id": "node_ocr_chunk_2", "name": "OCR Page 3-4 (Tables)", "duration_ms": 205.0},
            ],
            "FAILED": [],
        }

        counts = {k: len(v) for k, v in queues.items()}
        return {
            "mission_id": self.mission_id,
            "counts": counts,
            "queues": queues,
            "total_tasks": sum(counts.values()),
        }
