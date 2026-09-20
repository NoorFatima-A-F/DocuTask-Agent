"""
Observability Architecture & Instrumentation Analyzer.
"""
from typing import List, Dict, Any
from app.platform_verification.observability_verification.domain.models import ObservabilityArchitectureReport
from app.platform_verification.observability_verification.domain.interfaces import IObservabilityArchitectureAnalyzer


class ObservabilityArchitectureAnalyzer(IObservabilityArchitectureAnalyzer):
    """Audits telemetry instrumentation across all core subsystems."""

    REQUIRED_SUBSYSTEMS = {
        "api", "worker", "agent_runtime", "memory", "database",
        "queue", "storage", "ocr", "llm_provider", "security",
        "verification_engine", "telemetry_collector"
    }

    def analyze_architecture(self, services: List[Dict[str, Any]]) -> ObservabilityArchitectureReport:
        instrumented = set()
        for s in services:
            if s.get("has_logging", True) and s.get("has_metrics", True) and s.get("has_tracing", True):
                instrumented.add(s.get("name", ""))

        missing = list(self.REQUIRED_SUBSYSTEMS - instrumented)
        total = len(self.REQUIRED_SUBSYSTEMS)
        score = (len(instrumented) / max(total, 1)) * 100.0
        score = round(min(100.0, score), 2)
        status = "PASS" if len(missing) == 0 else "FAIL"

        return ObservabilityArchitectureReport(
            total_services=total,
            instrumented_services=len(instrumented),
            missing_instrumentation=missing,
            coverage_score=score,
            status=status,
        )
