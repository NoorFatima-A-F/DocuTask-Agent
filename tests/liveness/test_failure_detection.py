"""
Tests for Deadlock Detection and Liveness Failure Simulations (Parts 4 & 11).
"""
import pytest
from app.platform_verification.liveness.deadlock.deadlock_detector import DeadlockDetector
from app.platform_verification.liveness.failure_injection.liveness_failure_injector import (
    LivenessFailureInjector,
)


def test_deadlock_detector():
    detector = DeadlockDetector()
    report = detector.detect_deadlocks()

    assert report.deadlock_detected is False
    assert report.watchdog_active is True
    assert report.frozen_threads_count == 0
    assert report.restart_signal_generated is False
    assert report.passed is True


def test_failure_simulator():
    injector = LivenessFailureInjector()
    report = injector.execute_failure_simulations()

    assert report.total_simulations == 4
    assert report.passed_simulations == 4
    assert report.process_kill_handled is True
    assert report.event_loop_freeze_handled is True
    assert report.memory_exhaustion_handled is True
    assert report.worker_deadlock_handled is True
    assert report.passed is True
