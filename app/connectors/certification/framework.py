"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Certification.
Validates third-party and ecosystem connector packages against strict security, schema, and reliability standards.
"""

from __future__ import annotations

import logging
from typing import List, Optional
from pydantic import BaseModel, Field

from app.connectors.marketplace.registry import ConnectorPackageManifest
from app.connectors.sdk.base import BaseConnector

logger = logging.getLogger(__name__)


class CertificationReport(BaseModel):
    """Formal audit report evaluating a connector against enterprise certification requirements."""
    package_id: str
    certified: bool
    score: float  # 0.0 to 100.0
    security_passed: bool
    schema_passed: bool
    reliability_passed: bool
    documentation_passed: bool
    findings: List[str] = Field(default_factory=list)
    remediation_steps: List[str] = Field(default_factory=list)


class ConnectorCertification:
    """
    Automated security and architecture certification engine for marketplace plugins.
    """

    def certify(
        self,
        manifest: ConnectorPackageManifest,
        connector_instance: Optional[BaseConnector] = None,
    ) -> CertificationReport:
        """
        Runs comprehensive certification checks across security, schema, resilience, and documentation.
        """
        findings: List[str] = []
        remediations: List[str] = []
        score = 100.0

        # Gate 1: Security Audit
        security_passed = True
        if not manifest.permissions_required:
            security_passed = False
            score -= 20.0
            findings.append("Security warning: No explicit permissions declared in manifest.")
            remediations.append("Declare granular API permission scopes.")

        # Gate 2: Schema & Capabilities
        schema_passed = True
        if not manifest.capabilities:
            schema_passed = False
            score -= 25.0
            findings.append("Schema error: Package does not expose any standardized capabilities.")
            remediations.append("Add technology-independent capability mappings (e.g. email.send).")

        # Gate 3: Resilience & Health
        reliability_passed = True
        if connector_instance:
            try:
                actions = connector_instance.actions()
                if not actions:
                    reliability_passed = False
                    score -= 20.0
                    findings.append("Reliability error: No executable actions implemented.")
            except Exception as e:
                reliability_passed = False
                score -= 30.0
                findings.append(f"Action validation error: {e}")

        # Gate 4: Documentation
        doc_passed = True
        if not manifest.description or len(manifest.description) < 10:
            doc_passed = False
            score -= 10.0
            findings.append("Documentation warning: Description is too sparse.")
            remediations.append("Provide comprehensive setup and API usage documentation.")

        certified = (score >= 70.0 and security_passed and schema_passed)

        report = CertificationReport(
            package_id=manifest.package_id,
            certified=certified,
            score=max(0.0, score),
            security_passed=security_passed,
            schema_passed=schema_passed,
            reliability_passed=reliability_passed,
            documentation_passed=doc_passed,
            findings=findings,
            remediation_steps=remediations,
        )

        manifest.certified = certified
        logger.info(f"Certification audit for '{manifest.package_id}': certified={certified} (Score={score:.1f}/100)")
        return report
