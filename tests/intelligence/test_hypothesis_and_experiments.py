"""
Tests for Hypothesis Generation and Experimentation Engines (Pillars 4 & 5).
"""

import pytest
from app.runtime.intelligence.experience import (
    ExperienceExtractor,
    ExperienceRecord,
    ExperienceStore,
)
from app.runtime.intelligence.experiments.ab_validator import ABValidator
from app.runtime.intelligence.experiments.statistical_comparator import (
    StatisticalComparator,
)
from app.runtime.intelligence.hypothesis.hypothesis_engine import (
    HypothesisEngine,
    HypothesisStatus,
)
from app.runtime.intelligence.strategy.strategy_miner import StrategyMiner


def test_hypothesis_generation():
    store = ExperienceStore()
    extractor = ExperienceExtractor(store)

    for i in range(5):
        extractor.extract_from_mission(
            mission_id=f"msn_{i}",
            document_type="invoice",
            task_type="extraction",
            telemetry={"total_latency_ms": 1400.0, "total_cost_usd": 0.020, "retries_count": 1},
        )

    hyp_engine = HypothesisEngine()
    hypotheses = hyp_engine.generate_from_experiences(store.list_all())
    assert len(hypotheses) >= 1
    assert any(h.target_metric == "retries_count" for h in hypotheses)


def test_statistical_comparator_welch_ttest():
    control = [1000.0, 1020.0, 990.0, 1010.0, 1005.0]
    candidate = [800.0, 810.0, 790.0, 805.0, 795.0]

    comp = StatisticalComparator.compare_metrics("latency_ms", control, candidate, higher_is_better=False)
    assert comp.is_significant is True
    assert comp.p_value < 0.001
    assert comp.delta_pct < -15.0


def test_ab_validator_run():
    store = ExperienceStore()
    extractor = ExperienceExtractor(store)

    for i in range(6):
        extractor.extract_from_mission(
            mission_id=f"msn_{i}",
            document_type="invoice",
            task_type="extraction",
            telemetry={"total_latency_ms": 1200.0, "total_cost_usd": 0.015, "final_confidence": 0.94},
        )

    miner = StrategyMiner()
    ctrl = miner.mine_from_experiences(store.list_all())
    assert ctrl is not None

    cand = miner.mine_from_experiences(store.list_all())
    assert cand is not None
    cand.strategy_id = "cand_strat_01"
    cand.latency_profile.mean = 750.0  # Significant improvement

    validator = ABValidator()
    run = validator.run_experiment(
        title="Test Fast Pipeline",
        hypothesis_id="hyp_01",
        control_strategy=ctrl,
        candidate_strategy=cand,
        sample_size=10,
    )

    assert run.status.value == "CONCLUDED"
    assert run.latency_comparison is not None
    assert run.promotes_candidate is True
