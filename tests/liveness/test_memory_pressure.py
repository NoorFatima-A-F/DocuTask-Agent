"""
Tests for Resource and Memory Health (Parts 6 & 7).
"""
import pytest
from app.platform_verification.liveness.resources.resource_monitor import ResourceMonitor


def test_resource_monitor_healthy():
    monitor = ResourceMonitor()
    report = monitor.check_resource_health()

    assert report.memory_rss_mb > 0.0
    assert report.memory_heap_mb > 0.0
    assert report.memory_state in ["NORMAL", "WARNING", "CRITICAL", "UNHEALTHY"]
    assert isinstance(report.cpu_usage_pct, float)
    assert report.cpu_throttled is False
    assert report.passed is True
