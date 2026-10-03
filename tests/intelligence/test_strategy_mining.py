"""
Tests for Strategy Mining Engine (Pillar 2).
"""

import pytest
from app.runtime.intelligence.experience import ExperienceExtractor, ExperienceStore
from app.runtime.intelligence.strategy.strategy_library import StrategyLibrary
from app.runtime.intelligence.strategy.strategy_miner import StrategyMiner


def test_strategy_miner_and_library():
    store = ExperienceStore()
    extractor = ExperienceExtractor(store)

    for i in range(5):
        extractor.extract_from_mission(
            mission_id=f"msn_inv_{i}",
            document_type="invoice",
            task_type="extraction",
            telemetry={
                "total_latency_ms": 900.0 + i * 50,
                "total_cost_usd": 0.010,
                "final_confidence": 0.95 + i * 0.005,
            },
            tool_traces=[{"tool_name": "tesseract_ocr", "invocations": 1}],
        )

    miner = StrategyMiner()
    exps = store.query(document_type="invoice")
    strat = miner.mine_from_experiences(exps, strategy_name="Invoice Fast Track")

    assert strat is not None
    assert strat.document_domain == "invoice"
    assert strat.sample_size == 5
    assert strat.observed_success_rate == 1.0
    assert strat.latency_profile.mean == pytest.approx(1000.0, rel=0.1)

    lib = StrategyLibrary()
    lib.register_strategy(strat)
    assert lib.count() == 1

    # Promotion
    assert lib.promote_strategy(strat.strategy_id) is True
    active = lib.get_active_strategy("invoice")
    assert active is not None
    assert active.strategy_id == strat.strategy_id
    assert active.is_promoted is True
