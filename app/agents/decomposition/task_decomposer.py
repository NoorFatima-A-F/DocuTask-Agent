"""
Enterprise Multi-Agent Intelligence Platform (EMAIP) - Task Decomposition Engine.
Transforms high-level business goals into ordered, executable plan steps with
capability matching, dependency graphing, and Phase 3 Workflow export.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import uuid
import logging

from app.agents.domain.agent_entity import AgentPlan, GoalModel, PlanStep
from app.workflows.domain.models import (
    TaskDefinition,
    TaskPriority,
    TaskType,
    WorkflowDefinition,
)

logger = logging.getLogger(__name__)


class TaskDecomposer:
    """
    Decomposes business goals into executable sub-tasks using Rule-Based,
    AI-Assisted, or Hybrid strategies.
    """

    # Standard decomposition templates for common enterprise patterns
    DECOMPOSITION_TEMPLATES: Dict[str, List[Dict[str, Any]]] = {
        "invoice_processing": [
            {
                "name": "validate_document",
                "description": "Validate document format, layout and integrity",
                "agent_type": "ValidationAgent",
                "skills": ["validation", "ocr"],
                "tools": ["schema_validator"],
                "cost": 0.005,
                "timeout": 30,
            },
            {
                "name": "extract_invoice_data",
                "description": "Extract structured fields from invoice",
                "agent_type": "ExecutionAgent",
                "skills": ["extraction"],
                "tools": ["document_parser"],
                "dependencies": ["validate_document"],
                "cost": 0.02,
                "timeout": 60,
            },
            {
                "name": "compliance_and_tax_check",
                "description": "Verify tax calculations and regulatory compliance",
                "agent_type": "ComplianceAgent",
                "skills": ["compliance", "analysis"],
                "tools": ["tax_rules_engine"],
                "dependencies": ["extract_invoice_data"],
                "cost": 0.01,
                "timeout": 45,
            },
            {
                "name": "manager_approval_if_needed",
                "description": "Escalate to manager if amount exceeds threshold",
                "agent_type": "HumanLiaisonAgent",
                "skills": ["scheduling"],
                "tools": ["approval_gateway"],
                "dependencies": ["compliance_and_tax_check"],
                "cost": 0.001,
                "timeout": 300,
                "requires_approval": True,
            },
            {
                "name": "accounting_ledger_export",
                "description": "Record transaction into ledger",
                "agent_type": "ExecutionAgent",
                "skills": ["transformation"],
                "tools": ["ledger_connector"],
                "dependencies": ["manager_approval_if_needed"],
                "compensation": "revert_ledger_entry",
                "cost": 0.005,
                "timeout": 30,
            },
        ],
        "contract_review": [
            {
                "name": "ocr_and_parse_contract",
                "description": "Extract text and section headings from contract",
                "agent_type": "ExecutionAgent",
                "skills": ["ocr", "extraction"],
                "tools": ["document_parser"],
                "cost": 0.02,
                "timeout": 60,
            },
            {
                "name": "clause_risk_analysis",
                "description": "Analyze liability, indemnification, and termination clauses",
                "agent_type": "LegalAgent",
                "skills": ["analysis", "compliance"],
                "tools": ["clause_risk_scorer"],
                "dependencies": ["ocr_and_parse_contract"],
                "cost": 0.05,
                "timeout": 90,
            },
            {
                "name": "critic_review_and_summary",
                "description": "Evaluate findings and generate executive summary",
                "agent_type": "CriticAgent",
                "skills": ["summarization", "validation"],
                "tools": ["summary_generator"],
                "dependencies": ["clause_risk_analysis"],
                "cost": 0.02,
                "timeout": 60,
            },
        ],
        "default_generic": [
            {
                "name": "analyze_requirements",
                "description": "Analyze input data and plan execution",
                "agent_type": "PlannerAgent",
                "skills": ["planning", "analysis"],
                "tools": ["context_analyzer"],
                "cost": 0.01,
                "timeout": 30,
            },
            {
                "name": "execute_task",
                "description": "Execute main capability logic",
                "agent_type": "ExecutionAgent",
                "skills": ["extraction", "transformation"],
                "tools": ["execution_worker"],
                "dependencies": ["analyze_requirements"],
                "cost": 0.03,
                "timeout": 60,
            },
            {
                "name": "verify_and_reflect",
                "description": "Validate result quality and self-reflect",
                "agent_type": "CriticAgent",
                "skills": ["validation"],
                "tools": ["quality_checker"],
                "dependencies": ["execute_task"],
                "cost": 0.01,
                "timeout": 30,
            },
        ]
    }

    def decompose(
        self,
        goal: GoalModel,
        strategy: str = "HYBRID",
        template_name: Optional[str] = None
    ) -> AgentPlan:
        """
        Decomposes a goal into an AgentPlan containing ordered PlanSteps with dependencies.
        """
        # Determine appropriate template
        desc_lower = goal.description.lower()
        if template_name and template_name in self.DECOMPOSITION_TEMPLATES:
            selected_template = self.DECOMPOSITION_TEMPLATES[template_name]
        elif "invoice" in desc_lower or "vendor" in desc_lower or "payment" in desc_lower:
            selected_template = self.DECOMPOSITION_TEMPLATES["invoice_processing"]
        elif "contract" in desc_lower or "legal" in desc_lower or "agreement" in desc_lower:
            selected_template = self.DECOMPOSITION_TEMPLATES["contract_review"]
        else:
            selected_template = self.DECOMPOSITION_TEMPLATES["default_generic"]

        steps: List[PlanStep] = []
        name_to_step_id: Dict[str, str] = {}
        dep_map: Dict[str, List[str]] = {}

        total_cost = 0.0
        total_duration = 0.0
        assigned_agents: set[str] = set()

        for item in selected_template:
            step_id = f"step-{uuid.uuid4().hex[:8]}"
            name_to_step_id[item["name"]] = step_id

            deps = [name_to_step_id[d] for d in item.get("dependencies", []) if d in name_to_step_id]
            dep_map[step_id] = deps

            cost = item.get("cost", 0.01)
            duration = item.get("timeout", 60)
            agent_type = item.get("agent_type", "ExecutionAgent")

            total_cost += cost
            total_duration += duration
            assigned_agents.add(agent_type)

            step = PlanStep(
                id=step_id,
                name=item["name"],
                description=item["description"],
                assigned_agent_type=agent_type,
                required_skills=item.get("skills", []),
                required_tools=item.get("tools", []),
                dependencies=deps,
                timeout_seconds=duration,
                estimated_cost_usd=cost,
                requires_human_approval=item.get("requires_approval", False),
                compensation_action=item.get("compensation"),
                status="PLANNED",
            )
            steps.append(step)

        # Risk scoring based on human approval and cost
        risk_score = 0.1
        if any(s.requires_human_approval for s in steps):
            risk_score += 0.3
        if total_cost > 0.1:
            risk_score += 0.2

        plan = AgentPlan(
            plan_id=f"plan-{uuid.uuid4().hex[:12]}",
            goal_id=goal.id,
            goal_description=goal.description,
            steps=steps,
            dependencies=dep_map,
            assigned_agents=list(assigned_agents),
            estimated_cost_usd=round(total_cost, 4),
            estimated_duration_seconds=total_duration,
            risk_score=round(risk_score, 2),
            strategy=strategy,
            status="READY",
        )

        logger.info(
            f"Decomposed goal '{goal.id}' into {len(steps)} steps via {strategy} strategy "
            f"[Est. Cost: ${plan.estimated_cost_usd}, Risk: {plan.risk_score}]"
        )
        return plan

    def to_workflow_definition(self, plan: AgentPlan, workflow_id: Optional[str] = None) -> WorkflowDefinition:
        """
        Converts an AgentPlan directly into a Phase 3 WorkflowDefinition, bridging
        Agent Cognition with Workflow Orchestration.
        """
        tasks: List[TaskDefinition] = []
        for step in plan.steps:
            # Map agent types to workflow task types
            t_type = TaskType.AI
            if step.requires_human_approval:
                t_type = TaskType.APPROVAL
            elif "transformation" in step.required_skills:
                t_type = TaskType.TRANSFORM
            elif "validation" in step.required_skills:
                t_type = TaskType.VALIDATION

            task_def = TaskDefinition(
                id=step.id,
                name=step.name,
                type=t_type,
                capability=step.required_skills[0] if step.required_skills else "execution",
                inputs={"description": step.description, "tools": step.required_tools},
                outputs={},
                priority=TaskPriority.HIGH if step.requires_human_approval else TaskPriority.NORMAL,
                timeout_seconds=step.timeout_seconds,
                compensation_action=step.compensation_action,
            )
            tasks.append(task_def)

        wf_id = workflow_id or f"wf-agent-{plan.plan_id}"
        return WorkflowDefinition(
            id=wf_id,
            name=f"WorkflowFor-{plan.goal_description[:30]}",
            version="1.0.0",
            description=f"Auto-compiled from AgentPlan {plan.plan_id} (Goal: {plan.goal_description})",
            tasks=tasks,
            variables={"goal_id": plan.goal_id, "plan_id": plan.plan_id},
        )
