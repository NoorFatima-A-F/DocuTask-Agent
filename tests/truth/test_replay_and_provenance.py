"""
Tests for Replay Certification and Metric Provenance Engines (Pillars 3 & 4).
"""

import pytest
from app.runtime.truth.metric_provenance import MetricProvenanceEngine
from app.runtime.truth.replay_cert import ScientificReplayCertifier


def test_scientific_replay_certifier():
    certifier = ScientificReplayCertifier()
    
    orig = {"total_latency_ms": 1000.0, "total_cost_usd": 0.010}
    rep = {
        "total_latency_ms": 1010.0,
        "total_cost_usd": 0.010,
        "output_similarity_pct": 99.98,
        "bitwise_state_match_rate": 0.9999,
        "dag_exact_match": True,
        "tool_sequence_exact_match": True,
    }

    report = certifier.certify_replay("msn_1001", orig, rep)
    assert report.is_certified is True
    assert report.certification_tier == "SCIENTIFIC_REPRODUCIBLE"
    assert report.latency_delta_pct == pytest.approx(1.0, rel=0.1)


def test_metric_provenance_lineage():
    engine = MetricProvenanceEngine()
    lineage = engine.get_lineage("extraction_accuracy")
    
    assert lineage is not None
    assert lineage.numeric_value == 0.992
    assert "Levenshtein" in lineage.evaluation_methodology
    assert lineage.sample_size_n == 1420
    assert len(lineage.supporting_evidence_hashes) >= 1
