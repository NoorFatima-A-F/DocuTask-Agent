"""External Benchmark Dataset & Calibration Suite.

Provides standardized reference system profiles:
1. Good System: Clean AST scans, high test coverage, valid provenance -> Expected: PASS
2. Vulnerable System: Injected vulnerabilities, unauthenticated endpoints -> Expected: FAIL
3. Misleading System: Inflated claims ("100% secure"), unbacked documentation -> Expected: DETECTED_FRAUD
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from enterprise_audit_engine.certification_authority.policy.policy_engine import CertificationPolicyEngine
from enterprise_audit_engine.certification_authority.domain.models import EQIBreakdown
from enterprise_audit_engine.governance.claim_validator import ClaimValidator


class BenchmarkArchetypeResult(BaseModel):
    """Result of running the audit engine against a benchmark archetype."""
    archetype_name: str
    expected_outcome: str
    actual_outcome: str
    matched: bool
    discrimination_score: float  # 0 - 100
    details: Dict[str, Any] = Field(default_factory=dict)


class BenchmarkSuiteReport(BaseModel):
    """Full external benchmark calibration report."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    total_archetypes_tested: int
    archetypes_passed: int
    overall_calibration_accuracy: float
    status: str  # BENCHMARK_CALIBRATED, CALIBRATION_DRIFT_DETECTED
    results: List[BenchmarkArchetypeResult] = Field(default_factory=list)


class ExternalBenchmarkSuite:
    """Evaluates the audit engine against reference ground-truth systems."""

    @classmethod
    def run_all_benchmarks(cls) -> BenchmarkSuiteReport:
        results: List[BenchmarkArchetypeResult] = []

        # 1. Archetype: Good System
        good_evidence = [
            EvidenceRecord(
                id="EV-BENCH-GOOD-1",
                collector="PytestCollector",
                source_type=EvidenceSourceType.RUNTIME_EXECUTION,
                category="AutomatedTesting",
                summary="300 tests passed with 95% coverage",
                raw_payload={"passed": 300, "failed": 0},
                confidence=EvidenceConfidence.HIGH,
                classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
            ),
            EvidenceRecord(
                id="EV-BENCH-GOOD-2",
                collector="BanditCollector",
                source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
                category="SecurityAndCompliance",
                summary="Bandit AST scan zero high/medium issues",
                raw_payload={"issues": []},
                confidence=EvidenceConfidence.HIGH,
                classification=EvidenceClassification.VERIFIED,
            ),
        ]
        eqi_good = EQIBreakdown(
            evidence_coverage_score=24.0,
            verification_depth_score=24.0,
            reproducibility_score=19.0,
            integrity_score=14.0,
            freshness_score=14.0,
            total_eqi=95.0,
            rating="ENTERPRISE_GRADE",
        )
        eval_good = CertificationPolicyEngine.evaluate_policy(
            policy_name="enterprise_grade",
            overall_confidence="HIGH",
            overall_classification="VERIFIED_BY_EXECUTION",
            critical_findings=[],
            eqi=eqi_good,
            is_reproducible=True,
            active_domains=["runtime", "security", "testing", "reproducibility"],
        )
        good_pass = eval_good["passed"]
        results.append(BenchmarkArchetypeResult(
            archetype_name="GOOD_ENTERPRISE_SYSTEM",
            expected_outcome="PASS",
            actual_outcome="PASS" if good_pass else "FAIL",
            matched=good_pass,
            discrimination_score=100.0 if good_pass else 0.0,
            details={"policy_passed": good_pass},
        ))

        # 2. Archetype: Vulnerable System
        vuln_evidence = [
            EvidenceRecord(
                id="EV-BENCH-VULN-1",
                collector="SecurityScanner",
                source_type=EvidenceSourceType.RUNTIME_EXECUTION,
                category="SecurityAndCompliance",
                summary="Critical SQL Injection flaw identified in search endpoint",
                raw_payload={"cve": "CVE-2026-9999", "severity": "CRITICAL"},
                confidence=EvidenceConfidence.HIGH,
                classification=EvidenceClassification.CRITICAL_FINDING,
            ),
        ]
        eqi_vuln = EQIBreakdown(
            evidence_coverage_score=10.0,
            verification_depth_score=10.0,
            reproducibility_score=8.0,
            integrity_score=6.0,
            freshness_score=6.0,
            total_eqi=40.0,
            rating="DEGRADED",
        )
        eval_vuln = CertificationPolicyEngine.evaluate_policy(
            policy_name="enterprise_grade",
            overall_confidence="HIGH",
            overall_classification="CRITICAL_FINDING",
            critical_findings=["Critical SQL Injection vulnerability"],
            eqi=eqi_vuln,
            is_reproducible=False,
            active_domains=["security"],
        )
        vuln_blocked = not eval_vuln["passed"]
        results.append(BenchmarkArchetypeResult(
            archetype_name="VULNERABLE_SYSTEM",
            expected_outcome="FAIL",
            actual_outcome="FAIL" if vuln_blocked else "PASS",
            matched=vuln_blocked,
            discrimination_score=100.0 if vuln_blocked else 0.0,
            details={"blocked_properly": vuln_blocked},
        ))

        # 3. Archetype: Misleading / Inflated Claims System
        misleading_evidence = [
            EvidenceRecord(
                id="EV-BENCH-MIS-1",
                collector="DocumentationParser",
                source_type=EvidenceSourceType.CONFIGURATION_FILE,
                category="General",
                summary="README states system has 100% bug-free architecture",
                raw_payload={"doc_only": True},
                confidence=EvidenceConfidence.LOW,
                classification=EvidenceClassification.CONFIGURATION_PRESENT,
            ),
        ]
        from enterprise_audit_engine.domain.evidence.models import AuditFinding
        fnd_mis = AuditFinding(
            finding_id="FND-MIS-1",
            subsystem="General",
            claim="Our platform is 100% bug-free and fully verified by runtime execution",
            classification=EvidenceClassification.VERIFIED_BY_EXECUTION,
            evidence_ids=["EV-BENCH-MIS-1"],
            confidence=EvidenceConfidence.HIGH,
            analysis="Asserted from documentation",
        )
        is_valid_claim, _ = ClaimValidator.validate_claim(fnd_mis, misleading_evidence)
        mis_detected = not is_valid_claim
        results.append(BenchmarkArchetypeResult(
            archetype_name="MISLEADING_SYSTEM_WITH_INFLATED_CLAIMS",
            expected_outcome="DETECTED_AND_BLOCKED",
            actual_outcome="DETECTED_AND_BLOCKED" if mis_detected else "UNNOTICED",
            matched=mis_detected,
            discrimination_score=100.0 if mis_detected else 0.0,
            details={"unbacked_claim_blocked": mis_detected},
        ))

        passed_archetypes = sum(1 for r in results if r.matched)
        accuracy = (passed_archetypes / len(results) * 100.0) if results else 100.0

        return BenchmarkSuiteReport(
            total_archetypes_tested=len(results),
            archetypes_passed=passed_archetypes,
            overall_calibration_accuracy=round(accuracy, 2),
            status="BENCHMARK_CALIBRATED" if accuracy == 100.0 else "CALIBRATION_DRIFT_DETECTED",
            results=results,
        )
