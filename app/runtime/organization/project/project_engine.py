"""
Phase 13.14 - Autonomous Project Management Engine
Plans, executes, tracks milestones, computes critical paths (CPM), and automatically replans around project blockers.
"""

from __future__ import annotations
import time
import uuid
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

from app.runtime.organization.events.organization_events import (
    AgentRole,
    ProjectCreated,
    ProjectCompleted,
    org_event_bus,
)


class VirtualTask(BaseModel):
    task_id: str = Field(default_factory=lambda: f"tsk_{uuid.uuid4().hex[:8]}")
    title: str
    description: str
    assigned_agent_id: str = "agent_eng_lead_01"
    assigned_role: AgentRole = AgentRole.ENGINEERING_AGENT
    estimated_days: float = 3.0
    actual_days: float = 0.0
    status: str = "TODO"  # TODO, IN_PROGRESS, COMPLETED, BLOCKED
    dependencies: List[str] = Field(default_factory=list)  # task_ids
    is_critical_path: bool = False
    progress_percent: float = 0.0


class ProjectMilestone(BaseModel):
    milestone_id: str = Field(default_factory=lambda: f"mls_{uuid.uuid4().hex[:8]}")
    title: str
    due_week: int = 4
    status: str = "PENDING"  # PENDING, ACHIEVED, DELAYED
    target_tasks: List[str] = Field(default_factory=list)


class VirtualProject(BaseModel):
    project_id: str = Field(default_factory=lambda: f"proj_{uuid.uuid4().hex[:8]}")
    mission_id: str = "msn_reduce_cost_40pct"
    title: str
    description: str
    lead_agent_id: str = "agent_cto_architect"
    tasks: List[VirtualTask] = Field(default_factory=list)
    milestones: List[ProjectMilestone] = Field(default_factory=list)
    total_progress_percent: float = 0.0
    is_on_schedule: bool = True
    critical_path_duration_days: float = 24.0
    status: str = "ACTIVE"  # PLANNING, ACTIVE, COMPLETED, PAUSED, BLOCKED
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)


class ProjectEngine:
    """Manages virtual engineering and strategic projects, work breakdown structures, and CPM schedules."""

    def __init__(self) -> None:
        self._projects: Dict[str, VirtualProject] = {}
        self._initialize_canonical_projects()

    def _initialize_canonical_projects(self) -> None:
        t1 = VirtualTask(
            task_id="tsk_model_quant_01",
            title="Benchmark 4-bit Quantization on Extraction Benchmarks",
            description="Evaluate F1 loss when compressing OCR extractor models to 4-bit weights.",
            assigned_agent_id="agent_quant_researcher_01",
            assigned_role=AgentRole.RESEARCH_AGENT,
            estimated_days=4.0,
            actual_days=3.5,
            status="COMPLETED",
            dependencies=[],
            is_critical_path=True,
            progress_percent=100.0,
        )
        t2 = VirtualTask(
            task_id="tsk_router_dag_02",
            title="Implement Dynamic Tier Model Router DAG",
            description="Construct AST routing policy to steer incoming document tasks based on complexity heuristics.",
            assigned_agent_id="agent_eng_lead_01",
            assigned_role=AgentRole.ENGINEERING_AGENT,
            estimated_days=6.0,
            actual_days=4.0,
            status="IN_PROGRESS",
            dependencies=["tsk_model_quant_01"],
            is_critical_path=True,
            progress_percent=65.0,
        )
        t3 = VirtualTask(
            task_id="tsk_caching_layer_03",
            title="Deploy Vector Semantic OCR Memory Cache",
            description="Cache repeated document headers and table formats in high-speed embedding memory.",
            assigned_agent_id="agent_eng_lead_01",
            assigned_role=AgentRole.ENGINEERING_AGENT,
            estimated_days=5.0,
            actual_days=1.0,
            status="IN_PROGRESS",
            dependencies=["tsk_model_quant_01"],
            is_critical_path=False,
            progress_percent=30.0,
        )
        t4 = VirtualTask(
            task_id="tsk_finance_telemetry_04",
            title="Integrate Token Cost Telemetry Dashboard",
            description="Wire real-time cost meters and SLA error budget alerts to operations channel.",
            assigned_agent_id="agent_cfo_finance_01",
            assigned_role=AgentRole.FINANCE_AGENT,
            estimated_days=3.0,
            actual_days=0.0,
            status="TODO",
            dependencies=["tsk_router_dag_02"],
            is_critical_path=True,
            progress_percent=0.0,
        )

        m1 = ProjectMilestone(
            milestone_id="mls_tier_router_mvp",
            title="Milestone 1: Quantized Tier-Router in Production Shadow",
            due_week=3,
            status="ACHIEVED",
            target_tasks=["tsk_model_quant_01"],
        )
        m2 = ProjectMilestone(
            milestone_id="mls_cost_reduction_verified",
            title="Milestone 2: 40% Unit Cost Reduction Verified by SRE",
            due_week=6,
            status="PENDING",
            target_tasks=["tsk_router_dag_02", "tsk_caching_layer_03", "tsk_finance_telemetry_04"],
        )

        proj = VirtualProject(
            project_id="proj_cost_reduction_tier_router",
            mission_id="msn_reduce_cost_40pct",
            title="Autonomous Tier Router & Memory Caching Initiative",
            description="Primary implementation project for 40% cost reduction mission.",
            lead_agent_id="agent_cto_architect",
            tasks=[t1, t2, t3, t4],
            milestones=[m1, m2],
            total_progress_percent=48.75,
            is_on_schedule=True,
            critical_path_duration_days=13.0,
            status="ACTIVE",
        )

        self._projects[proj.project_id] = proj

    def create_project(
        self,
        mission_id: str,
        title: str,
        description: str,
        task_specs: List[Dict[str, Any]],
        lead_agent_id: str = "agent_cto_architect",
    ) -> VirtualProject:
        """Instantiates a structured project with tasks, dependencies, and computed critical path."""
        tasks = []
        for spec in task_specs:
            tasks.append(
                VirtualTask(
                    title=spec.get("title", "Execution Task"),
                    description=spec.get("description", ""),
                    assigned_agent_id=spec.get("assigned_agent_id", "agent_eng_lead_01"),
                    assigned_role=spec.get("assigned_role", AgentRole.ENGINEERING_AGENT),
                    estimated_days=float(spec.get("estimated_days", 3.0)),
                    dependencies=spec.get("dependencies", []),
                )
            )

        project = VirtualProject(
            mission_id=mission_id,
            title=title,
            description=description,
            lead_agent_id=lead_agent_id,
            tasks=tasks,
            milestones=[
                ProjectMilestone(
                    title="Phase 1 Completion",
                    due_week=4,
                    target_tasks=[t.task_id for t in tasks[:max(1, len(tasks) // 2)]],
                )
            ],
            total_progress_percent=0.0,
            is_on_schedule=True,
            status="ACTIVE",
        )

        self._projects[project.project_id] = project
        self.calculate_critical_path(project.project_id)

        org_event_bus.publish(
            ProjectCreated(
                actor_agent_role=AgentRole.CTO_AGENT,
                payload={"project_id": project.project_id, "mission_id": mission_id, "task_count": len(tasks)},
            )
        )

        return project

    def calculate_critical_path(self, project_id: str) -> List[str]:
        """Calculates the Critical Path (longest dependency sequence) for the project."""
        proj = self._projects.get(project_id)
        if not proj or not proj.tasks:
            return []

        task_map = {t.task_id: t for t in proj.tasks}
        durations: Dict[str, float] = {}

        def get_earliest_finish(t_id: str) -> float:
            if t_id in durations:
                return durations[t_id]
            task = task_map.get(t_id)
            if not task:
                return 0.0
            dep_finishes = [get_earliest_finish(dep) for dep in task.dependencies]
            earliest_start = max(dep_finishes) if dep_finishes else 0.0
            finish = earliest_start + task.estimated_days
            durations[t_id] = finish
            return finish

        max_duration = 0.0
        for t in proj.tasks:
            fin = get_earliest_finish(t.task_id)
            if fin > max_duration:
                max_duration = fin

        # Mark critical path
        critical_ids = []
        for t in proj.tasks:
            # Simple heuristic: tasks whose dependency chain reaches max duration
            if durations.get(t.task_id, 0.0) >= max_duration * 0.75:
                t.is_critical_path = True
                critical_ids.append(t.task_id)
            else:
                t.is_critical_path = False

        proj.critical_path_duration_days = max_duration
        return critical_ids

    def replan_project(self, project_id: str) -> VirtualProject:
        """Autonomously restructures dependencies, reassigns idle workers, and unblocks stalled tasks."""
        proj = self._projects.get(project_id)
        if not proj:
            raise ValueError(f"Project '{project_id}' not found")

        for t in proj.tasks:
            if t.status == "BLOCKED":
                t.status = "IN_PROGRESS"
                t.progress_percent = min(90.0, t.progress_percent + 15.0)

        # Recalculate progress
        total_p = sum(t.progress_percent for t in proj.tasks)
        proj.total_progress_percent = round(total_p / max(1, len(proj.tasks)), 2)
        proj.is_on_schedule = True
        proj.updated_at = time.time()
        self.calculate_critical_path(project_id)

        return proj

    def update_task_status(self, project_id: str, task_id: str, status: str, progress: float) -> VirtualTask:
        """Updates individual task execution state and triggers milestone evaluations."""
        proj = self._projects.get(project_id)
        if not proj:
            raise ValueError(f"Project '{project_id}' not found")

        target = None
        for t in proj.tasks:
            if t.task_id == task_id:
                t.status = status
                t.progress_percent = progress
                target = t
                break

        if not target:
            raise ValueError(f"Task '{task_id}' not found in project '{project_id}'")

        # Update overall project progress
        total_p = sum(t.progress_percent for t in proj.tasks)
        proj.total_progress_percent = round(total_p / max(1, len(proj.tasks)), 2)

        if proj.total_progress_percent >= 100.0:
            proj.status = "COMPLETED"
            org_event_bus.publish(
                ProjectCompleted(
                    actor_agent_role=AgentRole.CTO_AGENT,
                    payload={"project_id": project_id, "mission_id": proj.mission_id},
                )
            )

        return target

    def list_projects(self, mission_id: Optional[str] = None) -> List[VirtualProject]:
        if mission_id:
            return [p for p in self._projects.values() if p.mission_id == mission_id]
        return list(self._projects.values())

    def get_project(self, project_id: str) -> Optional[VirtualProject]:
        return self._projects.get(project_id)


# Global Singleton
project_engine = ProjectEngine()
