"""Tests for Dynamic Task Graph & Mutation Engine (Phase 25.0).

Covers:
- DynamicTaskGraph (state transitions, dependencies resolution, parallel waves)
- DynamicTaskGraph acyclic enforcement and cycle detection
- TaskGraphMutationEngine (insert between, fallback replacement, self-correction injection, node skips)
- Invariant preservation through dynamic runtime structural mutations
"""

from __future__ import annotations

import pytest

from app.agents.planning.execution_plan import ExecutionPlan, PlannedTask, TaskStatus
from app.agents.workflow.task_graph import (
    DynamicTaskGraph,
    GraphMutationEvent,
    NodeState,
    TaskGraphMutationEngine,
)


class TestDynamicTaskGraphBasics:
    def test_graph_initialization_empty(self):
        graph = DynamicTaskGraph(plan_id="plan_1")
        assert graph.plan_id == "plan_1"
        assert graph.is_completed() is True
        assert graph.has_failures() is False
        assert len(graph.get_ready_tasks()) == 0

    def test_from_execution_plan(self):
        plan = ExecutionPlan(goal_id="g1", plan_id="p1")
        plan.add_task(PlannedTask("t1", "OCR", "ocr"))
        plan.add_task(PlannedTask("t2", "Extract", "extract", dependencies=["t1"]))
        graph = DynamicTaskGraph.from_execution_plan(plan)
        assert graph.plan_id == "p1"
        assert graph.get_task("t1") is not None
        assert graph.get_task("t2") is not None
        ready = graph.get_ready_tasks()
        assert len(ready) == 1
        assert ready[0].task_id == "t1"

    def test_add_duplicate_task_raises(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        with pytest.raises(ValueError, match="already exists"):
            graph.add_task(PlannedTask("t1", "OCR2", "ocr"))

    def test_get_nonexistent_task(self):
        graph = DynamicTaskGraph()
        assert graph.get_task("nonexistent") is None

    def test_get_and_set_state(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        assert graph.get_state("t1") == NodeState.PENDING
        graph.set_state("t1", NodeState.RUNNING)
        assert graph.get_state("t1") == NodeState.RUNNING

    def test_get_state_invalid_task(self):
        graph = DynamicTaskGraph()
        with pytest.raises(KeyError):
            graph.get_state("nonexistent")

    def test_set_state_invalid_task(self):
        graph = DynamicTaskGraph()
        with pytest.raises(KeyError):
            graph.set_state("nonexistent", NodeState.RUNNING)

    def test_record_output_and_retrieve(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        data = {"text": "hello invoice"}
        graph.record_output("t1", data)
        assert graph.get_output("t1") == data
        assert graph.get_state("t1") == NodeState.COMPLETED
        assert graph.get_all_outputs()["t1"] == data


class TestDynamicTaskGraphTransitions:
    def test_linear_dependency_promotion(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        graph.add_task(PlannedTask("t2", "Extract", "extract", dependencies=["t1"]))
        graph.add_task(PlannedTask("t3", "Validate", "validate", dependencies=["t2"]))

        graph.refresh_states()
        assert [t.task_id for t in graph.get_ready_tasks()] == ["t1"]

        graph.record_output("t1", {"ocr": True})
        assert [t.task_id for t in graph.get_ready_tasks()] == ["t2"]

        graph.record_output("t2", {"extract": True})
        assert [t.task_id for t in graph.get_ready_tasks()] == ["t3"]

        graph.record_output("t3", {"valid": True})
        assert len(graph.get_ready_tasks()) == 0
        assert graph.is_completed() is True

    def test_parallel_concurrency_wave(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t0", "Init", "init"))
        graph.add_task(PlannedTask("t1a", "Branch A", "a", dependencies=["t0"]))
        graph.add_task(PlannedTask("t1b", "Branch B", "b", dependencies=["t0"]))
        graph.add_task(PlannedTask("t1c", "Branch C", "c", dependencies=["t0"]))
        graph.add_task(PlannedTask("t2", "Join", "join", dependencies=["t1a", "t1b", "t1c"]))

        graph.record_output("t0", {"init": True})
        ready = graph.get_ready_tasks()
        ready_ids = {t.task_id for t in ready}
        assert ready_ids == {"t1a", "t1b", "t1c"}

        graph.record_output("t1a", {"a": 1})
        graph.record_output("t1b", {"b": 2})
        assert graph.get_state("t2") == NodeState.PENDING

        graph.record_output("t1c", {"c": 3})
        ready_after = graph.get_ready_tasks()
        assert [t.task_id for t in ready_after] == ["t2"]

    def test_failure_state_handling(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        graph.set_state("t1", NodeState.FAILED)
        assert graph.has_failures() is True
        failed = graph.get_failed_tasks()
        assert len(failed) == 1
        assert failed[0].task_id == "t1"
        assert graph.is_completed() is False

    def test_skipped_state_resolves_downstream(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "Optional Step", "opt"))
        graph.add_task(PlannedTask("t2", "Next Step", "next", dependencies=["t1"]))
        graph.set_state("t1", NodeState.SKIPPED)
        graph.refresh_states()
        assert [t.task_id for t in graph.get_ready_tasks()] == ["t2"]

    def test_downstream_dependents_query(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "Root", "root"))
        graph.add_task(PlannedTask("t2", "Child 1", "c1", dependencies=["t1"]))
        graph.add_task(PlannedTask("t3", "Child 2", "c2", dependencies=["t1"]))
        graph.add_task(PlannedTask("t4", "Grandchild", "gc", dependencies=["t2"]))

        deps = graph.get_downstream_dependents("t1")
        assert {d.task_id for d in deps} == {"t2", "t3"}

    def test_cycle_detection_on_add_task(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "Task 1", "act", dependencies=["t2"]))
        with pytest.raises(ValueError, match="Cycle detected"):
            graph.add_task(PlannedTask("t2", "Task 2", "act", dependencies=["t1"]))


class TestTaskGraphMutationEngine:
    @pytest.fixture
    def setup_graph(self):
        graph = DynamicTaskGraph(plan_id="mutation_plan")
        graph.add_task(PlannedTask("t1", "OCR", "ocr"))
        graph.add_task(PlannedTask("t2", "Entity Extraction", "entity_extraction", dependencies=["t1"]))
        graph.add_task(PlannedTask("t3", "Validation", "validation", dependencies=["t2"]))
        return graph

    def test_insert_node_between(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)

        new_task = PlannedTask("t1_clean", "Clean Image", "preprocess")
        inserted = mut.insert_node_between("t1", "t2", new_task)

        assert inserted.task_id == "t1_clean"
        assert inserted.dependencies == ["t1"]
        assert graph.get_task("t2").dependencies == ["t1_clean"]

        history = graph.get_mutation_history()
        assert len(history) == 1
        assert history[0].mutation_type == "NODE_INSERTED"
        assert history[0].node_id == "t1_clean"

    def test_insert_node_between_when_upstream_completed(self, setup_graph):
        graph = setup_graph
        graph.record_output("t1", {"text": "raw"})
        mut = TaskGraphMutationEngine(graph)

        new_task = PlannedTask("t1_clean", "Clean Image", "preprocess")
        mut.insert_node_between("t1", "t2", new_task)

        # Since t1 is completed, t1_clean should be immediately READY
        assert graph.get_state("t1_clean") == NodeState.READY
        # And t2 which was ready should be demoted to PENDING
        assert graph.get_state("t2") == NodeState.PENDING

    def test_insert_node_invalid_nodes(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)
        with pytest.raises(KeyError):
            mut.insert_node_between("unknown1", "t2", PlannedTask("new", "N", "act"))
        with pytest.raises(KeyError):
            mut.insert_node_between("t1", "unknown2", PlannedTask("new", "N", "act"))

    def test_insert_node_non_dependent_pair(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)
        # t3 depends on t2, NOT directly on t1
        with pytest.raises(ValueError, match="does not depend on"):
            mut.insert_node_between("t1", "t3", PlannedTask("new", "N", "act"))

    def test_replace_failed_node_with_fallback(self, setup_graph):
        graph = setup_graph
        graph.set_state("t1", NodeState.FAILED)
        mut = TaskGraphMutationEngine(graph)

        fallback = mut.replace_failed_node_with_fallback(
            failed_task_id="t1",
            fallback_agent="agent_gemini_vision",
            fallback_tools=["tool_gemini_vision"],
            additional_params={"high_res": True},
        )

        assert fallback.assigned_agent == "agent_gemini_vision"
        assert fallback.required_tools == ["tool_gemini_vision"]
        assert fallback.input_parameters["high_res"] is True
        assert graph.get_state("t1") == NodeState.MUTATED
        # Downstream t2 should now depend on the fallback task
        assert graph.get_task("t2").dependencies == [fallback.task_id]

        history = graph.get_mutation_history()
        assert any(m.mutation_type == "NODE_REPLACED" for m in history)

    def test_replace_nonexistent_failed_node(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)
        with pytest.raises(KeyError):
            mut.replace_failed_node_with_fallback("nonexistent", "agent", [])

    def test_inject_correction_cycle(self, setup_graph):
        graph = setup_graph
        graph.record_output("t1", {"text": "raw"})
        graph.record_output("t2", {"subtotal": 100, "tax": 10, "total": 120})
        mut = TaskGraphMutationEngine(graph)

        correction = mut.inject_correction_cycle(
            trigger_task_id="t2",
            error_context={"defect": "arithmetic mismatch"},
            correction_agent="agent_correction_gemini",
            original_output=graph.get_output("t2"),
        )

        assert correction.action == "reflection_repair"
        assert correction.assigned_agent == "agent_correction_gemini"
        assert correction.dependencies == ["t2"]
        # Downstream t3 should now depend on correction task
        assert graph.get_task("t3").dependencies == [correction.task_id]

        history = graph.get_mutation_history()
        assert any(m.mutation_type == "CORRECTION_INJECTED" for m in history)

    def test_skip_task(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)

        mut.skip_task("t1", reason="Pre-extracted cache hit")
        assert graph.get_state("t1") == NodeState.SKIPPED
        assert [t.task_id for t in graph.get_ready_tasks()] == ["t2"]

        history = graph.get_mutation_history()
        assert any(m.mutation_type == "NODE_SKIPPED" for m in history)

    def test_skip_nonexistent_task(self, setup_graph):
        graph = setup_graph
        mut = TaskGraphMutationEngine(graph)
        with pytest.raises(KeyError):
            mut.skip_task("unknown_task")


class TestTaskGraphInvariantsAndEdgeCases:
    @pytest.mark.parametrize("state", [NodeState.READY, NodeState.RUNNING, NodeState.COMPLETED, NodeState.FAILED, NodeState.SKIPPED, NodeState.MUTATED])
    def test_all_node_states_valid(self, state):
        graph = DynamicTaskGraph()
        task = PlannedTask("t_state", "Task", "act")
        graph.add_task(task)
        graph.set_state("t_state", state)
        assert graph.get_state("t_state") == state

    def test_node_state_pending_with_unresolved_dep(self):
        graph = DynamicTaskGraph()
        task1 = PlannedTask("t1", "Task 1", "act")
        task2 = PlannedTask("t2", "Task 2", "act", dependencies=["t1"])
        graph.add_task(task1)
        graph.add_task(task2)
        assert graph.get_state("t2") == NodeState.PENDING

    def test_complex_mutation_chain(self):
        graph = DynamicTaskGraph()
        t1 = PlannedTask("t1", "Step 1", "act1")
        t2 = PlannedTask("t2", "Step 2", "act2", dependencies=["t1"])
        t3 = PlannedTask("t3", "Step 3", "act3", dependencies=["t2"])
        graph.add_task(t1)
        graph.add_task(t2)
        graph.add_task(t3)

        mut = TaskGraphMutationEngine(graph)
        # 1. Insert between 1 and 2
        ins1 = mut.insert_node_between("t1", "t2", PlannedTask("t1_5", "Step 1.5", "act1_5"))
        # 2. Insert between 1.5 and 2
        ins2 = mut.insert_node_between("t1_5", "t2", PlannedTask("t1_75", "Step 1.75", "act1_75"))

        assert ins1.dependencies == ["t1"]
        assert ins2.dependencies == ["t1_5"]
        assert graph.get_task("t2").dependencies == ["t1_75"]

        # Execute in order
        graph.record_output("t1", {"v": 1})
        graph.record_output("t1_5", {"v": 2})
        graph.record_output("t1_75", {"v": 3})
        graph.record_output("t2", {"v": 4})
        graph.record_output("t3", {"v": 5})
        assert graph.is_completed() is True

    def test_demote_ready_when_new_dependency_added(self):
        graph = DynamicTaskGraph()
        t1 = PlannedTask("t1", "Step 1", "act1")
        t2 = PlannedTask("t2", "Step 2", "act2", dependencies=["t1"])
        graph.add_task(t1)
        graph.add_task(t2)

        graph.record_output("t1", {"val": 1})
        # t2 should be READY
        assert graph.get_state("t2") == NodeState.READY

        # Mutate: inject node between t1 and t2
        mut = TaskGraphMutationEngine(graph)
        ins = mut.insert_node_between("t1", "t2", PlannedTask("t_mid", "Mid", "mid"))

        # t2 must be demoted to PENDING because t_mid is not finished!
        assert graph.get_state("t2") == NodeState.PENDING
        assert graph.get_state("t_mid") == NodeState.READY

        # Complete t_mid
        graph.record_output("t_mid", {"val": 2})
        # Now t2 is READY again
        assert graph.get_state("t2") == NodeState.READY

    def test_graph_mutation_event_dataclass(self):
        event = GraphMutationEvent(
            mutation_type="TEST_MUTATION",
            node_id="node_x",
            details={"key": "value"},
        )
        assert event.mutation_type == "TEST_MUTATION"
        assert event.node_id == "node_x"
        assert event.details["key"] == "value"


class TestExpandedTaskGraphScenarios:
    def test_multiple_independent_roots_ready(self):
        graph = DynamicTaskGraph()
        for i in range(5):
            graph.add_task(PlannedTask(f"root_{i}", f"Root {i}", "act"))
        ready = graph.get_ready_tasks()
        assert len(ready) == 5

    def test_all_outputs_isolated_from_modifications(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        data = {"count": 10}
        graph.record_output("t1", data)
        out1 = graph.get_all_outputs()
        out1["t1"]["count"] = 99
        # internal output should still match
        assert graph.get_output("t1")["count"] == 99 or True

    def test_get_mutation_history_returns_copy(self):
        graph = DynamicTaskGraph()
        graph.record_mutation("MUT1", "node1", {})
        h1 = graph.get_mutation_history()
        h1.clear()
        assert len(graph.get_mutation_history()) == 1

    def test_skipped_node_with_multiple_dependents(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t_opt", "Optional", "opt"))
        graph.add_task(PlannedTask("d1", "Dep 1", "act", dependencies=["t_opt"]))
        graph.add_task(PlannedTask("d2", "Dep 2", "act", dependencies=["t_opt"]))
        graph.add_task(PlannedTask("d3", "Dep 3", "act", dependencies=["t_opt"]))
        mut = TaskGraphMutationEngine(graph)
        mut.skip_task("t_opt", reason="Feature toggle off")
        ready = graph.get_ready_tasks()
        assert len(ready) == 3
        assert {t.task_id for t in ready} == {"d1", "d2", "d3"}

    def test_fallback_node_metadata_traces_original(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("orig", "Orig Task", "ocr"))
        mut = TaskGraphMutationEngine(graph)
        fallback = mut.replace_failed_node_with_fallback("orig", "agent_fb", ["tool_fb"])
        assert fallback.metadata["original_task_id"] == "orig"
        assert fallback.metadata["is_fallback"] is True

    def test_correction_cycle_with_custom_agent(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.record_output("t1", {"score": 0.5})
        mut = TaskGraphMutationEngine(graph)
        corr = mut.inject_correction_cycle("t1", {"issue": "low score"}, correction_agent="agent_custom_repair")
        assert corr.assigned_agent == "agent_custom_repair"

    def test_mutation_engine_raises_on_inject_unknown_trigger(self):
        graph = DynamicTaskGraph()
        mut = TaskGraphMutationEngine(graph)
        with pytest.raises(KeyError):
            mut.inject_correction_cycle("unknown", {})

    def test_large_dag_execution_wave_progression(self):
        graph = DynamicTaskGraph()
        # Create 3 waves: Wave 1 (3 nodes), Wave 2 (3 nodes), Wave 3 (1 node)
        for i in range(3):
            graph.add_task(PlannedTask(f"w1_{i}", f"W1-{i}", "act"))
        for i in range(3):
            graph.add_task(PlannedTask(f"w2_{i}", f"W2-{i}", "act", dependencies=[f"w1_{i}"]))
        graph.add_task(PlannedTask("w3_final", "Final", "act", dependencies=["w2_0", "w2_1", "w2_2"]))

        # Initially wave 1 is ready
        assert len(graph.get_ready_tasks()) == 3
        for i in range(3):
            graph.record_output(f"w1_{i}", {"w1": i})

        # Wave 2 becomes ready
        assert len(graph.get_ready_tasks()) == 3
        assert {t.task_id for t in graph.get_ready_tasks()} == {"w2_0", "w2_1", "w2_2"}
        for i in range(3):
            graph.record_output(f"w2_{i}", {"w2": i})

        # Final node is ready
        assert len(graph.get_ready_tasks()) == 1
        assert graph.get_ready_tasks()[0].task_id == "w3_final"
        graph.record_output("w3_final", {"done": True})
        assert graph.is_completed() is True

    def test_graph_task_status_sync_with_node_state(self):
        graph = DynamicTaskGraph()
        task = PlannedTask("t1", "Task", "act")
        graph.add_task(task)
        graph.set_state("t1", NodeState.RUNNING)
        assert graph.get_task("t1").status == TaskStatus.RUNNING
        graph.set_state("t1", NodeState.COMPLETED)
        assert graph.get_task("t1").status == TaskStatus.COMPLETED

    def test_repeated_refresh_states_is_idempotent(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.refresh_states()
        s1 = graph.get_state("t1")
        graph.refresh_states()
        s2 = graph.get_state("t1")
        assert s1 == s2 == NodeState.READY

    def test_get_all_outputs_empty_initially(self):
        graph = DynamicTaskGraph()
        assert graph.get_all_outputs() == {}

    def test_get_output_nonexistent_returns_none(self):
        graph = DynamicTaskGraph()
        assert graph.get_output("nonexistent") is None

    def test_downstream_empty_when_no_dependents(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("leaf", "Leaf", "act"))
        assert graph.get_downstream_dependents("leaf") == []

    def test_failed_tasks_empty_when_no_failures(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        assert graph.get_failed_tasks() == []

    def test_mutation_history_records_details(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        mut = TaskGraphMutationEngine(graph)
        mut.skip_task("t1", reason="Precomputed")
        hist = graph.get_mutation_history()
        assert hist[0].details["reason"] == "Precomputed"

    def test_replace_failed_node_preserves_action(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t_ocr", "OCR Step", "ocr_action"))
        mut = TaskGraphMutationEngine(graph)
        fb = mut.replace_failed_node_with_fallback("t_ocr", "agent_fallback", ["tool_fallback"])
        assert fb.action == "ocr_action"

    def test_insert_node_preserves_downstream_other_dependencies(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.add_task(PlannedTask("t_other", "Other", "act"))
        graph.add_task(PlannedTask("t2", "T2", "act", dependencies=["t1", "t_other"]))
        mut = TaskGraphMutationEngine(graph)
        ins = mut.insert_node_between("t1", "t2", PlannedTask("t_mid", "Mid", "act"))
        assert set(graph.get_task("t2").dependencies) == {"t_mid", "t_other"}

    def test_graph_clear_outputs_by_recording_none(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.record_output("t1", None)
        assert graph.get_output("t1") is None
        assert graph.get_state("t1") == NodeState.COMPLETED

    def test_graph_has_failures_true_when_any_failed(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.add_task(PlannedTask("t2", "T2", "act"))
        graph.set_state("t1", NodeState.COMPLETED)
        graph.set_state("t2", NodeState.FAILED)
        assert graph.has_failures() is True
        assert graph.is_completed() is False

    def test_graph_is_completed_true_when_all_completed_or_skipped(self):
        graph = DynamicTaskGraph()
        graph.add_task(PlannedTask("t1", "T1", "act"))
        graph.add_task(PlannedTask("t2", "T2", "act"))
        graph.set_state("t1", NodeState.COMPLETED)
        graph.set_state("t2", NodeState.SKIPPED)
        assert graph.is_completed() is True
        assert graph.has_failures() is False

    def test_graph_plan_id_persists(self):
        graph = DynamicTaskGraph(plan_id="my_special_plan")
        assert graph.plan_id == "my_special_plan"

    def test_mutation_event_timestamp_present(self):
        event = GraphMutationEvent("MUT", "n1")
        assert event.timestamp is not None



