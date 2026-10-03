"""Tests for Autonomous Planning Engine (Phase 25.0).

Covers:
- CapabilityDiscovery (agent/tool manifests, filtering, multi-factor matching)
- TaskDecomposer (decompositions across document domains, human approval injection)
- ExecutionPlan (topological sorting, cycle detection, task status tracking)
- AutonomousPlanner (plan generation, fallback routing, cost/latency estimation)
"""

from __future__ import annotations

import pytest

from app.agents.intelligence.goal import (
    GoalPriority,
    GoalSpecification,
)
from app.agents.planning import (
    AgentCapabilityRecord,
    AutonomousPlanner,
    CapabilityDiscovery,
    ExecutionPlan,
    FallbackStrategy,
    PlannedTask,
    TaskDecomposer,
    TaskStatus,
    ToolCapabilityRecord,
)


class TestCapabilityDiscovery:
    @pytest.fixture
    def discovery(self):
        return CapabilityDiscovery()

    def test_default_agents_registered(self, discovery):
        assert discovery.get_agent("agent_ocr_vision") is not None
        assert discovery.get_agent("agent_extraction_nlp") is not None
        assert discovery.get_agent("agent_validation_math") is not None
        assert discovery.get_agent("agent_compliance_sox") is not None
        assert discovery.get_agent("agent_correction_gemini") is not None

    def test_default_tools_registered(self, discovery):
        assert discovery.get_tool("tool_tesseract_ocr") is not None
        assert discovery.get_tool("tool_gemini_vision") is not None
        assert discovery.get_tool("tool_json_validator") is not None
        assert discovery.get_tool("tool_compliance_checker") is not None

    def test_register_custom_agent(self, discovery):
        agent = AgentCapabilityRecord(
            agent_id="custom_agent",
            role="CUSTOM_ROLE",
            capabilities=["special_ocr"],
            supported_intents=["DOCUMENT_EXTRACTION"],
        )
        discovery.register_agent(agent)
        assert discovery.get_agent("custom_agent") == agent

    def test_register_custom_tool(self, discovery):
        tool = ToolCapabilityRecord(
            tool_id="custom_tool",
            name="Custom Tool",
            action_type="custom_action",
            supported_modalities=["PDF"],
        )
        discovery.register_tool(tool)
        assert discovery.get_tool("custom_tool") == tool

    def test_find_agents_for_capability(self, discovery):
        matches = discovery.find_agents_for_capability("ocr")
        assert len(matches) >= 1
        assert matches[0].agent_id == "agent_ocr_vision"

    def test_find_agents_for_unknown_capability(self, discovery):
        matches = discovery.find_agents_for_capability("quantum_teleportation")
        assert len(matches) == 0

    def test_match_agent_primary_capability(self, discovery):
        agent = discovery.match_agent("arithmetic_verification", "INVOICE_PROCESSING")
        assert agent is not None
        assert agent.agent_id == "agent_validation_math"

    def test_match_agent_supported_intent_fallback(self, discovery):
        agent = discovery.match_agent("unknown_action", "CONTRACT_REVIEW")
        assert agent is not None
        assert "CONTRACT_REVIEW" in agent.supported_intents

    def test_match_agent_none_found(self, discovery):
        agent = discovery.match_agent("nonexistent_action", "NONEXISTENT_INTENT")
        assert agent is None

    def test_match_tool_low_cost(self, discovery):
        tool = discovery.match_tool("ocr", modality="IMAGE", high_accuracy=False)
        assert tool is not None
        assert tool.tool_id == "tool_tesseract_ocr"

    def test_match_tool_high_accuracy(self, discovery):
        tool = discovery.match_tool("ocr", modality="IMAGE", high_accuracy=True)
        assert tool is not None
        assert tool.tool_id == "tool_gemini_vision"

    def test_match_tool_modality_handwriting(self, discovery):
        tool = discovery.match_tool("ocr", modality="HANDWRITING")
        assert tool is not None
        assert tool.tool_id == "tool_gemini_vision"

    def test_match_tool_nonexistent(self, discovery):
        tool = discovery.match_tool("nonexistent_action")
        assert tool is None


class TestTaskDecomposer:
    @pytest.fixture
    def decomposer(self):
        return TaskDecomposer()

    def test_decompose_financial_invoice(self, decomposer):
        goal = GoalSpecification(objective="Extract invoice", intent="INVOICE_PROCESSING")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 4
        actions = [t.action for t in tasks]
        assert actions == ["ocr", "entity_extraction", "arithmetic_verification", "regulatory_audit"]

    def test_decompose_receipt(self, decomposer):
        goal = GoalSpecification(objective="Extract receipt", intent="RECEIPT_ANALYSIS")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 4
        assert tasks[0].action == "ocr"

    def test_decompose_compliance_audit(self, decomposer):
        goal = GoalSpecification(objective="Audit compliance", intent="COMPLIANCE_AUDIT")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 3
        actions = [t.action for t in tasks]
        assert actions == ["ocr", "clause_extraction", "regulatory_audit"]

    def test_decompose_contract_review(self, decomposer):
        goal = GoalSpecification(objective="Review contract", intent="CONTRACT_REVIEW")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 3
        actions = [t.action for t in tasks]
        assert actions == ["ocr", "clause_extraction", "risk_assessment"]

    def test_decompose_fraud_detection(self, decomposer):
        goal = GoalSpecification(objective="Detect fraud", intent="FRAUD_DETECTION")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 3
        actions = [t.action for t in tasks]
        assert actions == ["ocr", "tamper_analysis", "fraud_scoring"]

    def test_decompose_generic(self, decomposer):
        goal = GoalSpecification(objective="Extract generic data", intent="GENERIC_TASK")
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 2
        assert tasks[0].action == "ocr"
        assert tasks[1].action == "entity_extraction"

    def test_decompose_with_human_review_constraint(self, decomposer):
        goal = GoalSpecification(
            objective="Extract invoice",
            intent="INVOICE_PROCESSING",
            constraints={"require_human_review": True},
        )
        tasks = decomposer.decompose(goal)
        assert len(tasks) == 5
        assert tasks[-1].action == "human_review"
        assert tasks[-1].assigned_agent == "agent_human_supervisor"
        assert tasks[-1].dependencies == [tasks[-2].task_id]


class TestPlannedTaskAndExecutionPlan:
    def test_task_is_ready_no_dependencies(self):
        task = PlannedTask(task_id="t1", name="Task 1", action="ocr", dependencies=[])
        assert task.is_ready(set()) is True

    def test_task_is_ready_with_dependencies(self):
        task = PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"])
        assert task.is_ready(set()) is False
        assert task.is_ready({"t1"}) is True

    def test_execution_plan_add_and_get_task(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        plan.add_task(t1)
        assert plan.get_task("t1") == t1
        assert plan.get_task("unknown") is None

    def test_execution_plan_duplicate_task_error(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        plan.add_task(t1)
        with pytest.raises(ValueError, match="already exists"):
            plan.add_task(t1)

    def test_topological_order_linear(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        t2 = PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"])
        t3 = PlannedTask(task_id="t3", name="Task 3", action="validate", dependencies=["t2"])
        plan.add_task(t3)
        plan.add_task(t1)
        plan.add_task(t2)
        order = plan.get_topological_order()
        assert [t.task_id for t in order] == ["t1", "t2", "t3"]

    def test_topological_order_parallel_branches(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        t2a = PlannedTask(task_id="t2a", name="Task 2A", action="extract", dependencies=["t1"])
        t2b = PlannedTask(task_id="t2b", name="Task 2B", action="fraud", dependencies=["t1"])
        t3 = PlannedTask(task_id="t3", name="Task 3", action="merge", dependencies=["t2a", "t2b"])
        plan.add_task(t1)
        plan.add_task(t2a)
        plan.add_task(t2b)
        plan.add_task(t3)
        order = plan.get_topological_order()
        ids = [t.task_id for t in order]
        assert ids.index("t1") < ids.index("t2a")
        assert ids.index("t1") < ids.index("t2b")
        assert ids.index("t2a") < ids.index("t3")
        assert ids.index("t2b") < ids.index("t3")

    def test_topological_order_cycle_detected(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr", dependencies=["t2"])
        t2 = PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"])
        plan.add_task(t1)
        plan.add_task(t2)
        with pytest.raises(ValueError, match="Cycle detected"):
            plan.get_topological_order()


class TestAutonomousPlanner:
    @pytest.fixture
    def planner(self):
        return AutonomousPlanner()

    def test_generate_plan_for_invoice(self, planner):
        goal = GoalSpecification(
            objective="Process invoice INV-100 with accuracy >= 95%",
            intent="INVOICE_PROCESSING",
            constraints={"min_accuracy": 0.95},
        )
        plan = planner.generate_plan(goal)
        assert len(plan.tasks) == 4
        assert plan.goal_id == goal.goal_id
        assert plan.estimated_cost_usd > 0
        assert plan.estimated_duration_seconds > 0
        assert len(plan.verification_steps) >= 1

    def test_generate_plan_agent_assignments(self, planner):
        goal = GoalSpecification(objective="Process invoice", intent="INVOICE_PROCESSING")
        plan = planner.generate_plan(goal)
        assigned = [t.assigned_agent for t in plan.tasks]
        assert "agent_ocr_vision" in assigned
        assert "agent_extraction_nlp" in assigned
        assert "agent_validation_math" in assigned
        assert "agent_compliance_sox" in assigned

    def test_generate_plan_high_accuracy_tool_selection(self, planner):
        goal = GoalSpecification(
            objective="Process invoice with accuracy >= 98%",
            intent="INVOICE_PROCESSING",
            constraints={"min_accuracy": 0.98},
        )
        plan = planner.generate_plan(goal)
        ocr_task = plan.tasks[0]
        assert "tool_gemini_vision" in ocr_task.required_tools

    def test_generate_plan_low_accuracy_tool_selection(self, planner):
        goal = GoalSpecification(
            objective="Process invoice fast",
            intent="INVOICE_PROCESSING",
            constraints={"min_accuracy": 0.85},
        )
        plan = planner.generate_plan(goal)
        ocr_task = plan.tasks[0]
        assert "tool_tesseract_ocr" in ocr_task.required_tools

    def test_generate_plan_fallback_strategies(self, planner):
        goal = GoalSpecification(objective="Process invoice", intent="INVOICE_PROCESSING")
        plan = planner.generate_plan(goal)
        assert len(plan.fallback_strategies) >= 2
        ocr_task_id = plan.tasks[0].task_id
        assert ocr_task_id in plan.fallback_strategies
        assert plan.fallback_strategies[ocr_task_id].fallback_action == "SWITCH_TOOL"
        assert "tool_gemini_vision" in plan.fallback_strategies[ocr_task_id].alternative_tools

    def test_generate_plan_metadata(self, planner):
        goal = GoalSpecification(objective="Process invoice", intent="INVOICE_PROCESSING", priority=GoalPriority.HIGH)
        plan = planner.generate_plan(goal)
        assert plan.metadata["intent"] == "INVOICE_PROCESSING"
        assert plan.metadata["priority"] == "HIGH"
        assert plan.metadata["task_count"] == 4

    def test_generate_plan_compliance_audit(self, planner):
        goal = GoalSpecification(objective="Audit SOX", intent="COMPLIANCE_AUDIT")
        plan = planner.generate_plan(goal)
        assert len(plan.tasks) == 3
        assert plan.tasks[-1].action == "regulatory_audit"

    def test_generate_plan_contract_review(self, planner):
        goal = GoalSpecification(objective="Review NDA", intent="CONTRACT_REVIEW")
        plan = planner.generate_plan(goal)
        assert len(plan.tasks) == 3
        assert plan.tasks[-1].action == "risk_assessment"

    def test_generate_plan_fraud_detection(self, planner):
        goal = GoalSpecification(objective="Detect forgery", intent="FRAUD_DETECTION")
        plan = planner.generate_plan(goal)
        assert len(plan.tasks) == 3
        assert plan.tasks[-1].action == "fraud_scoring"

    def test_generate_plan_generic_task(self, planner):
        goal = GoalSpecification(objective="Transcribe document", intent="GENERIC_TASK")
        plan = planner.generate_plan(goal)
        assert len(plan.tasks) == 2


class TestPlanningInvariantsAndEdgeCases:
    def test_unavailable_agent_excluded_from_matching(self):
        disc = CapabilityDiscovery()
        agent = disc.get_agent("agent_ocr_vision")
        agent.is_available = False
        match = disc.match_agent("ocr", "DOCUMENT_EXTRACTION")
        # should not match the unavailable agent
        if match:
            assert match.agent_id != "agent_ocr_vision"

    def test_self_cycle_detected(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr", dependencies=["t1"])
        plan.add_task(t1)
        with pytest.raises(ValueError, match="Cycle detected"):
            plan.get_topological_order()

    def test_three_node_cycle_detected(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr", dependencies=["t3"])
        t2 = PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"])
        t3 = PlannedTask(task_id="t3", name="Task 3", action="validate", dependencies=["t2"])
        plan.add_task(t1)
        plan.add_task(t2)
        plan.add_task(t3)
        with pytest.raises(ValueError, match="Cycle detected"):
            plan.get_topological_order()

    def test_dependencies_map(self):
        plan = ExecutionPlan(goal_id="g1")
        t1 = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        t2 = PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"])
        plan.add_task(t1)
        plan.add_task(t2)
        dep_map = plan.get_dependencies_map()
        assert dep_map == {"t1": [], "t2": ["t1"]}

    def test_large_dag_topological_ordering(self):
        plan = ExecutionPlan(goal_id="g_large")
        for i in range(20):
            deps = [f"t{i-1}"] if i > 0 else []
            plan.add_task(PlannedTask(task_id=f"t{i}", name=f"Task {i}", action="step", dependencies=deps))
        order = plan.get_topological_order()
        assert len(order) == 20
        assert [t.task_id for t in order] == [f"t{i}" for i in range(20)]

    def test_fan_out_fan_in_dag(self):
        plan = ExecutionPlan(goal_id="g_fan")
        plan.add_task(PlannedTask(task_id="start", name="Start", action="init"))
        for i in range(5):
            plan.add_task(PlannedTask(task_id=f"branch_{i}", name=f"Branch {i}", action="work", dependencies=["start"]))
        plan.add_task(PlannedTask(task_id="join", name="Join", action="reduce", dependencies=[f"branch_{i}" for i in range(5)]))
        order = plan.get_topological_order()
        ids = [t.task_id for t in order]
        assert ids[0] == "start"
        assert ids[-1] == "join"
        for i in range(5):
            assert f"branch_{i}" in ids[1:6]

    def test_fallback_strategy_dataclass(self):
        fb = FallbackStrategy(
            task_id="t1",
            fallback_action="SWITCH_TOOL",
            alternative_agent="agent_fallback",
            alternative_tools=["tool_fallback"],
            max_fallback_attempts=3,
        )
        assert fb.task_id == "t1"
        assert fb.max_fallback_attempts == 3
        assert fb.alternative_agent == "agent_fallback"

    def test_planned_task_status_transitions(self):
        task = PlannedTask(task_id="t1", name="Task 1", action="ocr")
        assert task.status == TaskStatus.PENDING
        task.status = TaskStatus.RUNNING
        assert task.status == TaskStatus.RUNNING
        task.status = TaskStatus.COMPLETED
        assert task.status == TaskStatus.COMPLETED

    def test_agent_capability_record_properties(self):
        agent = AgentCapabilityRecord(
            agent_id="test_ag",
            role="TEST_ROLE",
            capabilities=["cap1", "cap2"],
            supported_intents=["INTENT_1"],
            latency_ms_p95=100.0,
            cost_per_invocation=0.005,
            accuracy_rating=0.99,
        )
        assert agent.agent_id == "test_ag"
        assert agent.accuracy_rating == 0.99
        assert agent.is_available is True

    def test_tool_capability_record_properties(self):
        tool = ToolCapabilityRecord(
            tool_id="test_tool",
            name="Test Tool",
            action_type="test_action",
            supported_modalities=["PDF", "IMAGE"],
            cost_per_call=0.001,
            latency_ms=50.0,
            reliability_rating=0.95,
        )
        assert tool.tool_id == "test_tool"
        assert tool.action_type == "test_action"
        assert "PDF" in tool.supported_modalities

    def test_discovery_register_override(self):
        disc = CapabilityDiscovery()
        custom = AgentCapabilityRecord(
            agent_id="agent_ocr_vision",
            role="OVERRIDDEN_ROLE",
            capabilities=["super_ocr"],
            supported_intents=["DOCUMENT_EXTRACTION"],
        )
        disc.register_agent(custom)
        assert disc.get_agent("agent_ocr_vision").role == "OVERRIDDEN_ROLE"

    def test_match_tool_category_fallback(self):
        disc = CapabilityDiscovery()
        # Modality not directly listed, falls back to action_type candidates
        matched = disc.match_tool("ocr", modality="AUDIO")
        assert matched is not None
        assert matched.action_type == "ocr"

    def test_task_decomposer_preserves_custom_inputs(self):
        decomposer = TaskDecomposer()
        goal = GoalSpecification(
            objective="Process invoice",
            intent="INVOICE_PROCESSING",
            input_requirements={"document_path": "/path/to/invoice.pdf", "expected_currency": "EUR"},
        )
        tasks = decomposer.decompose(goal)
        assert tasks[0].input_parameters["document_path"] == "/path/to/invoice.pdf"
        assert tasks[2].input_parameters["expected_currency"] == "EUR"

    @pytest.mark.parametrize("priority", [GoalPriority.LOW, GoalPriority.MEDIUM, GoalPriority.HIGH, GoalPriority.CRITICAL])
    def test_planner_handles_all_priorities(self, priority):
        planner = AutonomousPlanner()
        goal = GoalSpecification(objective="Task", priority=priority)
        plan = planner.generate_plan(goal)
        assert plan.metadata["priority"] == priority.value

    def test_planner_zero_cost_with_zero_tasks(self):
        plan = ExecutionPlan(goal_id="g_empty")
        assert plan.estimated_cost_usd == 0.0
        assert plan.estimated_duration_seconds == 0.0

    def test_planned_task_default_criticality(self):
        task = PlannedTask(task_id="t1", name="Task", action="act")
        assert task.is_critical is True
        assert task.timeout_seconds == 30.0
        assert task.max_retries == 2


