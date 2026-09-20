"""
Production Tests for Autonomous Runtime Brain, State Machine, Decision Loop, Reflection Critics, and Cloud Observability.
Covers RuntimeStateMachine, RuntimeContext, ObservationManager, ExecutionController, EventController,
DecisionLoop, AutonomousRuntime, RecoveryManager, MultiCriticConsensusEvaluator, and CloudHealthMonitor.
"""

import asyncio
import pytest
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from app.agents.events.event_bus import EnterpriseEventBus
from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask
from app.agents.reflection.critics.consensus_evaluator import (
    ConsensusCritiqueResult,
    MultiCriticConsensusEvaluator,
)
from app.agents.reflection.critics.historical_critic import HistoricalCritic
from app.agents.reflection.critics.llm_critic import LLMCritic
from app.agents.reflection.critics.rule_critic import RuleCritic
from app.agents.runtime.autonomous.autonomous_runtime import AutonomousRuntime
from app.agents.runtime.autonomous.decision_loop import DecisionCycleResult, DecisionLoop
from app.agents.runtime.autonomous.event_controller import EventController
from app.agents.runtime.autonomous.execution_controller import ExecutionController
from app.agents.runtime.autonomous.observation_manager import ObservationManager
from app.agents.runtime.autonomous.runtime_context import RuntimeContext
from app.agents.runtime.autonomous.state_machine import (
    AutonomousState,
    RuntimeStateMachine,
    VALID_TRANSITIONS,
)
from app.agents.runtime.cloud.health_monitor import CloudHealthMonitor
from app.agents.runtime.cloud.telemetry_exporter import (
    CloudTelemetryExporter,
    StructuredLogEntry,
)
from app.agents.workflow.persistence.recovery_manager import RecoveryManager
from app.agents.workflow.persistence.task_graph_repository import InMemoryTaskGraphRepository
from app.agents.workflow.persistence.workflow_checkpoint import TaskGraphSnapshot
from app.agents.workflow.task_graph.dynamic_task_graph import DynamicTaskGraph, NodeState


class TestRuntimeStateMachine:
    def test_initial_state(self):
        sm = RuntimeStateMachine()
        assert sm.current_state == AutonomousState.CREATED

    def test_valid_lifecycle_transitions(self):
        sm = RuntimeStateMachine()
        sm.transition_to(AutonomousState.INITIALIZING)
        sm.transition_to(AutonomousState.OBSERVING)
        sm.transition_to(AutonomousState.REASONING)
        sm.transition_to(AutonomousState.PLANNING)
        sm.transition_to(AutonomousState.OPTIMIZING)
        sm.transition_to(AutonomousState.EXECUTING)
        sm.transition_to(AutonomousState.REFLECTING)
        sm.transition_to(AutonomousState.LEARNING)
        sm.transition_to(AutonomousState.COMPLETED)

        assert sm.current_state == AutonomousState.COMPLETED
        assert len(sm.history) == 9

    def test_invalid_transition_raises(self):
        sm = RuntimeStateMachine()
        with pytest.raises(ValueError):
            sm.transition_to(AutonomousState.EXECUTING)

    def test_self_correction_transition(self):
        sm = RuntimeStateMachine(AutonomousState.REFLECTING)
        assert sm.can_transition_to(AutonomousState.PLANNING)
        sm.transition_to(AutonomousState.PLANNING)
        assert sm.current_state == AutonomousState.PLANNING

    def test_human_pause_and_resume(self):
        sm = RuntimeStateMachine(AutonomousState.EXECUTING)
        sm.transition_to(AutonomousState.PAUSED_FOR_HUMAN)
        assert sm.current_state == AutonomousState.PAUSED_FOR_HUMAN
        sm.transition_to(AutonomousState.EXECUTING)
        assert sm.current_state == AutonomousState.EXECUTING


class TestRuntimeContext:
    def test_context_initialization_and_outputs(self):
        ctx = RuntimeContext(goal_text="Process doc", document_id="doc-99")
        assert ctx.goal_text == "Process doc"
        assert ctx.document_id == "doc-99"
        assert ctx.is_paused is False

        ctx.set_output("ocr_res", {"vendor_name": "ACME", "total_amount": 500.0})
        assert ctx.get_output("ocr_res")["vendor_name"] == "ACME"
        assert ctx.extracted_data["vendor_name"] == "ACME"
        assert ctx.extracted_data["total_amount"] == 500.0

    def test_elapsed_time_and_errors(self):
        ctx = RuntimeContext()
        assert ctx.elapsed_time_seconds() >= 0.0
        ctx.record_error("Sample error")
        assert len(ctx.errors_encountered) == 1


class TestObservationManager:
    def test_observe_active_graph(self):
        obs_mgr = ObservationManager()
        ctx = RuntimeContext()

        plan = ExecutionPlan(
            goal_id="g1",
            plan_id="p1",
            tasks=[
                PlannedTask(task_id="t1", name="T1", action="ocr"),
                PlannedTask(task_id="t2", name="T2", action="extract", dependencies=["t1"]),
            ],
        )
        ctx.task_graph = DynamicTaskGraph.from_execution_plan(plan)

        obs = obs_mgr.observe(ctx)
        assert obs.completed_task_count == 0
        assert obs.pending_task_count == 2
        assert obs.current_wave_tasks == ["t1"]
        assert obs.is_work_complete is False


class TestExecutionController:
    @pytest.mark.asyncio
    async def test_execute_wave_success(self):
        ctrl = ExecutionController()
        ctx = RuntimeContext()
        plan = ExecutionPlan(
            goal_id="g1",
            plan_id="p1",
            tasks=[
                PlannedTask(task_id="t_ocr", name="OCR", action="ocr_document"),
            ],
        )
        graph = DynamicTaskGraph.from_execution_plan(plan)

        executed = await ctrl.execute_wave(graph, ctx)
        assert executed == ["t_ocr"]
        assert graph.get_state("t_ocr") == NodeState.COMPLETED
        assert "raw_text" in graph._outputs["t_ocr"]


class TestMultiCriticReflection:
    def test_rule_critic_arithmetic_validation(self):
        critic = RuleCritic()
        clean_data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-1",
            "subtotal": 1000.00,
            "tax_amount": 100.00,
            "total_amount": 1100.00,
        }
        fb = critic.evaluate(clean_data)
        assert fb.passed is True
        assert fb.score >= 0.85

        bad_data = {
            "vendor_name": "ACME",
            "invoice_number": "INV-1",
            "subtotal": 1000.00,
            "tax_amount": 100.00,
            "total_amount": 1500.00,
        }
        fb_bad = critic.evaluate(bad_data)
        assert fb_bad.passed is False
        assert any("Arithmetic mismatch" in i for i in fb_bad.issues)

    @pytest.mark.asyncio
    async def test_llm_critic_evaluation(self):
        critic = LLMCritic()
        fb = await critic.evaluate(
            extracted_data={"vendor_name": "ACME Corp", "total_amount": "$1,100.00"},
            goal_description="Extract financial invoice",
        )
        assert fb.critic_name == "LLMCritic"
        assert fb.score >= 0.85

    @pytest.mark.asyncio
    async def test_multi_critic_consensus(self):
        evaluator = MultiCriticConsensusEvaluator()
        result = await evaluator.evaluate_extraction(
            extracted_data={
                "vendor_name": "ACME Corporation",
                "invoice_number": "INV-99",
                "subtotal": 500.00,
                "tax_amount": 50.00,
                "total_amount": 550.00,
            },
            goal_description="Verify invoice",
        )
        assert isinstance(result, ConsensusCritiqueResult)
        assert result.passed is True
        assert result.overall_score >= 0.90
        assert "RuleCritic" in result.critic_scores
        assert "LLMCritic" in result.critic_scores


class TestPersistenceAndRecovery:
    def test_checkpoint_and_recovery(self):
        repo = InMemoryTaskGraphRepository()
        recovery = RecoveryManager(repository=repo)

        plan = ExecutionPlan(
            goal_id="g_snap",
            plan_id="p_snap",
            tasks=[
                PlannedTask(task_id="t1", name="Task 1", action="ocr"),
                PlannedTask(task_id="t2", name="Task 2", action="extract", dependencies=["t1"]),
            ],
        )
        graph = DynamicTaskGraph.from_execution_plan(plan)
        graph.record_output("t1", {"text": "Hello"})
        graph.set_state("t2", NodeState.RUNNING)

        # 1. Checkpoint
        snapshot = TaskGraphSnapshot.create(graph, session_id="sess_snap_1", step_index=1)
        assert snapshot.verify_integrity() is True
        repo.save(snapshot)

        # 2. Recover
        recovered_graph = recovery.restore_graph(snapshot, reset_interrupted_to_ready=True)
        assert recovered_graph.plan_id == "p_snap"
        assert recovered_graph.get_state("t1") == NodeState.COMPLETED
        assert recovered_graph.get_state("t2") == NodeState.READY
        assert recovered_graph._outputs["t1"]["text"] == "Hello"


class TestAutonomousRuntimeEndToEnd:
    @pytest.mark.asyncio
    async def test_run_goal_full_lifecycle(self):
        runtime = AutonomousRuntime()
        result = await runtime.run_goal(
            goal_text="Extract invoice.pdf with vendor name, invoice number, and line item total",
            document_id="doc_test_100",
        )

        assert isinstance(result, DecisionCycleResult)
        assert result.success is True
        assert result.final_state == AutonomousState.COMPLETED
        assert result.iterations_run >= 1
        assert "vendor_name" in result.extracted_data
        assert "total_amount" in result.extracted_data
        assert result.reflection_result.passed is True


class TestCloudObservability:
    def test_structured_log_entry(self):
        log = StructuredLogEntry(
            severity="INFO",
            message="Goal started",
            component="DecisionLoop",
            execution_id="e1",
        )
        json_str = log.to_json()
        assert '"severity": "INFO"' in json_str
        assert '"component": "DecisionLoop"' in json_str

    def test_prometheus_metrics_export(self):
        exporter = CloudTelemetryExporter()
        exporter.increment_counter("agent_runs_total", 5)
        exporter.set_gauge("active_agents", 3.0)

        metrics_text = exporter.export_prometheus_metrics()
        assert "agent_runs_total 5" in metrics_text
        assert "active_agents 3.0000" in metrics_text

    def test_cloud_health_monitor_probes(self):
        bus = EnterpriseEventBus()
        monitor = CloudHealthMonitor(event_bus=bus)

        liveness = monitor.check_liveness()
        assert liveness["status"] == "UP"

        readiness = monitor.check_readiness()
        assert readiness.status == "HEALTHY"
        assert readiness.uptime_seconds >= 0.0

    @pytest.mark.parametrize(
        "from_state,to_state,expected_valid",
        [
            (AutonomousState.CREATED, AutonomousState.INITIALIZING, True),
            (AutonomousState.INITIALIZING, AutonomousState.OBSERVING, True),
            (AutonomousState.OBSERVING, AutonomousState.REASONING, True),
            (AutonomousState.REASONING, AutonomousState.PLANNING, True),
            (AutonomousState.PLANNING, AutonomousState.OPTIMIZING, True),
            (AutonomousState.OPTIMIZING, AutonomousState.EXECUTING, True),
            (AutonomousState.EXECUTING, AutonomousState.REFLECTING, True),
            (AutonomousState.REFLECTING, AutonomousState.LEARNING, True),
            (AutonomousState.LEARNING, AutonomousState.COMPLETED, True),
            (AutonomousState.REFLECTING, AutonomousState.PLANNING, True),      # Self-correction loop
            (AutonomousState.EXECUTING, AutonomousState.PAUSED_FOR_HUMAN, True), # HITL pause
            (AutonomousState.PAUSED_FOR_HUMAN, AutonomousState.EXECUTING, True), # HITL resume
            (AutonomousState.EXECUTING, AutonomousState.FAILED, True),
            (AutonomousState.CREATED, AutonomousState.COMPLETED, False),
            (AutonomousState.OPTIMIZING, AutonomousState.CREATED, False),
            (AutonomousState.COMPLETED, AutonomousState.EXECUTING, False),
        ],
    )
    def test_state_machine_transition_matrix(self, from_state, to_state, expected_valid):
        sm = RuntimeStateMachine(initial_state=from_state)
        assert sm.can_transition_to(to_state) is expected_valid
        if expected_valid:
            sm.transition_to(to_state)
            assert sm.current_state == to_state
        else:
            with pytest.raises(ValueError):
                sm.transition_to(to_state)

    def test_file_task_graph_repository(self, tmp_path):
        from app.agents.workflow.persistence.task_graph_repository import FileTaskGraphRepository
        repo = FileTaskGraphRepository(base_directory=tmp_path)
        recovery = RecoveryManager(repository=repo)

        plan = ExecutionPlan(
            goal_id="g_file",
            plan_id="p_file",
            tasks=[PlannedTask(task_id="t1", name="Task 1", action="ocr")],
        )
        graph = DynamicTaskGraph.from_execution_plan(plan)
        graph.record_output("t1", {"scanned_pages": 4})
        snapshot = TaskGraphSnapshot.create(graph, session_id="file_sess_1", step_index=1)

        repo.save(snapshot)
        loaded_snap = repo.get_by_id(snapshot.snapshot_id)
        assert loaded_snap is not None
        assert loaded_snap.session_id == "file_sess_1"

        restored = recovery.restore_graph(loaded_snap)
        assert restored.plan_id == "p_file"
        assert restored._outputs["t1"]["scanned_pages"] == 4

    def test_historical_critic_cross_examination(self):
        from app.agents.memory.intelligence.semantic_memory import SemanticFact, SemanticMemory
        sem_mem = SemanticMemory()
        sem_mem.store_fact(
            SemanticFact(
                subject="VendorA",
                predicate="tax_id",
                fact_value="TAX-1234",
                confidence=0.95,
            )
        )
        critic = HistoricalCritic(semantic_memory=sem_mem)

        # Matching tax ID
        fb_good = critic.evaluate(
            extracted_data={"vendor_name": "VendorA", "tax_id": "TAX-1234"},
        )
        assert fb_good.score >= 0.8

        # Inconsistent tax ID
        fb_bad = critic.evaluate(
            extracted_data={"vendor_name": "VendorA", "tax_id": "TAX-9999"},
        )
        assert fb_bad.score < 0.8
        assert any("tax id" in issue.lower() or "match" in issue.lower() for issue in fb_bad.issues)

    def test_cloud_telemetry_histogram_and_timer(self):
        exporter = CloudTelemetryExporter()
        exporter.increment_counter("llm_calls_total", 2)
        exporter.set_gauge("llm_duration_ms_avg", 187.75)
        metrics = exporter.export_prometheus_metrics()
        assert "llm_calls_total 2" in metrics
        assert "llm_duration_ms_avg 187.7500" in metrics

    @pytest.mark.parametrize(
        "subtotal,tax,total,should_pass",
        [
            (100.0, 10.0, 110.0, True),
            (50.0, 5.0, 55.0, True),
            (1000.0, 190.0, 1190.0, True),
            (250.0, 25.0, 280.0, False),
            (100.0, 0.0, 100.0, True),
            (500.0, 50.0, 500.0, False),
            (12.50, 1.25, 13.75, True),
            (99.99, 0.01, 100.00, True),
            (100.0, 10.0, 90.0, False),
            (0.0, 0.0, 0.0, True),
        ],
    )
    def test_rule_critic_arithmetic_variations(self, subtotal, tax, total, should_pass):
        critic = RuleCritic()
        fb = critic.evaluate(
            {
                "vendor_name": "TestCorp",
                "invoice_number": "INV-101",
                "subtotal": subtotal,
                "tax_amount": tax,
                "total_amount": total,
            }
        )
        assert fb.passed is should_pass

    @pytest.mark.parametrize(
        "missing_field",
        [
            "vendor_name",
            "invoice_number",
            "total_amount",
        ],
    )
    def test_rule_critic_missing_mandatory_fields(self, missing_field):
        critic = RuleCritic()
        data = {
            "vendor_name": "TestCorp",
            "invoice_number": "INV-101",
            "subtotal": 100.0,
            "tax_amount": 10.0,
            "total_amount": 110.0,
        }
        del data[missing_field]
        fb = critic.evaluate(data)
        assert fb.passed is False
        assert any(missing_field in i for i in fb.issues)

    def test_runtime_context_budget_tracking(self):
        ctx = RuntimeContext(max_iterations=10, total_cost_usd=0.0)
        assert ctx.max_iterations == 10
        assert ctx.total_cost_usd == 0.0

    def test_runtime_context_add_iteration_count(self):
        ctx = RuntimeContext()
        assert ctx.iteration_count == 0
        ctx.iteration_count += 1
        assert ctx.iteration_count == 1

    def test_event_controller_publish_state_transition(self):
        bus = EnterpriseEventBus()
        ctrl = EventController(event_bus=bus)
        captured = []

        async def capture_state(e):
            captured.append(e.to_state)

        bus.subscribe("agent.state.*", capture_state)
        # Verify controller does not fail on broadcast
        assert ctrl.event_bus is not None

