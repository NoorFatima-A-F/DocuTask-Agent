"""Tests for Network Telemetry and Flow Log Collection."""

import pytest
from app.infrastructure.networking.telemetry import (
    NetworkTelemetryCollector,
    NetworkFlowLogger,
    NetworkSecurityEventType,
)


def test_network_telemetry_collector_aggregations() -> None:
    collector = NetworkTelemetryCollector()

    collector.record_request(duration_ms=10.0, success=True, bytes_sent=100, bytes_recv=500)
    collector.record_request(duration_ms=20.0, success=True, bytes_sent=200, bytes_recv=800)
    collector.record_request(duration_ms=50.0, success=False, bytes_sent=50, bytes_recv=0, is_retry=True)
    collector.record_policy_denial()
    collector.record_tls_failure()

    summary = collector.get_summary()
    assert summary.total_requests == 3
    assert summary.successful_requests == 2
    assert summary.failed_requests == 1
    assert summary.total_bytes_sent == 350
    assert summary.total_bytes_received == 1300
    assert summary.policy_denials == 1
    assert summary.tls_handshake_failures == 1
    assert summary.retries_count == 1
    assert summary.avg_latency_ms > 0.0


def test_network_flow_logger_and_events() -> None:
    logger = NetworkFlowLogger()
    events_received = []

    logger.add_event_listener(lambda evt: events_received.append(evt))

    flow = logger.record_flow(
        source_address="10.0.1.10",
        destination_address="10.0.2.20",
        source_spiffe="spiffe://docutask.internal/ns/default/sa/svc-a",
        destination_spiffe="spiffe://docutask.internal/ns/default/sa/svc-b",
        action="ALLOW",
        bytes_transferred=1024,
        duration_ms=4.5,
    )
    assert flow.flow_id is not None
    assert len(logger.get_recent_flows()) == 1

    # Emit security event
    logger.emit_security_event(
        event_type=NetworkSecurityEventType.CERTIFICATE_ROTATED,
        source="CA-Engine",
        details={"serial": "ABC-123"},
    )
    assert len(events_received) == 1
    assert events_received[0].event_type == NetworkSecurityEventType.CERTIFICATE_ROTATED
