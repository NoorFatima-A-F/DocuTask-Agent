"""
Tests for Internal Runtime Responsiveness (Part 3H.2C).
"""
import pytest
from app.platform_verification.liveness.responsiveness.responsiveness_verifier import (
    ResponsivenessVerifier,
)


def test_responsiveness_benchmark():
    verifier = ResponsivenessVerifier(threshold_ms=500.0)
    report = verifier.verify_responsiveness(probe_count=10)

    assert report.endpoint_tested == "/live"
    assert report.average_latency_ms < 500.0
    assert report.max_latency_ms < 500.0
    assert report.timeouts_count == 0
    assert report.responsive is True
    assert report.passed is True


def test_responsiveness_timeout_detection():
    # Artificially low threshold to test timeout branch
    verifier = ResponsivenessVerifier(threshold_ms=0.000001)
    report = verifier.verify_responsiveness(probe_count=5)

    assert report.timeouts_count > 0
    assert report.responsive is False
    assert report.passed is False
