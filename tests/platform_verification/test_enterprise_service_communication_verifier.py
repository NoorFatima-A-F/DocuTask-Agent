"""
Comprehensive Test Suite for Part 3B: Enterprise Service Communication & Distributed System Verification Framework.
"""
import pytest
from app.platform_verification.service_communication.runtime.service_communication_runtime import ServiceCommunicationRuntime
from app.platform_verification.service_communication.domain.models import (
    DistributedCertificationTier,
    ServiceDependencyNode,
    ServiceDependencyGraph,
    CommunicationProtocol,
)


@pytest.fixture
def comm_runtime():
    return ServiceCommunicationRuntime()


def test_service_dependency_graph_and_cycle_detection(comm_runtime):
    """Verifies dependency graph topology analysis, complexity scoring, and circular dependency detection."""
    # Acyclic graph
    acyclic_nodes = {
        "gateway": ServiceDependencyNode(name="gateway", protocol=CommunicationProtocol.HTTP_REST, depends_on=["api"]),
        "api": ServiceDependencyNode(name="api", protocol=CommunicationProtocol.HTTP_REST, depends_on=["db", "queue"]),
        "db": ServiceDependencyNode(name="db", protocol=CommunicationProtocol.SQL_CONNECTION, depends_on=[]),
        "queue": ServiceDependencyNode(name="queue", protocol=CommunicationProtocol.REDIS_QUEUE, depends_on=[]),
    }
    acyclic_graph = ServiceDependencyGraph(nodes=acyclic_nodes)
    rep = comm_runtime.graph_analyzer.analyze_dependencies(acyclic_graph)
    assert rep.status == "PASS"
    assert len(rep.circular_dependencies) == 0
    assert rep.dependency_complexity_score >= 80.0

    # Cyclic graph (API -> Worker -> API)
    cyclic_nodes = {
        "api": ServiceDependencyNode(name="api", protocol=CommunicationProtocol.HTTP_REST, depends_on=["worker"]),
        "worker": ServiceDependencyNode(name="worker", protocol=CommunicationProtocol.HTTP_REST, depends_on=["api"]),
    }
    cyclic_graph = ServiceDependencyGraph(nodes=cyclic_nodes)
    fail_rep = comm_runtime.graph_analyzer.analyze_dependencies(cyclic_graph)
    assert fail_rep.status == "FAIL"
    assert len(fail_rep.circular_dependencies) > 0


def test_communication_contract_validator(comm_runtime):
    """Verifies request/response schema validation and detects undocumented fields/breaking changes."""
    clean_contracts = [
        {"endpoint": "/api/v1/extract", "request_schema": {"id": "str"}, "response_schema": {"status": "str"}}
    ]
    clean_rep = comm_runtime.contract_validator.validate_contracts(clean_contracts)
    assert clean_rep.status == "PASS"
    assert clean_rep.schema_validation_passed

    breaking_contracts = [
        {"endpoint": "/api/v1/extract", "request_schema": {}, "response_schema": {}, "has_breaking_change": True, "breaking_reason": "removed field"}
    ]
    break_rep = comm_runtime.contract_validator.validate_contracts(breaking_contracts)
    assert break_rep.status == "FAIL"
    assert len(break_rep.breaking_changes) == 1
    assert len(break_rep.undocumented_fields) == 1


def test_timeout_and_exponential_backoff_retry_engine(comm_runtime):
    """Evaluates timeouts, exponential backoff with jitter, and retry storm prevention."""
    valid_configs = [
        {"name": "gemini", "timeout_seconds": 15.0, "backoff_strategy": "exponential", "jitter_enabled": True, "max_retries": 3}
    ]
    t_rep, r_rep = comm_runtime.timeout_retry_engine.evaluate_timeouts_and_retries(valid_configs)
    assert t_rep.status == "PASS"
    assert r_rep.status == "PASS"
    assert r_rep.exponential_backoff_verified
    assert r_rep.jitter_verified

    risky_configs = [
        {"name": "unbounded", "timeout_seconds": 0.0, "backoff_strategy": "linear", "jitter_enabled": False, "max_retries": 10}
    ]
    bad_t, bad_r = comm_runtime.timeout_retry_engine.evaluate_timeouts_and_retries(risky_configs)
    assert bad_t.status == "FAIL"
    assert bad_r.status == "FAIL"


def test_circuit_breaker_state_machine_tester(comm_runtime):
    """Tests circuit breaker 3-state transitions and fast failure on open circuit."""
    # Under threshold -> Closed
    normal_rep = comm_runtime.circuit_breaker_tester.test_circuit_breaker("ai_provider", 2)
    assert normal_rep.status == "PASS"

    # Exceeding threshold -> Open -> fast fail
    tripped_rep = comm_runtime.circuit_breaker_tester.test_circuit_breaker("ai_provider", 5)
    assert tripped_rep.status == "PASS"
    assert tripped_rep.fast_failure_on_open_verified
    assert tripped_rep.half_open_probe_verified


def test_network_chaos_failure_simulator(comm_runtime):
    """Verifies network latency spikes, packet loss, and severed connection handling."""
    good_scenarios = [
        {"scenario": "latency_spike", "fault_type": "latency", "gracefully_recovered": True},
        {"scenario": "packet_loss", "fault_type": "packet_loss", "gracefully_recovered": True},
        {"scenario": "connection_drop", "fault_type": "connection_drop", "gracefully_recovered": True},
    ]
    good_rep = comm_runtime.network_simulator.simulate_network_failures(good_scenarios)
    assert good_rep.status == "PASS"

    bad_scenarios = [
        {"scenario": "latency_spike", "fault_type": "latency", "gracefully_recovered": False},
    ]
    bad_rep = comm_runtime.network_simulator.simulate_network_failures(bad_scenarios)
    assert bad_rep.status == "FAIL"
    assert len(bad_rep.issues) == 1


def test_distributed_consistency_and_idempotency_verifier(comm_runtime):
    """Tests idempotency keys, compensation transactions, and orphan document prevention."""
    consistent_wf = [
        {"name": "doc_pipeline", "uses_idempotency_key": True, "orphan_records_created_on_crash": False, "duplicate_queue_task_on_retry": False, "has_compensation_rollback": True}
    ]
    cons_rep = comm_runtime.consistency_verifier.verify_consistency(consistent_wf)
    assert cons_rep.status == "PASS"
    assert cons_rep.idempotency_keys_enforced

    inconsistent_wf = [
        {"name": "bad_pipeline", "uses_idempotency_key": False, "orphan_records_created_on_crash": True, "duplicate_queue_task_on_retry": True, "has_compensation_rollback": False}
    ]
    fail_rep = comm_runtime.consistency_verifier.verify_consistency(inconsistent_wf)
    assert fail_rep.status == "FAIL"


def test_traceability_validator(comm_runtime):
    """Verifies propagation of request_id, trace_id, and correlation_id across all spans."""
    clean_spans = [
        {"span_name": "api_gateway", "request_id": "r1", "trace_id": "t1", "correlation_id": "c1"},
        {"span_name": "worker", "request_id": "r1", "trace_id": "t1", "correlation_id": "c1"},
    ]
    trace_rep = comm_runtime.traceability_validator.validate_traceability(clean_spans)
    assert trace_rep.status == "PASS"
    assert trace_rep.reconstructability_score == 100.0

    broken_spans = [
        {"span_name": "api_gateway", "request_id": "r1", "trace_id": "", "correlation_id": "c1"},
    ]
    bad_trace = comm_runtime.traceability_validator.validate_traceability(broken_spans)
    assert bad_trace.status == "FAIL"
    assert len(bad_trace.untraceable_spans) > 0


def test_end_to_end_service_communication_verification_and_api(comm_runtime):
    """Tests end-to-end full execution, evidence sealing, and in-process REST API."""
    package = comm_runtime.run_full_verification(commit_sha="git-commit-3b-55")
    assert package.scorecard.composite_score >= 90.0
    assert package.scorecard.tier in [DistributedCertificationTier.ENTERPRISE_DISTRIBUTED_SYSTEM_READY, DistributedCertificationTier.PRODUCTION_READY]
    assert package.package_sha256 != ""

    api = comm_runtime.api
    scan_res = api.post_scan({"commit_sha": "git-commit-3b-55"})
    assert scan_res["status"] == "COMPLETED"
    assert "package_id" in scan_res

    report_res = api.get_report(scan_res["package_id"])
    assert report_res is not None
    assert "scorecard" in report_res
    assert report_res["commit_sha"] == "git-commit-3b-55"

    metrics_res = api.get_metrics()
    assert "supported_protocols" in metrics_res
