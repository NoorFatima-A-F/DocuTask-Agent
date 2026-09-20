"""Tests for Multi-Signal RCA and Continuous Profiling."""

import pytest
from app.observability.incidents.rca import RCAEngine
from app.observability.profiling.analyzer import HotspotAnalyzer
from app.observability.profiling.profiler import ContinuousProfiler


def test_rca_engine_multi_signal_correlation():
    engine = RCAEngine()
    metrics = {"node_cpu_usage_percent": 92.0, "runtime_queue_depth": 250.0}
    spans = [
        {"name": "ai_inference_step", "service": "llm-worker", "duration_ms": 4500.0}
    ]

    rca = engine.analyze_incident(
        service_name="llm-worker",
        metrics_snapshot=metrics,
        trace_spans=spans,
    )
    assert rca.confidence_score >= 0.90
    assert len(rca.causal_chain) >= 2
    assert "saturation" in rca.primary_root_cause.lower()


def test_continuous_profiler_and_hotspot_analyzer():
    profiler = ContinuousProfiler()

    # Record profiling samples
    profiler.record_sample("ocr_parse_pdf", duration_ms=250.0)
    profiler.record_sample("ocr_parse_pdf", duration_ms=300.0)
    profiler.record_sample("db_lookup", duration_ms=10.0)

    analyzer = HotspotAnalyzer(profiler=profiler)
    hotspots = analyzer.identify_hotspots()
    assert len(hotspots) == 2
    assert hotspots[0].function_name == "ocr_parse_pdf"
    assert hotspots[0].percent_of_total_time > 80.0

    flamegraph = analyzer.generate_flamegraph_hierarchy()
    assert flamegraph["name"] == "root"
    assert len(flamegraph["children"]) == 2
