"""
Property-Based & Invariant Verification Test Suite.
Generates randomized DAG structures, randomized audit chains, and randomized session trees
to prove fundamental distributed systems properties:
1. Kahn topological order property: in any valid DAG, no edge points backward.
2. Cycle detection property: any graph with a directed back-edge is identified as cyclic.
3. Tamper-evident property: altering any byte in an audit chain invalidates verification.
4. Session tree property: all descendant sessions trace back to the unique root session_id.
"""

import hashlib
import json
import random
from uuid import uuid4
import pytest
from app.agents.runtime.dependency_graph import CircularDependencyError, DependencyGraph
from app.agents.runtime.enterprise.audit_event import AuditEventType
from app.agents.runtime.enterprise.audit_log import ImmutableRuntimeAuditLog
from app.agents.runtime.runtime_session import RuntimeSession


def test_property_dag_topological_sort_invariants():
    """Generates 50 randomized DAGs and proves topological ordering invariant."""
    random.seed(42)

    for run_idx in range(50):
        graph = DependencyGraph()
        num_nodes = random.randint(5, 20)
        node_names = [f"mod_{i}" for i in range(num_nodes)]

        # Add nodes
        for name in node_names:
            graph.add_node(name)

        # Add forward-only edges to guarantee DAG (i > j where i depends on j)
        edges = []
        for i in range(1, num_nodes):
            # Pick random number of prerequisites from preceding indices
            num_prereqs = random.randint(0, min(3, i))
            prereqs = random.sample(range(i), num_prereqs)
            for p in prereqs:
                mod = node_names[i]
                prereq = node_names[p]
                graph.add_dependency(mod, prereq)
                edges.append((mod, prereq))

        # Must not have cycles
        assert not graph.has_cycles(), f"Run {run_idx} falsely flagged cycle in DAG"
        assert graph.find_cycle() is None

        # Resolve order
        order = graph.get_resolution_order()
        assert len(order) == num_nodes
        assert set(order) == set(node_names)

        # INVARIANT: For every dependency (mod depends on prereq), prereq MUST precede mod
        pos = {node: idx for idx, node in enumerate(order)}
        for mod, prereq in edges:
            assert pos[prereq] < pos[mod], f"Violation in run {run_idx}: {prereq} at {pos[prereq]} >= {mod} at {pos[mod]}"


def test_property_dag_cycle_injection_invariants():
    """Generates 50 random DAGs, injects a back-edge cycle, and proves detection."""
    random.seed(1337)

    for run_idx in range(50):
        graph = DependencyGraph()
        num_nodes = random.randint(4, 15)
        node_names = [f"n_{i}" for i in range(num_nodes)]

        # Create chain: n_0 <- n_1 <- n_2 ...
        for i in range(1, num_nodes):
            graph.add_dependency(node_names[i], node_names[i - 1])

        # Inject back-edge cycle: n_0 depends on n_{last}
        last_idx = num_nodes - 1
        graph.add_dependency(node_names[0], node_names[last_idx])

        # INVARIANT: Graph MUST be detected as cyclic
        assert graph.has_cycles(), f"Run {run_idx} failed to detect cycle"
        cycle = graph.find_cycle()
        assert cycle is not None
        assert len(cycle) >= 2

        with pytest.raises(CircularDependencyError) as exc_info:
            graph.get_resolution_order()
        assert len(exc_info.value.cycle_path) >= 2


def test_property_audit_chain_tamper_evidence():
    """Generates 50 random audit chains and proves tamper detection on arbitrary mutation."""
    random.seed(999)

    for run_idx in range(50):
        log = ImmutableRuntimeAuditLog()
        chain_len = random.randint(3, 10)

        for i in range(chain_len):
            log.append(
                event_type=AuditEventType.TENANT_ACTION,
                actor=f"user_{i}@test.com",
                details={"action_id": i, "random_val": random.random()},
                tenant_id=f"tenant_{i % 3}",
            )

        # Valid chain
        assert log.verify_integrity(), f"Run {run_idx} valid chain failed verification"

        # Mutate a random event
        tamper_idx = random.randint(0, chain_len - 1)
        events = log._events
        orig_details = events[tamper_idx].details
        tampered_details = dict(orig_details)
        tampered_details["tampered"] = True
        events[tamper_idx] = events[tamper_idx].model_copy(update={"details": tampered_details})

        # INVARIANT: Must detect tampering
        assert not log.verify_integrity(), f"Run {run_idx} failed to detect tampering at index {tamper_idx}"


def test_property_session_tree_lineage():
    """Spawns deep random session trees and proves hierarchical lineage."""
    random.seed(777)

    root = RuntimeSession()
    all_sessions = [root]

    # Grow tree up to 30 nodes
    for i in range(30):
        parent = random.choice(all_sessions)
        child = parent.spawn_child_session(agent_id=f"agent_{i}")
        all_sessions.append(child)

    # INVARIANT: Every non-root session has a valid parent in the tree
    session_map = {s.session_id: s for s in all_sessions}
    for s in all_sessions:
        if s.session_id == root.session_id:
            assert s.parent_session_id is None
        else:
            assert s.parent_session_id in session_map
            # Trace up to root
            curr = s
            depth = 0
            while curr.parent_session_id is not None and depth < 50:
                curr = session_map[curr.parent_session_id]
                depth += 1
            assert curr.session_id == root.session_id
