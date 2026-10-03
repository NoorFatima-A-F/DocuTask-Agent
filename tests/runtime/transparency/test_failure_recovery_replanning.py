"""
Test Suite: Failure Recovery & Chaos Fault Injection
Validates runtime fault injection, dynamic subgraph replanning, and autonomous self-healing execution.
"""
import pytest
from app.runtime.failure_recovery.chaos_injector import ChaosFaultInjector
from app.runtime.failure_recovery.recovery_orchestrator import AutonomousRecoveryOrchestrator


def test_chaos_fault_injection_lifecycle():
    injector = ChaosFaultInjector()
    
    faults = injector.list_faults()
    assert len(faults) >= 3
    assert any(f["fault_id"] == "fault_ocr_crash" for f in faults)

    triggered = injector.trigger_fault("fault_ocr_crash")
    assert triggered.injected is True
    assert triggered.injected_at is not None

    with pytest.raises(ValueError):
        injector.trigger_fault("non_existent_fault")


def test_autonomous_recovery_orchestration_actions():
    orchestrator = AutonomousRecoveryOrchestrator()
    
    # Test OCR crash recovery
    ocr_rec = orchestrator.handle_task_failure("m1", "t_ocr_1", "PROCESS_CRASH")
    assert ocr_rec.recovery_action == "ALTERNATE_OCR_FALLBACK"
    assert "task_ocr_tesseract_fallback" in ocr_rec.new_subgraph_nodes
    assert ocr_rec.is_resumed_successfully is True

    # Test 429 Rate limit recovery
    rate_rec = orchestrator.handle_task_failure("m1", "t_llm_1", "HTTP_429_RATE_LIMIT")
    assert rate_rec.recovery_action == "EXPONENTIAL_BACKOFF_RETRY"
    assert "task_flash_lite_route" in rate_rec.new_subgraph_nodes

    # Test Schema drift recovery
    schema_rec = orchestrator.handle_task_failure("m1", "t_val_1", "SCHEMA_CORRUPTION")
    assert schema_rec.recovery_action == "SCHEMA_REPAIR_REFLECTION"
    assert "task_reflection_schema_patch" in schema_rec.new_subgraph_nodes

    history = orchestrator.get_recovery_history()
    assert len(history) == 3
