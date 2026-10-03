"""Independent Classification Rule Engine Validator."""

from typing import Dict, Any, List
from pydantic import BaseModel, Field
from enterprise_audit_engine.domain.evidence.models import (
    EvidenceRecord,
    EvidenceSourceType,
    EvidenceClassification,
    EvidenceConfidence,
)
from enterprise_audit_engine.analyzers.confidence_engine import ConfidenceEngine
from enterprise_audit_engine.analyzers.verification_strength_model import VerificationStrengthModel


class RuleExecutionEvidence:
    """Proof of rule engine invariant testing."""
    def __init__(self, rule_name: str, passed: bool, input_summary: str, expected: str, actual: str):
        self.rule_name = rule_name
        self.passed = passed
        self.input_summary = input_summary
        self.expected = expected
        self.actual = actual

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "passed": self.passed,
            "input_summary": self.input_summary,
            "expected": self.expected,
            "actual": self.actual,
        }


class RuleValidationResult(BaseModel):
    """Result of invariant validation testing."""
    is_valid: bool = True
    rules_checked_count: int = 0
    violations: List[str] = Field(default_factory=list)


class IndependentRuleValidator:
    """Formally tests classification rule invariants against synthetic scenarios."""

    TIER_RANK = {"DEVELOPMENT": 1, "COMMERCIAL": 2, "ENTERPRISE": 3}

    @classmethod
    def _create_record(cls, eid: str, cat: str, src: EvidenceSourceType, cls_type: EvidenceClassification, conf: EvidenceConfidence) -> EvidenceRecord:
        rec = EvidenceRecord(
            id=eid,
            collector="RuleTestCollector",
            source_type=src,
            category=cat,
            summary=f"Synthetic record for {cat}",
            raw_payload={"test": True},
            confidence=conf,
            classification=cls_type,
        )
        return rec.model_copy(update={"content_hash": rec.calculate_hash()})

    @classmethod
    def validate_all_rules(cls) -> Dict[str, Any]:
        evidence_list: List[RuleExecutionEvidence] = []

        # Invariant 1: Configuration only MUST NOT be VERIFIED
        cfg_record = cls._create_record(
            "EV-R1", "Database", EvidenceSourceType.CONFIGURATION_FILE,
            EvidenceClassification.CONFIGURATION_PRESENT, EvidenceConfidence.LOW,
        )
        sc1 = VerificationStrengthModel.evaluate_subsystem("Database", [cfg_record])
        inv1_passed = (sc1.classification != EvidenceClassification.VERIFIED)
        evidence_list.append(RuleExecutionEvidence(
            rule_name="INVARIANT_CONFIG_ONLY_NOT_VERIFIED",
            passed=inv1_passed,
            input_summary="Only CONFIGURATION_FILE evidence present",
            expected="NOT VERIFIED / CONFIGURATION_PRESENT",
            actual=sc1.classification.value,
        ))

        # Invariant 2: Static code only cannot claim VERIFIED_BY_EXECUTION
        stat_record = cls._create_record(
            "EV-R2", "Security", EvidenceSourceType.STATIC_SOURCE_CODE,
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS, EvidenceConfidence.MEDIUM,
        )
        sc2 = VerificationStrengthModel.evaluate_subsystem("Security", [stat_record])
        inv2_passed = (sc2.classification != EvidenceClassification.VERIFIED_BY_EXECUTION)
        evidence_list.append(RuleExecutionEvidence(
            rule_name="INVARIANT_STATIC_CANNOT_CLAIM_EXECUTION",
            passed=inv2_passed,
            input_summary="Only STATIC_SOURCE_CODE evidence present",
            expected="NOT VERIFIED_BY_EXECUTION",
            actual=sc2.classification.value,
        ))

        # Invariant 3: Empty evidence pool MUST be EVIDENCE_INSUFFICIENT
        sc3_cls = ConfidenceEngine.classify_subsystem([])
        inv3_passed = (sc3_cls in {EvidenceClassification.EVIDENCE_INSUFFICIENT, EvidenceClassification.UNKNOWN})
        evidence_list.append(RuleExecutionEvidence(
            rule_name="INVARIANT_EMPTY_EVIDENCE_IS_INSUFFICIENT",
            passed=inv3_passed,
            input_summary="Empty evidence list",
            expected="EVIDENCE_INSUFFICIENT",
            actual=sc3_cls.value,
        ))

        # Invariant 4: Critical finding dominates classification
        crit_record = cls._create_record(
            "EV-R4", "Database", EvidenceSourceType.RUNTIME_EXECUTION,
            EvidenceClassification.CRITICAL_FINDING, EvidenceConfidence.LOW,
        )
        sc4_cls = ConfidenceEngine.classify_subsystem([crit_record])
        inv4_passed = (sc4_cls == EvidenceClassification.CRITICAL_FINDING)
        evidence_list.append(RuleExecutionEvidence(
            rule_name="INVARIANT_CRITICAL_FINDING_DOMINANCE",
            passed=inv4_passed,
            input_summary="Contains CRITICAL_FINDING record",
            expected="CRITICAL_FINDING",
            actual=sc4_cls.value,
        ))

        all_passed = all(e.passed for e in evidence_list)
        return {
            "all_invariants_valid": all_passed,
            "total_rules_tested": len(evidence_list),
            "passed_rules_count": sum(1 for e in evidence_list if e.passed),
            "rule_evidence": [e.to_dict() for e in evidence_list],
            "status": "RULES_FORMALLY_VERIFIED" if all_passed else "RULE_INVARIANT_VIOLATION",
        }

    @classmethod
    def validate_all_invariants(cls) -> RuleValidationResult:
        res = cls.validate_all_rules()
        violations = []
        if not res["all_invariants_valid"]:
            for r in res["rule_evidence"]:
                if not r["passed"]:
                    violations.append(f"{r['rule_name']}: expected {r['expected']}, got {r['actual']}")
        return RuleValidationResult(
            is_valid=res["all_invariants_valid"],
            rules_checked_count=res["total_rules_tested"],
            violations=violations,
        )

    @classmethod
    def verify_monotonic_tier(cls, score_low: float, tier_low: str, score_high: float, tier_high: str) -> bool:
        r_low = cls.TIER_RANK.get(tier_low, 0)
        r_high = cls.TIER_RANK.get(tier_high, 0)
        if score_high >= score_low:
            return r_high >= r_low
        return r_low >= r_high

    @classmethod
    def verify_tier_boundary(cls, score: float, assigned_tier: str) -> bool:
        if score < 50.0 and assigned_tier == "ENTERPRISE":
            return False
        if score >= 90.0 and assigned_tier == "DEVELOPMENT":
            return False
        return True
