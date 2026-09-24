"""
Master Execution Platform Runtime for Phase 13.15.
Coordinates all cyber-physical and real-world execution subsystems, policy validation, simulation, and multi-runtime bridges.
"""

from typing import Any, Dict

from app.runtime.execution.audit.audit_engine import audit_engine
from app.runtime.execution.browser.browser_engine import browser_engine
from app.runtime.execution.connectors.connector_engine import connector_engine
from app.runtime.execution.credential.credential_engine import credential_engine
from app.runtime.execution.events.execution_events import (
    MissionStatus,
    execution_event_bus,
)
from app.runtime.execution.execution.execution_engine import execution_engine
from app.runtime.execution.monitoring.monitoring_engine import monitoring_engine
from app.runtime.execution.planner.execution_planner import execution_planner
from app.runtime.execution.policy.policy_engine import policy_engine
from app.runtime.execution.rollback.rollback_engine import rollback_engine
from app.runtime.execution.simulation.execution_simulation import execution_simulation_engine
from app.runtime.execution.tool_registry.tool_registry_engine import tool_registry_engine
from app.runtime.execution.workflow.workflow_engine import workflow_engine


class ExecutionRuntime:
    """Master Coordinator for Autonomous Real-World Execution (ARWE-UTOCOP)."""

    def __init__(self):
        self.tool_registry = tool_registry_engine
        self.connectors = connector_engine
        self.browser = browser_engine
        self.workflow = workflow_engine
        self.planner = execution_planner
        self.credentials = credential_engine
        self.policy = policy_engine
        self.simulation = execution_simulation_engine
        self.execution = execution_engine
        self.verification = None  # Loaded lazily or via verification_engine
        self.rollback = rollback_engine
        self.monitoring = monitoring_engine
        self.audit = audit_engine
        self.event_bus = execution_event_bus

    def execute_goal_end_to_end(
        self,
        goal: str,
        dry_run: bool = False,
        initiated_by: str = "autonomous_org_director",
    ) -> Dict[str, Any]:
        """Full end-to-end execution of a natural language goal through the Core Invariant pipeline."""
        # 1. Plan goal into Workflow + CPM Critical Path
        wf, plan = self.planner.plan_mission(goal)
        self.workflow.register_workflow(wf)

        # 2. Instantiate Mission
        mission = self.execution.create_mission(goal=goal, workflow=wf, initiated_by=initiated_by)

        # 3. Simulate and/or Execute
        sim_report = self.simulation.simulate_workflow(wf)
        executed_mission = self.execution.execute_mission(mission.mission_id, dry_run=dry_run)

        return {
            "mission_id": executed_mission.mission_id,
            "goal": goal,
            "status": executed_mission.status.value if isinstance(executed_mission.status, MissionStatus) else str(executed_mission.status),
            "plan_id": plan.plan_id,
            "simulation_id": sim_report.simulation_id,
            "critical_path_steps": plan.critical_path_steps,
            "total_execution_time_ms": executed_mission.total_execution_time_ms,
            "steps_executed": len(executed_mission.steps),
            "audit_trail_valid": self.audit.verify_ledger_integrity()[0],
            "mission": executed_mission.to_dict(),
        }

    def get_executive_overview(self) -> Dict[str, Any]:
        """Provides a consolidated dashboard summary of the entire execution platform."""
        tools_stats = self.tool_registry.get_stats()
        conn_stats = self.connectors.get_summary()
        telemetry = self.monitoring.get_telemetry_snapshot()
        missions = self.execution.list_missions()
        plans = self.planner.list_plans()
        rules = self.policy.list_rules()
        approvals = self.policy.list_approvals()
        rollbacks = self.rollback.list_rollbacks()
        browser_sessions = self.browser.list_sessions()
        audit_valid, _ = self.audit.verify_ledger_integrity()

        return {
            "system_status": "OPERATIONAL",
            "autonomous_mode": "ACTIVE_GOVERNED",
            "total_tools": tools_stats["total_tools"],
            "active_tools": tools_stats["active_tools"],
            "total_connectors": conn_stats["total_connectors"],
            "connected_count": conn_stats["connected_count"],
            "total_missions": len(missions),
            "completed_missions": sum(1 for m in missions if m.status == MissionStatus.COMPLETED),
            "failed_missions": sum(1 for m in missions if m.status in [MissionStatus.FAILED, MissionStatus.ROLLED_BACK]),
            "active_browser_sessions": len(browser_sessions),
            "total_plans": len(plans),
            "active_policy_rules": len(rules),
            "pending_approvals": sum(1 for a in approvals if a.status == "pending"),
            "total_rollbacks": len(rollbacks),
            "audit_ledger_integrity": audit_valid,
            "telemetry": telemetry.to_dict(),
        }


# Global Runtime Singleton
execution_runtime = ExecutionRuntime()
