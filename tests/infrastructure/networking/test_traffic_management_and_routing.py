"""Tests for Traffic Management, Load Balancing, Canary Splits, Retries, and Circuit Breakers."""

import pytest
from app.infrastructure.networking.control_plane import NetworkEndpoint, RouteRule, RoutingStrategy
from app.infrastructure.networking.traffic import (
    LoadBalancerEngine,
    TrafficRouter,
    RetryEngine,
    RetryPolicy,
    CircuitState,
    CircuitBreakerConfig,
    TrafficFailoverManager,
)


def test_load_balancer_algorithms() -> None:
    lb = LoadBalancerEngine()
    ep1 = NetworkEndpoint(host="10.0.0.1", port=443, active_connections=10, latency_ms=25.0)
    ep2 = NetworkEndpoint(host="10.0.0.2", port=443, active_connections=2, latency_ms=8.0)
    ep3 = NetworkEndpoint(host="10.0.0.3", port=443, active_connections=5, latency_ms=15.0)
    endpoints = [ep1, ep2, ep3]

    # Least connections
    least_conn = lb.select_endpoint(endpoints, strategy=RoutingStrategy.LEAST_CONNECTIONS)
    assert least_conn.host == "10.0.0.2"

    # Latency based
    lowest_lat = lb.select_endpoint(endpoints, strategy=RoutingStrategy.LATENCY_BASED)
    assert lowest_lat.host == "10.0.0.2"

    # Round robin
    rr1 = lb.select_endpoint(endpoints, strategy=RoutingStrategy.ROUND_ROBIN, service_key="svc1")
    rr2 = lb.select_endpoint(endpoints, strategy=RoutingStrategy.ROUND_ROBIN, service_key="svc1")
    assert rr1.host == "10.0.0.1"
    assert rr2.host == "10.0.0.2"


def test_traffic_router_canary_and_blue_green() -> None:
    router = TrafficRouter()

    primary_ep = NetworkEndpoint(host="10.0.1.1", port=443, metadata={"version": "blue"})
    canary_ep = NetworkEndpoint(host="10.0.2.1", port=443, metadata={"version": "canary"})

    route = RouteRule(
        rule_id="r_canary",
        service_name="ingestion-api",
        endpoints=[primary_ep],
        canary_endpoints=[canary_ep],
        canary_weight=1.0,  # 100% canary for test determinism
    )

    dec = router.route_request(route)
    assert dec is not None
    assert dec.is_canary is True
    assert dec.target_endpoint.host == "10.0.2.1"


def test_retries_and_circuit_breaker() -> None:
    # Retry engine
    retry_engine = RetryEngine(RetryPolicy(max_attempts=3, retryable_status_codes={503}))
    assert retry_engine.should_retry(1, status_code=503) is True
    assert retry_engine.should_retry(3, status_code=503) is False
    assert retry_engine.should_retry(1, status_code=400) is False

    # Circuit breaker
    cb_mgr = TrafficFailoverManager(CircuitBreakerConfig(consecutive_errors_threshold=3, recovery_time_seconds=1.0))
    ep = NetworkEndpoint(host="10.0.5.1", port=8080)

    assert cb_mgr.can_execute(ep) is True
    cb_mgr.record_failure(ep)
    cb_mgr.record_failure(ep)
    cb_mgr.record_failure(ep)

    assert cb_mgr.get_circuit_state(ep) == CircuitState.OPEN
    assert cb_mgr.can_execute(ep) is False
    assert ep.healthy is False
