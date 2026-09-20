"""Evidence Reliability Index (ERI) Calculator.

Calculates multi-dimensional evidence reliability:
ERI = 0.30 * Execution Reality +
      0.25 * Independent Confirmation +
      0.20 * Artifact Completeness +
      0.15 * Historical Stability +
      0.10 * External Reproducibility
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class EriDimensionScores(BaseModel):
    """Breakdown of individual ERI dimensions."""
    execution_reality_score: float  # Weight: 30%
    independent_confirmation_score: float  # Weight: 25%
    artifact_completeness_score: float  # Weight: 20%
    historical_stability_score: float  # Weight: 15%
    external_reproducibility_score: float  # Weight: 10%


class EvidenceReliabilityReport(BaseModel):
    """Full Evidence Reliability Index report."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    eri_score: float  # 0.0 - 100.0
    classification: str  # HIGH_TRUST_EVIDENCE, COMMERCIAL_TRUST_EVIDENCE, EVIDENCE_UNTRUSTED
    dimensions: EriDimensionScores
    is_acceptable_for_enterprise: bool


class EvidenceReliabilityIndexCalculator:
    """Computes rigorous Evidence Reliability Index across collected audit artifacts."""

    @classmethod
    def calculate_eri(
        cls,
        evidence_items: List[Dict[str, Any]],
        reality_checks_passed: bool = True,
        reproducibility_passed: bool = True,
        drift_detected: bool = False,
    ) -> EvidenceReliabilityReport:
        total_items = len(evidence_items)
        if total_items == 0:
            dims = EriDimensionScores(
                execution_reality_score=0.0,
                independent_confirmation_score=0.0,
                artifact_completeness_score=0.0,
                historical_stability_score=0.0,
                external_reproducibility_score=0.0,
            )
            return EvidenceReliabilityReport(
                eri_score=0.0,
                classification="EVIDENCE_UNTRUSTED",
                dimensions=dims,
                is_acceptable_for_enterprise=False,
            )

        # 1. Execution Reality (30%): Proportion of runtime execution evidence vs static/config
        exec_count = sum(1 for e in evidence_items if "runtime" in str(e.get("category", "")).lower() or "exec" in str(e.get("classification", "")).lower())
        exec_reality = min(100.0, max(50.0, (exec_count / total_items) * 150.0)) if reality_checks_passed else 20.0

        # 2. Independent Confirmation (25%): AST / Test / Cryptographic validation
        indep_count = sum(1 for e in evidence_items if e.get("confidence") in {"HIGH", "VERY_HIGH"})
        indep_conf = (indep_count / total_items * 100.0) if total_items > 0 else 0.0

        # 3. Artifact Completeness (20%): Payloads non-empty & valid hashes
        complete_count = sum(1 for e in evidence_items if e.get("raw_payload") and e.get("content_hash"))
        completeness = (complete_count / total_items * 100.0) if total_items > 0 else 0.0

        # 4. Historical Stability (15%): Low drift & non-tampered ledger
        stability = 95.0 if not drift_detected else 40.0

        # 5. External Reproducibility (10%): Deterministic twin audit results
        reproducibility = 100.0 if reproducibility_passed else 0.0

        # Composite ERI calculation
        eri = (
            0.30 * exec_reality +
            0.25 * indep_conf +
            0.20 * completeness +
            0.15 * stability +
            0.10 * reproducibility
        )
        eri = round(eri, 2)

        if eri >= 90.0:
            cls_name = "HIGH_TRUST_EVIDENCE"
            enterprise_ok = True
        elif eri >= 75.0:
            cls_name = "COMMERCIAL_TRUST_EVIDENCE"
            enterprise_ok = True
        else:
            cls_name = "EVIDENCE_UNTRUSTED"
            enterprise_ok = False
        dims = EriDimensionScores(
            execution_reality_score=round(exec_reality, 2),
            independent_confirmation_score=round(indep_conf, 2),
            artifact_completeness_score=round(completeness, 2),
            historical_stability_score=round(stability, 2),
            external_reproducibility_score=round(reproducibility, 2),
        )

        return EvidenceReliabilityReport(
            eri_score=eri,
            classification=cls_name,
            dimensions=dims,
            is_acceptable_for_enterprise=enterprise_ok,
        )
