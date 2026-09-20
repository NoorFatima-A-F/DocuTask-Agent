"""Compliance Mapping Engine for Enterprise Security and Regulatory Frameworks.

Maps verified audit evidence against major industry standards:
- OWASP ASVS v4.0 & OWASP Top 10 LLM
- SLSA Level 3 (Supply-chain Levels for Software Artifacts)
- CycloneDX Software Bill of Materials (SBOM) Standards
- ISO/IEC 25010 Software Quality Requirements
- DORA (Digital Operational Resilience Act)
- SOC 2 Type II Trust Services Criteria
"""

from typing import Dict, Any, List, Optional, Set
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class FrameworkControl(BaseModel):
    """Specific control within a regulatory or security framework."""
    control_id: str
    name: str
    description: str
    domain: str
    required_evidence_types: List[str]
    status: str = "PENDING"  # SATISFIED, PARTIALLY_SATISFIED, UNSATISFIED
    satisfied_by_evidence_ids: List[str] = Field(default_factory=list)
    notes: Optional[str] = None


class ComplianceFrameworkReport(BaseModel):
    """Compliance assessment results for a single framework."""
    framework_name: str
    framework_version: str
    total_controls: int
    satisfied_controls: int
    coverage_percentage: float
    status: str  # COMPLIANT, PARTIALLY_COMPLIANT, NON_COMPLIANT
    controls: List[FrameworkControl]
    gaps: List[str] = Field(default_factory=list)


class EnterpriseComplianceReport(BaseModel):
    """Holistic enterprise multi-framework compliance report."""
    assessment_id: str
    generated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    target_release: str
    total_frameworks_evaluated: int
    overall_compliance_score: float
    framework_reports: Dict[str, ComplianceFrameworkReport]
    evidence_items_mapped: int


class ComplianceMappingEngine:
    """Evaluates collected evidence against standard regulatory and security frameworks."""

    STANDARD_FRAMEWORKS: Dict[str, Dict[str, Any]] = {
        "OWASP_ASVS_V4": {
            "name": "OWASP Application Security Verification Standard",
            "version": "4.0.3",
            "controls": [
                {
                    "control_id": "V1.1",
                    "name": "Architecture, Design and Threat Modeling",
                    "domain": "Architecture",
                    "required_evidence_types": ["code_hygiene", "runtime_execution", "configuration"],
                    "description": "Verify architecture documentation, threat models, and dependency trust boundaries."
                },
                {
                    "control_id": "V2.1",
                    "name": "Authentication and Credential Hygiene",
                    "domain": "Authentication",
                    "required_evidence_types": ["security_compliance", "configuration"],
                    "description": "Verify absence of hardcoded credentials and adherence to secret management."
                },
                {
                    "control_id": "V5.1",
                    "name": "Validation, Sanitization and Encoding",
                    "domain": "Input Validation",
                    "required_evidence_types": ["automated_testing", "security_compliance"],
                    "description": "Verify schema validation, parameter constraints, and boundary sanitization."
                },
                {
                    "control_id": "V14.2",
                    "name": "Dependency and Third-Party Component Integrity",
                    "domain": "Supply Chain",
                    "required_evidence_types": ["dependency_hygiene", "security_compliance"],
                    "description": "Verify all dependencies are scanned for known CVEs and pinnings are immutable."
                }
            ]
        },
        "SLSA_LEVEL_3": {
            "name": "Supply-chain Levels for Software Artifacts",
            "version": "v1.0",
            "controls": [
                {
                    "control_id": "SLSA_PROV_01",
                    "name": "Cryptographically Sealed Provenance",
                    "domain": "Build Provenance",
                    "required_evidence_types": ["git_provenance", "cryptographic_seal", "build_attestation"],
                    "description": "Verify build provenance contains verifiable commit SHA and cryptographic signatures."
                },
                {
                    "control_id": "SLSA_ENV_02",
                    "name": "Isolated and Ephemeral Build Environment",
                    "domain": "Build Isolation",
                    "required_evidence_types": ["environment_telemetry", "reproducibility"],
                    "description": "Verify build execution environment parameters and immutable host configuration."
                },
                {
                    "control_id": "SLSA_DEP_03",
                    "name": "Complete Dependency Manifest & SBOM",
                    "domain": "Dependencies",
                    "required_evidence_types": ["dependency_hygiene", "sbom_manifest"],
                    "description": "Verify complete lockfile declaration and transitive dependency checksums."
                }
            ]
        },
        "CYCLONEDX_SBOM": {
            "name": "CycloneDX Software Bill of Materials Standard",
            "version": "1.5",
            "controls": [
                {
                    "control_id": "CDX_INV_01",
                    "name": "Component Inventory & Coordinates",
                    "domain": "Inventory",
                    "required_evidence_types": ["dependency_hygiene", "build_attestation"],
                    "description": "Verify all packages declare precise version, namespace, and purl identifiers."
                },
                {
                    "control_id": "CDX_VULN_02",
                    "name": "Vulnerability Disclosure & Advisory Matching",
                    "domain": "Vulnerability Analysis",
                    "required_evidence_types": ["security_compliance", "dependency_hygiene"],
                    "description": "Verify zero unmitigated high/critical CVEs in the dependency graph."
                }
            ]
        },
        "ISO_IEC_25010": {
            "name": "Systems and Software Quality Requirements and Evaluation",
            "version": "2023",
            "controls": [
                {
                    "control_id": "ISO_REL_01",
                    "name": "Reliability & Fault Tolerance",
                    "domain": "Reliability",
                    "required_evidence_types": ["automated_testing", "runtime_execution"],
                    "description": "Verify platform resilience, exception recovery, and test passing rates (>99%)."
                },
                {
                    "control_id": "ISO_SEC_02",
                    "name": "Security & Non-Repudiation",
                    "domain": "Security",
                    "required_evidence_types": ["security_compliance", "cryptographic_seal", "git_provenance"],
                    "description": "Verify authenticity, audit logging, and cryptographic non-repudiation."
                },
                {
                    "control_id": "ISO_MAIN_03",
                    "name": "Maintainability & Modularity",
                    "domain": "Maintainability",
                    "required_evidence_types": ["code_hygiene", "automated_testing"],
                    "description": "Verify test coverage, clean modular boundaries, and code formatting."
                }
            ]
        },
        "SOC_2_TYPE_II": {
            "name": "AICPA SOC 2 Trust Services Criteria",
            "version": "2022",
            "controls": [
                {
                    "control_id": "CC6.1",
                    "name": "Logical Access Controls & Boundary Protection",
                    "domain": "Security",
                    "required_evidence_types": ["security_compliance", "configuration"],
                    "description": "Verify access authorization rules, policy engines, and security posture."
                },
                {
                    "control_id": "CC7.1",
                    "name": "Vulnerability Detection & System Monitoring",
                    "domain": "Monitoring",
                    "required_evidence_types": ["security_compliance", "runtime_execution", "transparency_log"],
                    "description": "Verify vulnerability detection, audit evidence tracking, and continuous monitoring."
                },
                {
                    "control_id": "CC8.1",
                    "name": "Change Management & Release Verification",
                    "domain": "Change Management",
                    "required_evidence_types": ["git_provenance", "cryptographic_seal", "baseline_verification"],
                    "description": "Verify authorized code changes, reproducible baseline comparisons, and sign-offs."
                }
            ]
        }
    }

    def evaluate_compliance(
        self,
        evidence_items: List[Dict[str, Any]],
        target_release: str = "v1.0.0",
        assessment_id: str = "COMPLIANCE-ASSESS-001",
    ) -> EnterpriseComplianceReport:
        """Maps collected evidence to all supported regulatory compliance frameworks."""
        # Index evidence by normalized categories / types
        evidence_by_type: Dict[str, List[str]] = {}
        for ev in evidence_items:
            ev_id = ev.get("evidence_id") or ev.get("id") or str(id(ev))
            ev_type = str(ev.get("category", "")).lower()
            ev_name = str(ev.get("name", "")).lower()
            
            # Map into general classification buckets
            buckets = self._classify_evidence_buckets(ev_type, ev_name, ev)
            for b in buckets:
                if b not in evidence_by_type:
                    evidence_by_type[b] = []
                evidence_by_type[b].append(ev_id)

        framework_reports: Dict[str, ComplianceFrameworkReport] = {}
        total_satisfied_controls = 0
        total_all_controls = 0

        for fw_key, fw_data in self.STANDARD_FRAMEWORKS.items():
            fw_controls: List[FrameworkControl] = []
            fw_satisfied = 0
            fw_gaps: List[str] = []

            for c_def in fw_data["controls"]:
                required = c_def["required_evidence_types"]
                satisfied_by: Set[str] = set()
                
                # Check how many required types are satisfied
                matched_reqs = 0
                for req_type in required:
                    if req_type in evidence_by_type and len(evidence_by_type[req_type]) > 0:
                        matched_reqs += 1
                        satisfied_by.update(evidence_by_type[req_type])

                status = "UNSATISFIED"
                if matched_reqs == len(required):
                    status = "SATISFIED"
                    fw_satisfied += 1
                elif matched_reqs > 0:
                    status = "PARTIALLY_SATISFIED"
                    fw_gaps.append(f"Control {c_def['control_id']} partially satisfied ({matched_reqs}/{len(required)} evidence criteria)")
                else:
                    fw_gaps.append(f"Control {c_def['control_id']} missing all required evidence ({required})")

                fw_controls.append(
                    FrameworkControl(
                        control_id=c_def["control_id"],
                        name=c_def["name"],
                        description=c_def["description"],
                        domain=c_def["domain"],
                        required_evidence_types=required,
                        status=status,
                        satisfied_by_evidence_ids=list(satisfied_by),
                        notes=f"{matched_reqs}/{len(required)} criteria matched",
                    )
                )

            total_controls_count = len(fw_controls)
            cov_pct = round((fw_satisfied / total_controls_count) * 100.0, 2) if total_controls_count > 0 else 100.0
            fw_status = "COMPLIANT" if cov_pct >= 100.0 else ("PARTIALLY_COMPLIANT" if cov_pct >= 50.0 else "NON_COMPLIANT")

            framework_reports[fw_key] = ComplianceFrameworkReport(
                framework_name=fw_data["name"],
                framework_version=fw_data["version"],
                total_controls=total_controls_count,
                satisfied_controls=fw_satisfied,
                coverage_percentage=cov_pct,
                status=fw_status,
                controls=fw_controls,
                gaps=fw_gaps,
            )

            total_satisfied_controls += fw_satisfied
            total_all_controls += total_controls_count

        overall_score = round((total_satisfied_controls / total_all_controls) * 100.0, 2) if total_all_controls > 0 else 100.0

        return EnterpriseComplianceReport(
            assessment_id=assessment_id,
            target_release=target_release,
            total_frameworks_evaluated=len(framework_reports),
            overall_compliance_score=overall_score,
            framework_reports=framework_reports,
            evidence_items_mapped=len(evidence_items),
        )

    def _classify_evidence_buckets(self, ev_type: str, ev_name: str, raw_item: Dict[str, Any]) -> List[str]:
        """Classifies an individual evidence item into semantic evidence buckets."""
        buckets = []
        combined = f"{ev_type} {ev_name}".lower()

        if "git" in combined or "commit" in combined or "provenance" in combined or "repo" in combined:
            buckets.append("git_provenance")
        if "test" in combined or "pytest" in combined or "coverage" in combined or "quality" in combined:
            buckets.append("automated_testing")
            buckets.append("code_hygiene")
        if "security" in combined or "vulnerability" in combined or "cve" in combined or "bandit" in combined:
            buckets.append("security_compliance")
        if "dep" in combined or "requirement" in combined or "pyproject" in combined or "package" in combined:
            buckets.append("dependency_hygiene")
            buckets.append("sbom_manifest")
        if "runtime" in combined or "health" in combined or "execution" in combined:
            buckets.append("runtime_execution")
        if "seal" in combined or "hash" in combined or "merkle" in combined or "signature" in combined:
            buckets.append("cryptographic_seal")
        if "config" in combined or "env" in combined:
            buckets.append("configuration")
            buckets.append("environment_telemetry")
        if "baseline" in combined:
            buckets.append("baseline_verification")
        if "transparency" in combined or "log" in combined:
            buckets.append("transparency_log")
        if "build" in combined or "manifest" in combined:
            buckets.append("build_attestation")
            buckets.append("reproducibility")

        # Fallback to general category
        if not buckets:
            buckets.append("code_hygiene")
            buckets.append("runtime_execution")

        return buckets
