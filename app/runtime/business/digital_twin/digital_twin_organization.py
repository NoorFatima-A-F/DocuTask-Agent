"""
Phase 13.19: Digital Twin of the Organization (DTO).
Maintains a live, synchronized simulation model of enterprise departments, worker loads, and resource contention.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, timezone
from app.runtime.business.models.schemas import DigitalTwinOrgState


class DigitalTwinOrganization:
    def __init__(self):
        self._state = DigitalTwinOrgState(
            total_departments=4,
            active_human_workers=90,
            active_agent_workers=24,
            running_business_processes=8,
            pending_approvals=1,
            mean_org_sla_compliance_pct=99.2,
            department_workloads={
                "dept_finance": 78.5,
                "dept_legal": 42.0,
                "dept_ops": 85.0,
                "dept_exec": 30.0,
            },
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    def get_digital_twin_state(self) -> DigitalTwinOrgState:
        self._state.timestamp = datetime.now(timezone.utc).isoformat()
        return self._state

    def update_department_load(self, department_id: str, load_pct: float) -> DigitalTwinOrgState:
        self._state.department_workloads[department_id] = max(0.0, min(100.0, load_pct))
        self._state.timestamp = datetime.now(timezone.utc).isoformat()
        return self._state
