"""
Production Readiness Assessment Framework for Enterprise AAOS.
Evaluates concrete checklist criteria across 10 mission-critical pillars:
Reliability, Security, Observability, Scalability, Testing, Recovery,
Compliance, Deployment, Maintainability, and Performance.
Replaces arbitrary percentages with evidence-verified checklist assertions.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from app.evidence.registry.evidence_models import VerificationStatus
from app.evidence.registry.evidence_registry import EvidenceRegistry

logger = logging.getLogger(__name__)


@dataclass
class ReadinessCriterion:
    """Individual measurable readiness checklist item."""

    criterion_id: str
    category: str
    description: str
    weight: float
    required_evidence_type: str
    linked_evidence_id: Optional[str] = None
    passed: bool = False
    evidence_summary: str = ""
    missing_items: List[str] = field(default_factory=list)


@dataclass
class CategoryScore:
    """Evaluated score for a readiness category."""

    category: str
    total_criteria: int
    passed_criteria: int
    weight_total: float
    weight_passed: float
    passed: bool
    missing_checklist: List[str] = field(default_factory=list)


class ProductionReadinessEvaluator:
    """
    Evaluates system readiness against rigorous enterprise standards.
    Requires verified evidence for every single check.
    """

    def __init__(self, registry: Optional[EvidenceRegistry] = None) -> None:
        self.registry = registry or EvidenceRegistry()
        self.criteria: List[ReadinessCriterion] = self._build_standard_checklist()

    def _build_standard_checklist(self) -> List[ReadinessCriterion]:
        """Builds the 10-category production readiness matrix."""
        return [
            # 1. Testing
            ReadinessCriterion("TST-01", "Testing", "Unit & Integration test suite passes at 100% green", 10.0, "UNIT_TEST"),
            ReadinessCriterion("TST-02", "Testing", "Regression tests for edge cases and tool failures pass", 5.0, "INTEGRATION_TEST"),
            # 2. Reliability
            ReadinessCriterion("REL-01", "Reliability", "Continuous 12-state autonomous decision loop verified", 10.0, "RUNTIME_TRACE"),
            ReadinessCriterion("REL-02", "Reliability", "Multi-critic consensus reflection prevents bad extractions", 8.0, "BENCHMARK"),
            ReadinessCriterion("REL-03", "Reliability", "Dead-letter queue isolates poisoned event messages", 7.0, "CHAOS_TEST"),
            # 3. Recovery
            ReadinessCriterion("REC-01", "Recovery", "SHA-256 verified workflow checkpoints restore interrupted state", 10.0, "RECOVERY_TEST"),
            ReadinessCriterion("REC-02", "Recovery", "Adaptive replanning engine mutates DAG on tool failure without data loss", 8.0, "RECOVERY_TEST"),
            # 4. Security & Compliance
            ReadinessCriterion("SEC-01", "Security", "Zero-trust PII tokenization sanitizes SSN/PAN before model dispatch", 10.0, "SECURITY_SCAN"),
            ReadinessCriterion("SEC-02", "Security", "Append-only SHA-256 event store provides immutable audit trail", 8.0, "SECURITY_SCAN"),
            ReadinessCriterion("CMP-01", "Compliance", "Statutory HIPAA/GDPR/PCI-DSS policy gate engine enforced", 8.0, "SECURITY_SCAN"),
            # 5. Scalability & Distributed
            ReadinessCriterion("SCA-01", "Scalability", "Distributed lock manager prevents split-brain and race conditions", 10.0, "STRESS_TEST"),
            ReadinessCriterion("SCA-02", "Scalability", "Optimistic concurrency state protects multi-worker workflow updates", 8.0, "STRESS_TEST"),
            # 6. Observability
            ReadinessCriterion("OBS-01", "Observability", "OpenTelemetry bridge propagates W3C traceparent headers", 7.0, "TELEMETRY"),
            ReadinessCriterion("OBS-02", "Observability", "SLO availability and error budget tracking implemented", 7.0, "TELEMETRY"),
            # 7. Memory & Learning
            ReadinessCriterion("MEM-01", "Memory", "Background consolidation mines patterns and promotes semantic facts", 8.0, "BENCHMARK"),
            ReadinessCriterion("MEM-02", "Memory", "Temporal decay and contradiction detection resolve stale facts", 6.0, "BENCHMARK"),
            # 8. Human-In-The-Loop
            ReadinessCriterion("HITL-01", "Human Collaboration", "SLA ticket queue pauses execution for operator review", 8.0, "INTEGRATION_TEST"),
            ReadinessCriterion("HITL-02", "Human Collaboration", "Operator feedback imprints ground truth into semantic memory", 7.0, "INTEGRATION_TEST"),
            # 9. Performance & Cost
            ReadinessCriterion("PRF-01", "Performance", "End-to-end cognitive decision cycle p95 latency under 1000ms", 8.0, "PERFORMANCE_TEST"),
            ReadinessCriterion("CST-01", "Cost Intelligence", "Token consumption and cost tracking recorded per execution", 6.0, "TELEMETRY"),
        ]

    def link_evidence(self, criterion_id: str, evidence_id: str) -> bool:
        """Links an evidence item to a readiness criterion and verifies it."""
        for c in self.criteria:
            if c.criterion_id == criterion_id:
                item = self.registry.get(evidence_id)
                if item and item.verification_status == VerificationStatus.VERIFIED:
                    c.linked_evidence_id = evidence_id
                    c.passed = True
                    c.evidence_summary = item.description
                    c.missing_items = []
                    logger.info("Criterion %s PASSED with evidence %s", criterion_id, evidence_id)
                    return True
                else:
                    c.passed = False
                    c.missing_items = [f"Evidence {evidence_id} not found or unverified"]
                    return False
        return False

    def evaluate(self) -> Dict[str, Any]:
        """Evaluates readiness status across all categories."""
        categories: Dict[str, List[ReadinessCriterion]] = {}
        for c in self.criteria:
            if c.category not in categories:
                categories[c.category] = []
            categories[c.category].append(c)

        cat_scores: Dict[str, CategoryScore] = {}
        total_weight = sum(c.weight for c in self.criteria)
        passed_weight = sum(c.weight for c in self.criteria if c.passed)

        for cat_name, crit_list in categories.items():
            c_total = len(crit_list)
            c_passed = sum(1 for c in crit_list if c.passed)
            w_total = sum(c.weight for c in crit_list)
            w_passed = sum(c.weight for c in crit_list if c.passed)
            missing = [c.description for c in crit_list if not c.passed]

            cat_scores[cat_name] = CategoryScore(
                category=cat_name,
                total_criteria=c_total,
                passed_criteria=c_passed,
                weight_total=w_total,
                weight_passed=w_passed,
                passed=(c_passed == c_total),
                missing_checklist=missing,
            )

        overall_passed = all(cs.passed for cs in cat_scores.values())

        return {
            "overall_status": "READY" if overall_passed else "NOT_READY",
            "total_criteria": len(self.criteria),
            "passed_criteria": sum(1 for c in self.criteria if c.passed),
            "total_weight": total_weight,
            "passed_weight": passed_weight,
            "readiness_ratio": round(passed_weight / total_weight, 4) if total_weight > 0 else 0.0,
            "categories": {
                k: {
                    "passed": v.passed,
                    "passed_criteria": f"{v.passed_criteria}/{v.total_criteria}",
                    "weight_passed": f"{v.weight_passed}/{v.weight_total}",
                    "missing_items": v.missing_checklist,
                }
                for k, v in cat_scores.items()
            },
            "checklist": [
                {
                    "criterion_id": c.criterion_id,
                    "category": c.category,
                    "description": c.description,
                    "weight": c.weight,
                    "passed": c.passed,
                    "linked_evidence_id": c.linked_evidence_id,
                    "evidence_summary": c.evidence_summary,
                    "missing_items": c.missing_items,
                }
                for c in self.criteria
            ],
        }

    def export_reports(self, output_json: Path, output_md: Path) -> None:
        """Exports production_readiness.json and production_readiness.md."""
        data = self.evaluate()

        output_json.parent.mkdir(parents=True, exist_ok=True)
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        md_lines = [
            "# Production Readiness Assessment Report",
            f"**Overall Status**: `{data['overall_status']}` | **Passed**: {data['passed_criteria']}/{data['total_criteria']} criteria ({data['readiness_ratio']*100:.1f}%)",
            "",
            "## Category Breakdown",
            "| Category | Status | Criteria Passed | Weight Score | Missing Items |",
            "| :--- | :---: | :---: | :---: | :--- |",
        ]
        for cat, details in data["categories"].items():
            status_badge = "PASS" if details["passed"] else "INCOMPLETE"
            missing_str = ", ".join(details["missing_items"]) if details["missing_items"] else "None"
            md_lines.append(
                f"| **{cat}** | `{status_badge}` | {details['passed_criteria']} | {details['weight_passed']} | {missing_str} |"
            )

        md_lines.extend([
            "",
            "## Measurable Evidence Checklist",
            "| ID | Category | Requirement | Weight | Status | Evidence ID | Evidence Summary |",
            "| :--- | :--- | :--- | :---: | :---: | :--- | :--- |",
        ])
        for item in data["checklist"]:
            status_badge = "PASS" if item["passed"] else "FAIL"
            evi_id = item["linked_evidence_id"] or "None"
            evi_sum = item["evidence_summary"] or "Unsatisfied requirement"
            md_lines.append(
                f"| `{item['criterion_id']}` | {item['category']} | {item['description']} | {item['weight']} | `{status_badge}` | `{evi_id}` | {evi_sum} |"
            )

        with open(output_md, "w", encoding="utf-8") as f:
            f.write("\n".join(md_lines))
        logger.info("Saved readiness reports to %s and %s", output_json, output_md)
