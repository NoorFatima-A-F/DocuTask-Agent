"""
DocuTask Agent - Domain Event Platform Pytest Suite (ARODP)
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.runtime.events import (
    DomainEvent,
    DomainEventType,
    EventSubsystem,
    MissionEventFactory,
    PlannerEventFactory,
    WorkerEventFactory,
    AsyncDomainEventBus,
    DomainEventStore,
    AppendOnlyEventLog,
    planner_projection,
    mission_projection,
    worker_projection,
    dashboard_projection,
    EventSerializer,
    CausationDAGBuilder,
    EventFilterEngine,
    EventFilterCriteria,
    EventIndexTree,
)


@pytest.fixture
def client():
    return TestClient(app)


# --- 1. Universal Domain Event Model Tests ---

def test_domain_event_creation_and_hash():
    event = DomainEvent(
        mission_id="mission-test-001",
        event_type=DomainEventType.MISSION_CREATED,
        subsystem=EventSubsystem.MISSION_CONTROL,
        component="TestComponent",
        payload={"goal": "Process Invoices"},
    )
    assert event.event_id.startswith("evt-")
    assert event.evidence_hash is not None
    assert len(event.evidence_hash) == 64  # SHA-256 length

    d = event.to_dict()
    assert d["mission_id"] == "mission-test-001"
    assert d["event_type"] == "MissionCreated"

    restored = DomainEvent.from_dict(d)
    assert restored.event_id == event.event_id
    assert restored.event_type == DomainEventType.MISSION_CREATED


def test_event_serialization():
    event = MissionEventFactory.created("m-123", "Extract data")
    json_str = EventSerializer.serialize_json(event)
    assert "Extract data" in json_str

    deserialized = EventSerializer.deserialize_json(json_str)
    assert deserialized.mission_id == "m-123"
    assert deserialized.event_type == DomainEventType.MISSION_CREATED


# --- 2. Event Bus Pub/Sub Tests ---

@pytest.mark.asyncio
async def test_async_event_bus_pub_sub():
    bus = AsyncDomainEventBus()
    received = []

    async def test_handler(event: DomainEvent):
        received.append(event)

    bus.subscribe(
        subscriber_id="sub-test-1",
        handler=test_handler,
        event_types={DomainEventType.PLANNER_STARTED},
    )

    ev1 = PlannerEventFactory.started("m-100", "Goal 1")
    ev2 = MissionEventFactory.created("m-100", "Goal 1")

    await bus.publish(ev1)
    await bus.publish(ev2)  # Should not be received (filtered out)

    assert len(received) == 1
    assert received[0].event_type == DomainEventType.PLANNER_STARTED

    bus.unsubscribe("sub-test-1")
    assert len(bus._subscribers) == 0


# --- 3. Event Store & Append Log Tests ---

@pytest.mark.asyncio
async def test_append_only_log_and_hash_chain():
    log = AppendOnlyEventLog(partition_id="part-1")
    ev1 = MissionEventFactory.created("m-1", "Step 1")
    ev2 = PlannerEventFactory.started("m-1", "Step 2")

    offset1 = log.append(ev1)
    offset2 = log.append(ev2)

    assert offset1 == 0
    assert offset2 == 1
    assert ev1.truth_ledger_hash is not None
    assert ev2.truth_ledger_hash is not None
    assert ev1.truth_ledger_hash != ev2.truth_ledger_hash
    assert log.verify_integrity() is True


@pytest.mark.asyncio
async def test_domain_event_store_queries():
    store = DomainEventStore()
    m_id = "mission-store-test"

    ev1 = MissionEventFactory.created(m_id, "Goal A")
    ev2 = PlannerEventFactory.started(m_id, "Goal A")
    ev3 = WorkerEventFactory.task_completed(m_id, "task-1", "worker-1", 45.0)

    await store.append(ev1)
    await store.append(ev2)
    await store.append(ev3)

    # Query by mission
    mission_events = store.get_by_mission(m_id)
    assert len(mission_events) == 3

    # Query by ID
    single = store.get_by_id(ev2.event_id)
    assert single is not None
    assert single.event_type == DomainEventType.PLANNER_STARTED

    # Store stats
    stats = store.get_store_stats()
    assert stats["total_events_stored"] >= 3
    assert stats["integrity_verified"] is True


# --- 4. Projections Tests ---

def test_planner_projection():
    proj = planner_projection
    ev_start = PlannerEventFactory.started("m-proj", "Analyze document")
    ev_finish = PlannerEventFactory.finished("m-proj", task_count=5, estimated_cost_usd=0.0025, critical_path_latency_ms=120.0)
    ev_replan = PlannerEventFactory.replanned("m-proj", reason="Worker timeout", mutated_nodes=["node-2"])

    proj.apply_event(ev_start)
    assert proj.state == "PLANNING"

    proj.apply_event(ev_finish)
    assert proj.state == "EXECUTION_READY"
    assert proj.generated_tasks_count == 5

    proj.apply_event(ev_replan)
    assert proj.total_replans_executed >= 1

    state = proj.get_projection_state()
    assert state["total_plans_generated"] >= 1
    assert state["estimated_cost_usd"] > 0.0


def test_mission_and_worker_projections():
    m_proj = mission_projection
    w_proj = worker_projection

    ev_m_created = MissionEventFactory.created("m-w-test", "OCR Mission")
    ev_t_assigned = WorkerEventFactory.task_assigned("m-w-test", "task-10", "worker-alpha", "OCR")
    ev_t_done = WorkerEventFactory.task_completed("m-w-test", "task-10", "worker-alpha", duration_ms=85.0, tokens_used=150)
    ev_m_done = MissionEventFactory.completed("m-w-test", total_tasks=1, duration_seconds=1.2, cost_usd=0.001)

    m_proj.apply_event(ev_m_created)
    m_proj.apply_event(ev_t_assigned)
    m_proj.apply_event(ev_t_done)
    m_proj.apply_event(ev_m_done)

    w_proj.apply_event(ev_t_assigned)
    w_proj.apply_event(ev_t_done)

    m_state = m_proj.get_mission_state("m-w-test")
    assert m_state is not None
    assert m_state["status"] == "COMPLETED"
    assert m_state["tasks_completed"] == 1

    w_pool = w_proj.get_worker_pool_state()
    assert w_pool["total_workers"] >= 1
    assert w_pool["total_tasks_executed"] >= 1


def test_telemetry_and_dashboard_projections():
    dash = dashboard_projection
    ev = WorkerEventFactory.task_completed("m-dash", "task-1", "worker-1", duration_ms=45.0)
    dash.apply_event(ev)

    dash_state = dash.get_composite_dashboard_state()
    assert "planner" in dash_state
    assert "missions" in dash_state
    assert "workers" in dash_state
    assert "telemetry" in dash_state
    assert dash_state["zero_fabrication_verified"] is True


# --- 5. Correlation & Causation Tests ---

def test_causation_dag_builder():
    ev_root = MissionEventFactory.created("m-corr", "Root")
    ev_child1 = PlannerEventFactory.started("m-corr", "Plan", parent_event_id=ev_root.event_id)
    ev_child2 = WorkerEventFactory.task_assigned("m-corr", "t-1", "w-1", "OCR", parent_event_id=ev_child1.event_id)

    tree = CausationDAGBuilder.build_causation_tree([ev_root, ev_child1, ev_child2])
    assert tree["total_nodes"] == 3
    assert tree["root_events_count"] == 1
    assert len(tree["tree"][0]["children"]) == 1
    assert tree["tree"][0]["children"][0]["children"][0]["event_id"] == ev_child2.event_id


# --- 6. Filtering & Indexing Tests ---

def test_event_filtering_and_indexing():
    ev1 = MissionEventFactory.created("m-filter", "Goal")
    ev2 = PlannerEventFactory.started("m-filter", "Plan")

    # Index
    idx_tree = EventIndexTree()
    idx_tree.index_event(ev1)
    idx_tree.index_event(ev2)

    assert len(idx_tree.get_event_ids_by_mission("m-filter")) == 2

    # Filter
    criteria = EventFilterCriteria(event_types={"PlannerStarted"})
    filtered = EventFilterEngine.filter_events([ev1, ev2], criteria)
    assert len(filtered) == 1
    assert filtered[0].event_type == DomainEventType.PLANNER_STARTED


# --- 7. REST API Endpoints Tests ---

def test_api_publish_and_query_events(client):
    # Publish event
    res_pub = client.post("/api/v1/events/publish", json={
        "mission_id": "mission-api-test-001",
        "event_type": "MissionCreated",
        "subsystem": "MISSION_CONTROL",
        "component": "APIController",
        "actor_id": "test-admin",
        "actor_type": "HUMAN",
        "payload": {"goal": "Audit 2026 Invoices"},
    })
    assert res_pub.status_code == 200
    pub_event = res_pub.json()["event"]
    assert pub_event["mission_id"] == "mission-api-test-001"
    e_id = pub_event["event_id"]

    # Query by mission
    res_m = client.get("/api/v1/events/missions/mission-api-test-001")
    assert res_m.status_code == 200
    assert res_m.json()["total_returned"] >= 1

    # Query single event by ID
    res_single = client.get(f"/api/v1/events/events/{e_id}")
    assert res_single.status_code == 200
    assert res_single.json()["event"]["event_id"] == e_id

    # Query timeline
    res_tl = client.get("/api/v1/events/timeline")
    assert res_tl.status_code == 200

    # Filter endpoint
    res_flt = client.post("/api/v1/events/filter", json={
        "mission_id": "mission-api-test-001",
        "event_types": ["MissionCreated"],
    })
    assert res_flt.status_code == 200
    assert res_flt.json()["total_matched"] >= 1


def test_api_projections_and_metrics(client):
    res_pl = client.get("/api/v1/events/planner")
    assert res_pl.status_code == 200
    assert "planner_projection" in res_pl.json()

    res_wk = client.get("/api/v1/events/workers")
    assert res_wk.status_code == 200
    assert "worker_projection" in res_wk.json()

    res_tel = client.get("/api/v1/events/telemetry")
    assert res_tel.status_code == 200
    assert "telemetry_projection" in res_tel.json()

    res_dash = client.get("/api/v1/events/dashboard")
    assert res_dash.status_code == 200
    assert "dashboard" in res_dash.json()

    res_met = client.get("/api/v1/events/metrics")
    assert res_met.status_code == 200
    assert res_met.json()["overall_health"] == "OPTIMAL_ACTIVE"
