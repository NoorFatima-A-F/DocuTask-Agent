"""Tests for SLO Calculations, Burn Rates, and Error Budget Release Gates."""

from app.observability.slo.budgets import BudgetStatus, ErrorBudgetEngine
from app.observability.slo.calculator import SLOCalculator
from app.observability.slo.models import ServiceLevelObjective


def test_slo_calculator_compliance_and_burn_rate():
    slo = ServiceLevelObjective(
        slo_id="slo-api-avail",
        name="Document API Availability",
        service_name="api-gateway",
        target_percent=99.9,
    )

    # 9,995 good out of 10,000 total = 99.95% (Compliant)
    res = SLOCalculator.calculate_compliance(
        slo=slo,
        good_events=9995,
        total_events=10000,
        bad_events_1h=1,
        total_events_1h=1000,
    )
    assert res.compliant is True
    assert res.actual_percent == 99.95
    assert res.burn_rate_1h == 1.0


def test_error_budget_exhaustion_and_release_freeze():
    engine = ErrorBudgetEngine(at_risk_threshold_percent=20.0)
    slo = ServiceLevelObjective(
        slo_id="slo-ocr-latency",
        name="OCR Latency Budget",
        service_name="ocr-processor",
        target_percent=99.0,  # 1% allowed errors = 10 out of 1000
    )
    engine.register_slo(slo)

    # 1. 2 errors out of 1000 (Budget remaining: 8/10 = 80%) -> HEALTHY
    b1 = engine.calculate_budget("slo-ocr-latency", total_events=1000, bad_events=2)
    assert b1 is not None
    assert b1.status == BudgetStatus.HEALTHY
    assert b1.release_freeze_enforced is False

    # 2. 9 errors out of 1000 (Budget remaining: 1/10 = 10%) -> AT_RISK
    b2 = engine.calculate_budget("slo-ocr-latency", total_events=1000, bad_events=9)
    assert b2.status == BudgetStatus.AT_RISK
    assert b2.release_freeze_enforced is False

    # 3. 15 errors out of 1000 (Budget exhausted) -> EXHAUSTED & FREEZE
    b3 = engine.calculate_budget("slo-ocr-latency", total_events=1000, bad_events=15)
    assert b3.status == BudgetStatus.EXHAUSTED
    assert b3.release_freeze_enforced is True
