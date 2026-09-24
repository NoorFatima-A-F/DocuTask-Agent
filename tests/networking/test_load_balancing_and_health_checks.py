"""Tests for Multi-Algorithm Load Balancing and Health Outlier Detection."""

from app.networking.discovery.registry import EndpointHealth, ServiceEndpoint, ServiceRegistry
from app.networking.load_balancing.algorithms import LoadBalancerEngine
from app.networking.load_balancing.health import HealthCheckEngine
from app.networking.routing.policies import LoadBalancingAlgorithm


def test_load_balancer_algorithms():
    lb = LoadBalancerEngine()
    ep1 = ServiceEndpoint(endpoint_id="ep-1", service_name="svc", host="10.0.0.1", port=80, weight=10)
    ep2 = ServiceEndpoint(endpoint_id="ep-2", service_name="svc", host="10.0.0.2", port=80, weight=90)
    endpoints = [ep1, ep2]

    # Round Robin
    res1 = lb.select_endpoint(endpoints, algorithm=LoadBalancingAlgorithm.ROUND_ROBIN)
    res2 = lb.select_endpoint(endpoints, algorithm=LoadBalancingAlgorithm.ROUND_ROBIN)
    assert res1.endpoint_id != res2.endpoint_id

    # Consistent Hashing
    ch1 = lb.select_endpoint(endpoints, algorithm=LoadBalancingAlgorithm.CONSISTENT_HASH, hash_key="tenant-abc")
    ch2 = lb.select_endpoint(endpoints, algorithm=LoadBalancingAlgorithm.CONSISTENT_HASH, hash_key="tenant-abc")
    assert ch1.endpoint_id == ch2.endpoint_id


def test_health_outlier_ejection():
    registry = ServiceRegistry()
    ep = ServiceEndpoint(endpoint_id="ep-flaky", service_name="flaky-svc", host="10.0.0.5", port=80)
    registry.register_endpoint(ep)

    health_engine = HealthCheckEngine(registry=registry)

    # Record 3 consecutive errors
    health_engine.record_call_result("ep-flaky", is_error=True, consecutive_error_threshold=3, ejection_duration_seconds=5.0)
    health_engine.record_call_result("ep-flaky", is_error=True, consecutive_error_threshold=3, ejection_duration_seconds=5.0)
    assert health_engine.is_ejected("ep-flaky") is False

    health_engine.record_call_result("ep-flaky", is_error=True, consecutive_error_threshold=3, ejection_duration_seconds=5.0)
    assert health_engine.is_ejected("ep-flaky") is True
    assert registry.get_endpoint("ep-flaky").health == EndpointHealth.UNHEALTHY
