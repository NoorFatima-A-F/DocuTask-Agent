"""Evidence Completeness & Coverage Verification Analyzer."""

from typing import List, Dict, Any
from enterprise_audit_engine.domain.evidence.models import EvidenceRecord, AuditFinding


class IncompleteEvidenceCoverageError(Exception):
    """Raised when an audit report or finding lacks 100% verified evidence coverage."""
    pass


class EvidenceCoverageAnalyzer:
    """Verifies that 100% of reported claims, findings, and statements have backing evidence."""

    @classmethod
    def verify_coverage(cls, findings: List[AuditFinding], records: List[EvidenceRecord]) -> Dict[str, Any]:
        record_map = {r.id: r for r in records}
        unsupported_findings: List[Dict[str, Any]] = []
        covered_findings: List[str] = []

        for finding in findings:
            finding_issues: List[str] = []

            # 1. Check evidence IDs exist
            if not finding.evidence_ids:
                finding_issues.append("Zero evidence IDs attached to finding.")
            else:
                for eid in finding.evidence_ids:
                    if eid not in record_map:
                        finding_issues.append(f"Referenced evidence ID '{eid}' does not exist in store.")
                    else:
                        rec = record_map[eid]
                        # 2. Check hash validity
                        if not rec.content_hash or rec.content_hash != rec.calculate_hash():
                            finding_issues.append(f"Evidence '{eid}' has invalid or missing content hash.")
                        # 3. Check payload exists
                        if not rec.raw_payload:
                            finding_issues.append(f"Evidence '{eid}' has empty raw payload.")

            if finding_issues:
                unsupported_findings.append({
                    "finding_id": finding.finding_id,
                    "claim": finding.claim,
                    "issues": finding_issues,
                })
            else:
                covered_findings.append(finding.finding_id)

        total_findings = len(findings)
        coverage_pct = (len(covered_findings) / total_findings * 100.0) if total_findings > 0 else 100.0
        is_complete = len(unsupported_findings) == 0

        if not is_complete:
            raise IncompleteEvidenceCoverageError(
                f"Evidence completeness check failed ({coverage_pct:.1f}% coverage). "
                f"{len(unsupported_findings)} findings lack complete evidence:\n"
                + "\n".join(f"- {f['finding_id']}: {f['issues']}" for f in unsupported_findings)
            )

        return {
            "is_complete": is_complete,
            "coverage_pct": round(coverage_pct, 2),
            "total_findings": total_findings,
            "covered_count": len(covered_findings),
            "unsupported_count": len(unsupported_findings),
            "status": "100_PERCENT_EVIDENCE_COVERED",
        }
