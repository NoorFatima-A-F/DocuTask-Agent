"""Audit History & Regression Detector."""

from typing import Dict, Any, List
from enterprise_audit_engine.certification_authority.domain.models import CertificationRecord


class AuditRegressionDetector:
    """Compares two historical release audits to detect quality and security regressions."""

    @classmethod
    def compare_certifications(
        cls,
        previous: CertificationRecord,
        current: CertificationRecord,
    ) -> Dict[str, Any]:
        """Performs structured comparative delta analysis between previous and current release audits."""
        
        # 1. Critical findings regression
        prev_crit_count = len(previous.critical_findings)
        curr_crit_count = len(current.critical_findings)
        crit_delta = curr_crit_count - prev_crit_count

        # 2. EQI score delta
        eqi_delta = round(current.eqi_score - previous.eqi_score, 2)

        # 3. Verification depth delta
        depth_deltas = {}
        all_depth_keys = set(previous.verification_depth.keys()).union(set(current.verification_depth.keys()))
        for k in all_depth_keys:
            prev_d = previous.verification_depth.get(k, 0.0)
            curr_d = current.verification_depth.get(k, 0.0)
            depth_deltas[k] = {
                "previous": prev_d,
                "current": curr_d,
                "delta": round(curr_d - prev_d, 2),
            }

        # 4. Status and Policy Compliance
        status_change = {
            "previous_status": previous.status.value,
            "current_status": current.status.value,
            "previous_policy": previous.policy_name,
            "current_policy": current.policy_name,
        }

        # Determine regression indicators
        regressions: List[str] = []
        if crit_delta > 0:
            regressions.append(f"Security/Stability regression: +{crit_delta} critical finding(s) introduced.")
        if eqi_delta < -5.0:
            regressions.append(f"Evidence Quality degradation: EQI dropped by {abs(eqi_delta)} points ({previous.eqi_score} -> {current.eqi_score}).")
        if previous.status.value == "VALID" and current.status.value != "VALID":
            regressions.append(f"Certification status degraded from {previous.status.value} to {current.status.value}.")

        has_regression = len(regressions) > 0

        # Format comparison table lines
        table_rows = [
            {"area": "Release Version", "previous": previous.release_version, "current": current.release_version, "status": "UPGRADE"},
            {"area": "Certification Status", "previous": previous.status.value, "current": current.status.value, "status": "MATCH" if previous.status == current.status else "CHANGED"},
            {"area": "EQI Quality Score", "previous": f"{previous.eqi_score}/100", "current": f"{current.eqi_score}/100", "status": "IMPROVED" if eqi_delta >= 0 else "DEGRADED"},
            {"area": "Critical Findings", "previous": str(prev_crit_count), "current": str(curr_crit_count), "status": "SAFE" if curr_crit_count == 0 else "WARNING"},
            {"area": "Merkle Tree Root", "previous": f"{previous.merkle_root[:12]}...", "current": f"{current.merkle_root[:12]}...", "status": "UPDATED"},
        ]

        return {
            "has_regression": has_regression,
            "regressions_count": len(regressions),
            "regressions": regressions,
            "previous_version": previous.release_version,
            "current_version": current.release_version,
            "eqi_delta": eqi_delta,
            "critical_findings_delta": crit_delta,
            "depth_deltas": depth_deltas,
            "status_change": status_change,
            "comparison_table": table_rows,
        }
