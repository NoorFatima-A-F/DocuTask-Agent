"""
Tests for Goal Management, Task Decomposition, Planning Engine, and Workflow Export.
"""

from app.agents.decomposition.task_decomposer import TaskDecomposer
from app.agents.domain.agent_entity import Agent, AgentType, GoalModel
from app.agents.goals.goal_manager import GoalManager
from app.agents.planning.planning_engine import PlanningEngine
from app.agents.registry.agent_registry import AgentRegistry


def test_goal_hierarchy_and_management():
    manager = GoalManager()

    parent = manager.create_goal(
        description="Process Quarter 3 Vendor Invoices",
        priority="HIGH",
        budget={"max_cost_usd": 2.0},
        success_conditions=["All invoices extracted", "Ledger updated"],
    )
    assert parent.id.startswith("goal-")

    subgoal1 = manager.add_subgoal(
        parent_goal_id=parent.id,
        description="Extract and validate vendor line items",
    )
    subgoal2 = manager.add_subgoal(
        parent_goal_id=parent.id,
        description="Verify tax compliance against rules",
    )

    tree = manager.get_hierarchy(parent.id)
    assert tree["goal"]["id"] == parent.id
    assert len(tree["children"]) == 2

    manager.update_status(parent.id, "ACTIVE")
    assert manager.get_goal(parent.id).status == "ACTIVE"


def test_task_decomposition_and_workflow_export():
    manager = GoalManager()
    goal = manager.create_goal(description="Process vendor invoice for Acme Corp")

    decomposer = TaskDecomposer()
    plan = decomposer.decompose(goal=goal, strategy="HYBRID")

    assert len(plan.steps) >= 3
    assert plan.goal_id == goal.id
    assert plan.estimated_cost_usd > 0
    assert plan.risk_score >= 0.1

    # Test conversion to Phase 3 WorkflowDefinition
    workflow_def = decomposer.to_workflow_definition(plan)
    assert workflow_def.id.startswith("wf-agent-")
    assert len(workflow_def.tasks) == len(plan.steps)
    assert workflow_def.variables["goal_id"] == goal.id


def test_planning_engine_agent_matching_and_cycle_check():
    registry = AgentRegistry()
    registry.register(Agent(name="Validator1", type=AgentType.VALIDATION, skills=["validation", "ocr"]))
    registry.register(Agent(name="Executor1", type=AgentType.EXECUTION, skills=["extraction", "transformation"]))

    planner = PlanningEngine(registry=registry)
    goal = GoalModel(description="Review vendor contract agreement")

    plan = planner.create_plan(goal=goal, strategy="HYBRID")
    assert plan.plan_id.startswith("plan-")
    assert len(plan.steps) > 0
    assert plan.strategy == "HYBRID"
