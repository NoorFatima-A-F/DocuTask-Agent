"""
Unit and Integration Tests for Digital Twin Shadow Execution & Safety Sandboxing (ASVSP Pillar 4).
"""

from app.runtime.digital_twin import (
    SafetySandbox,
    FidelityMonitor,
    DigitalTwinEngine,
)


def test_safety_sandbox_interception():
    sandbox = SafetySandbox()
    sbx_id = sandbox.create_sandbox("m_sec_01")
    actions = [
        {"type": "OCR_PARSE", "is_mutation": False, "key": "ocr_text"},
        {"type": "DB_MUTATE_DIRECT", "is_mutation": True, "target": "DB.production", "value": "test"},
    ]
    record = sandbox.execute_in_sandbox(sbx_id, "m_sec_01", actions)
    assert record.status == "INTERCEPTED_MUTATION"
    assert len(record.intercepted_mutations) == 1
    assert "ocr_text" in record.virtual_state


def test_fidelity_monitor():
    metrics = FidelityMonitor.compute_fidelity(
        shadow_id="shw_01",
        prod_output="Invoice total is $500",
        shadow_output="Invoice total is $500",
        prod_latency_ms=450.0,
        shadow_latency_ms=460.0,
        prod_tokens=1000,
        shadow_tokens=1020,
        prod_decision="PROCEED",
        shadow_decision="PROCEED",
    )
    assert metrics.fidelity_status == "HIGH_FIDELITY"
    assert metrics.output_agreement_score == 1.0


def test_digital_twin_engine():
    engine = DigitalTwinEngine()
    result = engine.run_shadow_simulation(
        mission_id="m_twin_01",
        prod_policy="v4.2-pareto",
        shadow_policy="v5.0-bayesian-candidate",
    )
    assert result["mission_id"] == "m_twin_01"
    assert result["fidelity"]["output_agreement_score"] > 0.8
    assert len(engine.get_shadow_history()) == 1
