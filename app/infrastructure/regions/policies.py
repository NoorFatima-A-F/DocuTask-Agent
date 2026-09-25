"""Regional Governance, Data Residency, and Compliance Policies."""

from typing import List, Tuple
from app.infrastructure.regions.models import Region, RegionStatus


class RegionPolicyEngine:
    """Evaluates regional compliance, data residency, and boundary governance."""

    def evaluate_data_residency(
        self, region: Region, required_jurisdiction: str
    ) -> Tuple[bool, List[str]]:
        """Validate whether a region satisfies data residency jurisdiction constraints."""
        violations = []
        if required_jurisdiction.upper() == "GLOBAL":
            return True, []

        region_jurisdiction = region.data_residency_jurisdiction.upper()
        geo_jurisdiction = region.geography.jurisdiction.upper()

        if region_jurisdiction != required_jurisdiction.upper() and geo_jurisdiction != required_jurisdiction.upper():
            violations.append(
                f"Data residency violation: region '{region.region_id}' operates in jurisdiction "
                f"'{region_jurisdiction}/{geo_jurisdiction}', required '{required_jurisdiction}'."
            )

        return len(violations) == 0, violations

    def validate_compliance(
        self, region: Region, required_certifications: List[str]
    ) -> Tuple[bool, List[str]]:
        """Validate if region holds all required compliance certifications."""
        violations = []
        region_certs = set(c.upper() for c in region.compliance_certifications)

        for cert in required_certifications:
            if cert.upper() not in region_certs:
                violations.append(
                    f"Compliance violation: region '{region.region_id}' lacks certification '{cert}'."
                )

        return len(violations) == 0, violations

    def validate_egress_policy(
        self, source_region: Region, target_region: Region
    ) -> Tuple[bool, List[str]]:
        """Validate whether data transmission between source and target region is legally permitted."""
        violations = []
        # Strictest rule: EU data cannot freely egress to non-adequate jurisdiction without gateway
        src_juris = source_region.data_residency_jurisdiction.upper()
        dst_juris = target_region.data_residency_jurisdiction.upper()

        if src_juris == "EU" and dst_juris != "EU":
            if not source_region.egress_gateways and not target_region.egress_gateways:
                violations.append(
                    f"Egress policy violation: Cross-border egress from EU region '{source_region.region_id}' "
                    f"to '{target_region.region_id}' ({dst_juris}) requires verified egress gateway."
                )

        return len(violations) == 0, violations

    def check_regional_quorum(
        self, active_regions: List[Region], min_quorum_count: int = 2
    ) -> bool:
        """Check if minimum quorum of ACTIVE regions is maintained for distributed consensus."""
        healthy_active = [
            r for r in active_regions if r.status == RegionStatus.ACTIVE
        ]
        return len(healthy_active) >= min_quorum_count
