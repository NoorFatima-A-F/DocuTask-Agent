"""
Automated Pytest Suite for Enterprise AI Red Teaming & Threat Hardening.
Coverage target: > 90%.
"""

import os
import pytest
from app.validation.security.adversarial_dataset.generator import AdversarialDatasetGenerator
from app.validation.security.fuzzer import SecurityFuzzer
from app.validation.security.multi_turn import MultiTurnSecurityTester
from app.validation.security.observability import SecurityMetricsCollector
from app.validation.security.owasp.llm_top10 import OWASPSecuritySuite


def test_owasp_llm_top10_checks():
    """Verifies OWASP LLM Top 10 security category checks (LLM01 - LLM10)."""
    results = OWASPSecuritySuite.run_all_owasp_checks()
    assert len(results) == 10
    assert all(r.passed for r in results)
    assert any(r.owasp_id == "LLM01" for r in results)
    assert any(r.owasp_id == "LLM08" for r in results)


def test_large_adversarial_dataset_generation():
    """Verifies AdversarialDatasetGenerator produces 500+ structured attack cases."""
    cases = AdversarialDatasetGenerator.generate_500_dataset()
    assert len(cases) >= 500

    langs = set(c.payload for c in cases if "urdu" in c.payload.lower())
    assert len(langs) > 0

    saved_path = AdversarialDatasetGenerator.persist_dataset_to_disk("docs/audits/adversarial_dataset.json")
    assert os.path.exists(saved_path)


def test_security_fuzzer_execution():
    """Verifies SecurityFuzzer runs high-throughput randomized fuzzing."""
    fuzz_res = SecurityFuzzer.run_fuzzing_suite(iterations=100)
    assert fuzz_res["passed_cases"] == 100
    assert fuzz_res["pass_rate_percentage"] == 100.0


def test_multi_turn_context_security():
    """Verifies MultiTurnSecurityTester neutralizes conversation poisoning."""
    turns = MultiTurnSecurityTester.test_multi_turn_poisoning()
    assert len(turns) == 3
    assert not any(t.memory_leak_detected for t in turns)


def test_prometheus_security_observability():
    """Verifies Prometheus security metrics endpoint formatting."""
    prom_str = SecurityMetricsCollector.get_metrics_prometheus_format()
    assert "ai_attack_attempts_total" in prom_str
    assert "ai_attack_blocked_total" in prom_str
