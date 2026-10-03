"""
Enterprise Backpressure & Admission Controller Test Suite.
Validates:
- BackpressureMonitor state evaluation (NORMAL -> THROTTLED -> SHEDDING)
- AdmissionController priority gating rules
- RequestSheddedError exception raising on rejected intake
"""

import pytest
from app.agents.runtime.enterprise.admission_controller import (
    AdmissionController,
    RequestSheddedError,
)
from app.agents.runtime.enterprise.backpressure import (
    BackpressureMonitor,
    BackpressureState,
)
from app.agents.runtime.enterprise.scheduler_state import JobPriority


def test_backpressure_monitor_states():
    monitor = BackpressureMonitor(throttle_threshold=50, shedding_threshold=200)

    assert monitor.evaluate_state(10) == BackpressureState.NORMAL
    assert monitor.evaluate_state(50) == BackpressureState.THROTTLED
    assert monitor.evaluate_state(150) == BackpressureState.THROTTLED
    assert monitor.evaluate_state(200) == BackpressureState.SHEDDING
    assert monitor.evaluate_state(500) == BackpressureState.SHEDDING


def test_admission_controller_normal():
    ac = AdmissionController(BackpressureMonitor(throttle_threshold=100, shedding_threshold=300))

    # All admitted in NORMAL
    assert ac.can_admit(JobPriority.CRITICAL, current_queue_depth=10)
    assert ac.can_admit(JobPriority.NORMAL, current_queue_depth=10)
    assert ac.can_admit(JobPriority.LOW, current_queue_depth=10)
    # Should not raise
    ac.admit_or_reject(JobPriority.LOW, current_queue_depth=10)


def test_admission_controller_throttled():
    ac = AdmissionController(BackpressureMonitor(throttle_threshold=50, shedding_threshold=150))

    # In THROTTLED: LOW is rejected, CRITICAL & NORMAL accepted
    assert ac.can_admit(JobPriority.CRITICAL, current_queue_depth=75)
    assert ac.can_admit(JobPriority.NORMAL, current_queue_depth=75)
    assert not ac.can_admit(JobPriority.LOW, current_queue_depth=75)

    with pytest.raises(RequestSheddedError) as exc_info:
        ac.admit_or_reject(JobPriority.LOW, current_queue_depth=75)
    assert "was shedded due to backpressure" in str(exc_info.value)


def test_admission_controller_shedding():
    ac = AdmissionController(BackpressureMonitor(throttle_threshold=50, shedding_threshold=100))

    # In SHEDDING: only CRITICAL admitted
    assert ac.can_admit(JobPriority.CRITICAL, current_queue_depth=120)
    assert not ac.can_admit(JobPriority.HIGH, current_queue_depth=120)
    assert not ac.can_admit(JobPriority.NORMAL, current_queue_depth=120)
    assert not ac.can_admit(JobPriority.LOW, current_queue_depth=120)

    with pytest.raises(RequestSheddedError):
        ac.admit_or_reject(JobPriority.NORMAL, current_queue_depth=120)
