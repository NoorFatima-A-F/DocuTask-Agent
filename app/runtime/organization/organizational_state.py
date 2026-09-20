"""
AMAEOP Pillar 1 - Organizational State Manager
Thread-safe real-time state tracking of departments, active missions, queues, and resource utilization.
"""

from typing import Dict, List, Any, Optional
import time
import threading
from app.runtime.organization.department import CANONICAL_DEPARTMENTS, Department


class OrganizationalStateManager:
    """Tracks dynamic enterprise state, department workloads, and active organizational metrics."""

    def __init__(self):
        self._lock = threading.RLock()
        self._departments: Dict[str, Department] = {k: v for k, v in CANONICAL_DEPARTMENTS.items()}
        self._mission_assignments: Dict[str, List[str]] = {
            "mission_live_001": ["dept_executive", "dept_ocr", "dept_extraction", "dept_validation", "dept_governance"],
            "mission_batch_100": ["dept_executive", "dept_ocr", "dept_extraction", "dept_qa"],
        }

    def get_department(self, department_id: str) -> Optional[Department]:
        with self._lock:
            return self._departments.get(department_id)

    def list_departments(self) -> List[Dict[str, Any]]:
        with self._lock:
            return [d.to_dict() for d in self._departments.values()]

    def update_department_metrics(
        self,
        department_id: str,
        queue_delta: int = 0,
        active_workers: Optional[int] = None,
        health_score: Optional[float] = None,
        budget_spent_delta: float = 0.0,
    ) -> Optional[Department]:
        with self._lock:
            if department_id not in self._departments:
                return None
            d = self._departments[department_id]
            d.queue_depth = max(0, d.queue_depth + queue_delta)
            if active_workers is not None:
                d.active_workers = min(d.concurrency_limit, max(0, active_workers))
            if health_score is not None:
                d.health_score = max(0.0, min(100.0, health_score))
            if budget_spent_delta != 0.0:
                d.budget_spent_usd = round(d.budget_spent_usd + budget_spent_delta, 4)
            d.updated_at = time.time()
            return d

    def get_organizational_kpis(self) -> Dict[str, Any]:
        with self._lock:
            depts = list(self._departments.values())
            avg_health = sum(d.health_score for d in depts) / len(depts)
            total_workers = sum(d.active_workers for d in depts)
            total_queue = sum(d.queue_depth for d in depts)
            total_budget = sum(d.budget_allocated_usd for d in depts)
            total_spent = sum(d.budget_spent_usd for d in depts)
            avg_sla = sum(d.kpis.sla_compliance_pct for d in depts) / len(depts)
            avg_acc = sum(d.kpis.accuracy_rate_pct for d in depts) / len(depts)

            return {
                "organization_health_index": round(avg_health, 2),
                "total_active_agents": total_workers,
                "total_queued_tasks": total_queue,
                "total_budget_allocated_usd": round(total_budget, 2),
                "total_budget_spent_usd": round(total_spent, 2),
                "budget_utilization_pct": round((total_spent / max(1.0, total_budget)) * 100, 1),
                "macro_sla_compliance_pct": round(avg_sla, 2),
                "macro_accuracy_rate_pct": round(avg_acc, 2),
                "active_missions_count": len(self._mission_assignments),
                "status": "HEALTHY_OPTIMAL" if avg_health >= 95.0 else "ELEVATED_LOAD",
            }


org_state_manager = OrganizationalStateManager()
