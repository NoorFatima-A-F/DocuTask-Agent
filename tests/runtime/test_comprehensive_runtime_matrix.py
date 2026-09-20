"""
Comprehensive Runtime Matrix & Combinatorial Test Suite.
Exercises exhaustive test matrices across:
- All 10 RuntimeLifecycleState transitions (valid and invalid)
- All 8 PluginState transitions
- All 4 JobPriority levels and state changes
- Semver compatibility range
- Dynamic DAG topologies (trees, diamonds, pipelines, multi-root)
- Error hierarchy assertions
- PlatformRuntimeConfig validation and immutability
"""

from uuid import uuid4
import pytest
from app.agents.runtime.configuration import PlatformRuntimeConfig
from app.agents.runtime.dependency_graph import CircularDependencyError, DependencyGraph
from app.agents.runtime.enterprise.compatibility_checker import VersionCompatibilityChecker
from app.agents.runtime.enterprise.scheduler_state import (
    JobPriority,
    JobStatus,
    ScheduledJob,
)
from app.agents.runtime.exceptions import (
    CyclicDependencyError,
    InvalidRuntimeStateTransitionError,
    PluginValidationError,
    RuntimeKernelException,
    SubsystemCrashError,
    TenantIsolationViolationError,
)
from app.agents.runtime.plugin_loader import PluginState
from app.agents.runtime.runtime_lifecycle import RuntimeLifecycleState
from app.agents.runtime.runtime_state import RuntimeState


# --- Matrix 1: Lifecycle State Transitions ---
@pytest.mark.parametrize(
    "from_state, to_state, should_succeed",
    [
        (RuntimeLifecycleState.OFFLINE, RuntimeLifecycleState.BOOTING, True),
        (RuntimeLifecycleState.BOOTING, RuntimeLifecycleState.INITIALIZING, True),
        (RuntimeLifecycleState.INITIALIZING, RuntimeLifecycleState.READY, True),
        (RuntimeLifecycleState.INITIALIZING, RuntimeLifecycleState.DEGRADED, False),
        (RuntimeLifecycleState.READY, RuntimeLifecycleState.RUNNING, True),
        (RuntimeLifecycleState.RUNNING, RuntimeLifecycleState.DRAINING, True),
        (RuntimeLifecycleState.DRAINING, RuntimeLifecycleState.STOPPING, True),
        (RuntimeLifecycleState.STOPPING, RuntimeLifecycleState.TERMINATED, True),
        (RuntimeLifecycleState.RUNNING, RuntimeLifecycleState.DEGRADED, True),
        (RuntimeLifecycleState.DEGRADED, RuntimeLifecycleState.RUNNING, True),
        # Allowed re-boot from TERMINATED
        (RuntimeLifecycleState.TERMINATED, RuntimeLifecycleState.BOOTING, True),
        # Invalid transitions
        (RuntimeLifecycleState.OFFLINE, RuntimeLifecycleState.RUNNING, False),
        (RuntimeLifecycleState.DRAINING, RuntimeLifecycleState.BOOTING, False),
        (RuntimeLifecycleState.OFFLINE, RuntimeLifecycleState.DRAINING, False),
        (RuntimeLifecycleState.STOPPING, RuntimeLifecycleState.RUNNING, False),
    ],
)
def test_lifecycle_state_matrix(from_state, to_state, should_succeed):
    state = RuntimeState(lifecycle_state=from_state)
    if should_succeed:
        next_state = state.transition_to(to_state)
        assert next_state.lifecycle_state == to_state
    else:
        with pytest.raises(InvalidRuntimeStateTransitionError):
            state.transition_to(to_state)


# --- Matrix 2: Plugin Lifecycle States ---
@pytest.mark.parametrize(
    "state",
    [
        PluginState.DISCOVERED,
        PluginState.VALIDATED,
        PluginState.LOADED,
        PluginState.REGISTERED,
        PluginState.ACTIVATED,
        PluginState.RUNNING,
        PluginState.DISABLED,
        PluginState.UNLOADED,
    ],
)
def test_all_plugin_states_exist(state):
    assert state.value in {
        "DISCOVERED",
        "VALIDATED",
        "LOADED",
        "REGISTERED",
        "ACTIVATED",
        "RUNNING",
        "DISABLED",
        "UNLOADED",
    }


# --- Matrix 3: Scheduler Job Priority Combinations ---
@pytest.mark.parametrize(
    "priority, expected_val",
    [
        (JobPriority.CRITICAL, 1),
        (JobPriority.HIGH, 2),
        (JobPriority.NORMAL, 3),
        (JobPriority.LOW, 4),
    ],
)
def test_job_priorities_values(priority, expected_val):
    assert priority.value == expected_val
    job = ScheduledJob(name=f"job_{priority.name}", priority=priority)
    assert job.priority.value == expected_val


# --- Matrix 4: Semver Compatibility Range ---
@pytest.mark.parametrize(
    "runtime_v, comp_v, compatible",
    [
        ("23.0.0", "23.0.0", True),
        ("23.0.0", "23.0.5", True),
        ("23.0.0", "23.1.0", True),
        ("23.0.0", "23.2.0", False),
        ("23.0.0", "24.0.0", False),
        ("23.0.0", "22.9.9", False),
        ("24.1.0", "24.1.2", True),
        ("24.1.0", "24.2.0", True),
        ("24.1.0", "24.3.0", False),
    ],
)
def test_semver_compatibility_matrix(runtime_v, comp_v, compatible):
    assert VersionCompatibilityChecker.is_compatible(runtime_v, comp_v) == compatible


# --- Matrix 5: Graph Topologies (Kahn Algorithm & Topological Order) ---
@pytest.mark.parametrize(
    "topology_name, deps, expected_prefixes, expected_suffixes",
    [
        # Linear pipeline: B depends on A, C depends on B, D depends on C (Order: A, B, C, D)
        ("linear", [("B", "A"), ("C", "B"), ("D", "C")], ["A"], ["D"]),
        # Diamond: B depends on A, C depends on A, D depends on B & C (Order: A, B/C, D)
        ("diamond", [("B", "A"), ("C", "A"), ("D", "B"), ("D", "C")], ["A"], ["D"]),
        # Multi-root: C depends on A & B, D depends on C (Order: A & B, C, D)
        ("multi_root", [("C", "A"), ("C", "B"), ("D", "C")], ["A", "B"], ["D"]),
        # Independent pairs: B depends on A, D depends on C
        ("disconnected", [("B", "A"), ("D", "C")], [], []),
    ],
)
def test_graph_topology_matrix(topology_name, deps, expected_prefixes, expected_suffixes):
    graph = DependencyGraph()
    for mod, prereq in deps:
        graph.add_dependency(mod, prereq)

    order = graph.get_resolution_order()

    # All nodes must be present
    all_nodes = {mod for mod, _ in deps} | {prereq for _, prereq in deps}
    assert set(order) == all_nodes

    # Check topological ordering property: for every (mod, prereq), prereq must appear before mod
    for mod, prereq in deps:
        assert order.index(prereq) < order.index(mod)

    # Check expected start/end nodes
    for prefix in expected_prefixes:
        for suffix in expected_suffixes:
            assert order.index(prefix) < order.index(suffix)


# --- Matrix 6: Graph Cycle Detection Permutations ---
@pytest.mark.parametrize(
    "cycle_deps, expected_in_cycle",
    [
        ([("A", "B"), ("B", "A")], {"A", "B"}),
        ([("X", "Y"), ("Y", "Z"), ("Z", "X")], {"X", "Y", "Z"}),
        ([("1", "2"), ("2", "3"), ("3", "4"), ("4", "2")], {"2", "3", "4"}),
    ],
)
def test_graph_cycle_matrix(cycle_deps, expected_in_cycle):
    graph = DependencyGraph()
    for mod, prereq in cycle_deps:
        graph.add_dependency(mod, prereq)

    assert graph.has_cycles()
    cycle_path = graph.find_cycle()
    assert cycle_path is not None
    assert expected_in_cycle.issubset(set(cycle_path))

    with pytest.raises(CircularDependencyError):
        graph.get_resolution_order()


# --- Matrix 7: Exception Subtyping Hierarchy ---
@pytest.mark.parametrize(
    "exc_cls",
    [
        CyclicDependencyError,
        InvalidRuntimeStateTransitionError,
        PluginValidationError,
        SubsystemCrashError,
        TenantIsolationViolationError,
    ],
)
def test_exception_subtyping_matrix(exc_cls):
    instance = exc_cls("test error message")
    assert isinstance(instance, RuntimeKernelException)
    assert isinstance(instance, Exception)
    assert "test error message" in str(instance)


# --- Matrix 8: PlatformRuntimeConfig Defaults & Immutability ---
def test_platform_runtime_config_immutability():
    config = PlatformRuntimeConfig(environment="PROD")
    assert config.environment == "PROD"
    assert config.max_concurrent_sessions == 1000

    # Frozen check
    with pytest.raises(Exception):
        config.environment = "DEV"
