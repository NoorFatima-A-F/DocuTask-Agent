"""
Tests for Async Event Loop Health (Part 3).
"""
from app.platform_verification.liveness.event_loop.event_loop_monitor import (
    EventLoopMonitor,
)


def test_event_loop_monitor():
    monitor = EventLoopMonitor(failure_threshold_ms=5000.0, heartbeat_interval_seconds=5.0)
    report = monitor.monitor_event_loop()

    assert report.average_latency_ms < 5000.0
    assert report.maximum_latency_ms < 5000.0
    assert report.loop_healthy is True
    assert report.passed is True
    assert "status" in report.details
