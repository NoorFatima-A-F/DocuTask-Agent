"""Multi-Dimensional Verification Strength Model."""

from typing import List, Dict
from ..domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
    VerificationScorecard,
)


class VerificationStrengthModel:
    """Evaluates multi-dimensional evidence strength rather than binary presence checks."""

    # Weights defined by Enterprise Due Diligence Framework
    WEIGHTS = {
        "SOURCE_INSPECTION": 20.0,
        "AUTOMATED_TESTS": 20.0,
        "RUNTIME_EXECUTION": 25.0,
        "SECURITY_VALIDATION": 15.0,
        "BENCHMARK_EVIDENCE": 10.0,
        "REPRODUCIBILITY": 10.0,
    }

    @classmethod
    def evaluate_subsystem(cls, subsystem_name: str, records: List[EvidenceRecord]) -> VerificationScorecard:
        """Computes a multi-dimensional weighted verification score for a subsystem."""
        if not records:
            return VerificationScorecard(
                subsystem=subsystem_name,
                total_score=0.0,
                classification=EvidenceClassification.EVIDENCE_INSUFFICIENT,
                confidence=EvidenceConfidence.NONE,
                justification="No verifiable evidence records found for subsystem.",
            )

        # Check for critical security findings
        for r in records:
            if r.classification == EvidenceClassification.CRITICAL_FINDING:
                return VerificationScorecard(
                    subsystem=subsystem_name,
                    total_score=0.0,
                    classification=EvidenceClassification.CRITICAL_FINDING,
                    confidence=EvidenceConfidence.HIGH,
                    justification=f"Critical finding detected: {r.summary}",
                )

        source_types = {r.source_type for r in records}
        categories = {r.category for r in records}

        # 1. Source Inspection (0-20)
        source_score = 20.0 if EvidenceSourceType.STATIC_SOURCE_CODE in source_types else 0.0

        # 2. Automated Tests (0-20)
        tests_score = 0.0
        if EvidenceSourceType.AUTOMATED_TEST_EXECUTION in source_types:
            has_failed_tests = any(r.exit_code is not None and r.exit_code != 0 for r in records)
            tests_score = 20.0 if not has_failed_tests else 10.0

        # 3. Runtime Execution (0-25)
        runtime_score = 25.0 if EvidenceSourceType.RUNTIME_EXECUTION in source_types else 0.0

        # 4. Security Validation (0-15)
        security_score = 0.0
        if "SecurityAndCompliance" in categories or "Security" in categories:
            security_score = 15.0

        # 5. Benchmark Evidence (0-10)
        benchmark_score = 0.0
        for r in records:
            if "benchmark" in r.summary.lower() or "latency" in r.summary.lower() or "dora" in r.summary.lower():
                benchmark_score = 10.0
                break

        # 6. Reproducibility & Configuration (0-10)
        repro_score = 10.0 if EvidenceSourceType.CONFIGURATION_FILE in source_types else 5.0

        total_score = source_score + tests_score + runtime_score + security_score + benchmark_score + repro_score

        # Determine Classification & Confidence based on weighted score
        if total_score >= 90.0:
            classification = EvidenceClassification.VERIFIED_BY_EXECUTION
            confidence = EvidenceConfidence.VERY_HIGH
            justification = "Subsystem fully proven through static analysis, automated testing, and live runtime execution."
        elif total_score >= 70.0:
            classification = EvidenceClassification.VERIFIED
            confidence = EvidenceConfidence.HIGH
            justification = "Subsystem verified through static source analysis, automated test execution, and configuration."
        elif total_score >= 40.0:
            classification = EvidenceClassification.PARTIALLY_VERIFIED
            confidence = EvidenceConfidence.MEDIUM
            justification = "Subsystem has static evidence and configuration, but lacks complete test or runtime execution proof."
        else:
            classification = EvidenceClassification.EVIDENCE_INSUFFICIENT
            confidence = EvidenceConfidence.LOW
            justification = "Insufficient evidence collected to substantiate subsystem claims."

        return VerificationScorecard(
            subsystem=subsystem_name,
            source_inspection_score=source_score,
            automated_tests_score=tests_score,
            runtime_execution_score=runtime_score,
            security_validation_score=security_score,
            benchmark_evidence_score=benchmark_score,
            reproducibility_score=repro_score,
            total_score=total_score,
            classification=classification,
            confidence=confidence,
            justification=justification,
        )
