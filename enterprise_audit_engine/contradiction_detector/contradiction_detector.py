"""Certification Contradiction Detector.

Detects discrepancies and semantic conflicts between:
1. Internal Evidence Classifications vs External Reality Verification
2. Evidence Records vs Textual Report Claims
3. Internal Policy Evaluations vs Actual Runtime Responses
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ContradictionItem(BaseModel):
    """Specific conflict between evidence, claims, and reality."""
    contradiction_id: str
    category: str  # EVIDENCE_VS_CLAIM, REALITY_VS_CERTIFICATION, CLASSIFICATION_MISMATCH
    claimed_statement: str
    observed_reality: str
    evidence_id: Optional[str] = None
    severity: str = "CRITICAL"  # CRITICAL, HIGH, MEDIUM
    remediation_required: str


class ContradictionReport(BaseModel):
    """Report detailing detected contradictions."""
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    has_contradictions: bool
    contradiction_count: int
    contradictions: List[ContradictionItem] = Field(default_factory=list)
    status: str  # NO_CONTRADICTIONS, CERTIFICATION_CONTRADICTION_FOUND
    final_verdict: str  # CERTIFICATION_PERMITTED, CERTIFICATION_REJECTED


class ContradictionDetector:
    """Finds irreconcilable conflicts between internal claims and external reality."""

    @classmethod
    def analyze_contradictions(
        cls,
        evidence_items: List[Dict[str, Any]],
        claims: List[Dict[str, Any]],
        reality_validation_results: Optional[Dict[str, Any]] = None,
    ) -> ContradictionReport:
        contradictions: List[ContradictionItem] = []

        # Index evidence by id and category
        ev_by_id = {str(e.get("id") or e.get("evidence_id")): e for e in evidence_items}

        # 1. Analyze Claim vs Evidence Classifications
        for c in claims:
            c_text = str(c.get("claim") or c.get("text") or "").lower()
            ev_ids = c.get("evidence_ids", [])
            for eid in ev_ids:
                ev = ev_by_id.get(eid)
                if ev:
                    cls_val = str(ev.get("classification", "")).upper()
                    
                    # Contradiction: Claiming runtime verified with only config
                    if ("runtime verified" in c_text or "execution verified" in c_text) and (
                        "CONFIGURATION" in cls_val or "DOCUMENTATION" in cls_val
                    ):
                        contradictions.append(ContradictionItem(
                            contradiction_id=f"CON-{len(contradictions)+1:03d}",
                            category="EVIDENCE_VS_CLAIM",
                            claimed_statement=f"Claim asserts runtime verification: '{c.get('claim') or c.get('text')}'",
                            observed_reality=f"Evidence {eid} is only classified as {cls_val}",
                            evidence_id=eid,
                            severity="CRITICAL",
                            remediation_required="Provide actual execution traces or downgrade claim",
                        ))
                    
                    # Contradiction: Claiming production ready with insufficient evidence
                    if ("production ready" in c_text or "fully verified" in c_text) and (
                        "INSUFFICIENT" in cls_val or "CRITICAL" in cls_val
                    ):
                        contradictions.append(ContradictionItem(
                            contradiction_id=f"CON-{len(contradictions)+1:03d}",
                            category="EVIDENCE_VS_CLAIM",
                            claimed_statement=f"Claim asserts production readiness: '{c.get('claim') or c.get('text')}'",
                            observed_reality=f"Evidence {eid} contains {cls_val}",
                            evidence_id=eid,
                            severity="CRITICAL",
                            remediation_required="Resolve critical finding or collect required evidence",
                        ))

        # 2. Analyze Reality Validation Failures vs Internal Certification
        if reality_validation_results:
            api_res = reality_validation_results.get("api", {})
            db_res = reality_validation_results.get("db", {})
            sec_res = reality_validation_results.get("security", {})

            for contra in api_res.get("contradictions", []):
                contradictions.append(ContradictionItem(
                    contradiction_id=f"CON-{len(contradictions)+1:03d}",
                    category="REALITY_VS_CERTIFICATION",
                    claimed_statement="API layer claimed conformant to authentication and security policies",
                    observed_reality=contra,
                    severity="CRITICAL",
                    remediation_required="Fix API security defect or remove certification claim",
                ))

            for contra in db_res.get("contradictions", []):
                contradictions.append(ContradictionItem(
                    contradiction_id=f"CON-{len(contradictions)+1:03d}",
                    category="REALITY_VS_CERTIFICATION",
                    claimed_statement="Database layer claimed ACID compliant and indexed",
                    observed_reality=contra,
                    severity="HIGH",
                    remediation_required="Resolve migration drift or index scan bottleneck",
                ))

            for vuln in sec_res.get("vulnerabilities", []):
                contradictions.append(ContradictionItem(
                    contradiction_id=f"CON-{len(contradictions)+1:03d}",
                    category="REALITY_VS_CERTIFICATION",
                    claimed_statement="Security controls claimed robust against adversarial attacks",
                    observed_reality=f"Penetration probe escaped: {vuln}",
                    severity="CRITICAL",
                    remediation_required="Patch vulnerability immediately",
                ))

        has_con = len(contradictions) > 0
        return ContradictionReport(
            has_contradictions=has_con,
            contradiction_count=len(contradictions),
            contradictions=contradictions,
            status="CERTIFICATION_CONTRADICTION_FOUND" if has_con else "NO_CONTRADICTIONS",
            final_verdict="CERTIFICATION_REJECTED" if has_con else "CERTIFICATION_PERMITTED",
        )
