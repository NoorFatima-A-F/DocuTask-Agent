"""
Phase 3O: Infrastructure Evidence Normalizer.
"""

import re
from typing import Any, Dict, List

from ..domain.interfaces import IEvidenceNormalizer
from ..domain.models import (
    NormalizedEvidenceItem,
    RawEvidenceBundle,
    RiskLevel,
    VerificationStatus,
)


class EvidenceNormalizer(IEvidenceNormalizer):
    """
    Normalizes diverse verification payloads into a unified, risk-annotated schema
    categorized into the 6 enterprise engineering pillars:
    - Reliability (25%)
    - Security (20%)
    - Scalability (20%)
    - Observability (15%)
    - Deployment Quality (10%)
    - Recovery Capability (10%)
    """

    CATEGORY_PATTERNS = {
        "Reliability": [
            r"chaos", r"resilience", r"health", r"liveness", r"failover",
            r"3k", r"3h", r"availability", r"worker_rel"
        ],
        "Security": [
            r"security", r"secret", r"iam", r"rbac", r"network_sec", r"mtls",
            r"vulnerability", r"cve", r"supply_chain", r"3n", r"threat", r"ai_sec"
        ],
        "Scalability": [
            r"performance", r"capacity", r"throughput", r"latency", r"autoscaling",
            r"load", r"stress", r"soak", r"3j", r"worker_eff", r"bottleneck"
        ],
        "Observability": [
            r"observability", r"logging", r"tracing", r"metrics", r"telemetry",
            r"alert", r"3i", r"siem", r"grafana", r"prometheus"
        ],
        "Deployment Quality": [
            r"deploy", r"iac", r"terraform", r"helm", r"cicd", r"cloud_readiness",
            r"3m", r"3g", r"3b", r"environment", r"migration"
        ],
        "Recovery Capability": [
            r"backup", r"disaster", r"recovery", r"restore", r"pitr", r"bcp",
            r"rto", r"rpo", r"3l", r"storage_backup"
        ],
    }

    def _determine_category(self, identifier: str, source_phase: str) -> str:
        combined = f"{identifier} {source_phase}".lower()
        for cat, patterns in self.CATEGORY_PATTERNS.items():
            for pat in patterns:
                if re.search(pat, combined):
                    return cat
        return "Reliability"

    def normalize(self, bundles: List[RawEvidenceBundle]) -> List[NormalizedEvidenceItem]:
        normalized_items: List[NormalizedEvidenceItem] = []

        for bundle in bundles:
            for payload in bundle.raw_payloads:
                verifier_id = payload.get("verifier_id", payload.get("phase_id", "UNKNOWN-VERIFIER"))
                phase_name = payload.get("phase_name", payload.get("report_title", "General Verification"))
                category = self._determine_category(verifier_id, bundle.source_phase)

                checks = payload.get("checks", [])
                if isinstance(checks, list) and len(checks) > 0:
                    for idx, chk in enumerate(checks):
                        if isinstance(chk, dict):
                            chk_name = chk.get("name", f"Check {idx + 1}")
                            passed = chk.get("passed", True)
                            details = chk.get("details", "")
                            metrics = chk.get("metrics", {})
                        else:
                            chk_name = getattr(chk, "name", f"Check {idx + 1}")
                            passed = getattr(chk, "passed", True)
                            details = getattr(chk, "details", "")
                            metrics = getattr(chk, "metrics", {})

                        status = VerificationStatus.PASSED if passed else VerificationStatus.FAILED
                        severity = RiskLevel.NONE if passed else self._infer_severity(chk_name, details)
                        score = 100.0 if passed else 0.0

                        normalized_items.append(
                            NormalizedEvidenceItem(
                                category=category,
                                subcategory=phase_name,
                                test_id=f"{verifier_id}-{idx + 1}",
                                name=chk_name,
                                status=status,
                                score=score,
                                severity=severity,
                                weight=1.0,
                                details=details,
                                metrics=metrics,
                            )
                        )
                else:
                    # Fallback: Treat the whole report as a single item
                    raw_score = float(payload.get("score", 100.0))
                    status_val = payload.get("status", "PASSED")
                    status = VerificationStatus.PASSED if "PASS" in str(status_val).upper() else VerificationStatus.FAILED
                    severity = RiskLevel.NONE if status == VerificationStatus.PASSED else RiskLevel.HIGH

                    normalized_items.append(
                        NormalizedEvidenceItem(
                            category=category,
                            subcategory=phase_name,
                            test_id=str(verifier_id),
                            name=phase_name,
                            status=status,
                            score=raw_score,
                            severity=severity,
                            weight=1.0,
                            details=payload.get("summary", ""),
                            metrics={},
                        )
                    )

        return normalized_items

    def _infer_severity(self, name: str, details: str) -> RiskLevel:
        combined = f"{name} {details}".lower()
        if any(w in combined for w in ["critical", "corruption", "data loss", "unauthenticated", "cve"]):
            return RiskLevel.CRITICAL
        if any(w in combined for w in ["high", "restore fail", "timeout", "escape", "leak"]):
            return RiskLevel.HIGH
        if any(w in combined for w in ["medium", "latency", "degraded", "warning"]):
            return RiskLevel.MEDIUM
        return RiskLevel.LOW
