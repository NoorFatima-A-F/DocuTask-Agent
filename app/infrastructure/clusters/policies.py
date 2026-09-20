"""Cluster-Level Policy Engine and Workload Enforcement."""

from typing import Any, Dict, List, Optional, Tuple
from .models import Cluster


class ClusterPolicyEngine:
    """Evaluates whether a cluster satisfies workload, security, and compliance policies."""

    def validate_workload_support(self, cluster: Cluster, workload_type: str) -> Tuple[bool, List[str]]:
        if workload_type not in cluster.supported_workloads:
            return False, [f"Cluster '{cluster.cluster_id}' does not support workload '{workload_type}'."]
        return True, []

    def validate_compliance(
        self, cluster: Cluster, required_compliance: List[str]
    ) -> Tuple[bool, List[str]]:
        violations = []
        cluster_comps = set(cluster.compliance_profiles)
        for comp in required_compliance:
            if comp not in cluster_comps:
                violations.append(f"Cluster '{cluster.cluster_id}' lacks compliance profile '{comp}'.")
        return len(violations) == 0, violations

    def validate_tenant_affinity(
        self, cluster: Cluster, tenant_id: str
    ) -> Tuple[bool, List[str]]:
        if cluster.tenant_affinity and tenant_id not in cluster.tenant_affinity:
            return False, [f"Cluster '{cluster.cluster_id}' is restricted, excluding tenant '{tenant_id}'."]
        return True, []

    def validate_capacity_threshold(
        self, cluster: Cluster, max_utilization_pct: float = 0.90
    ) -> Tuple[bool, List[str]]:
        if cluster.capacity.total_cpu_cores > 0:
            utilization = cluster.capacity.utilized_cpu_cores / cluster.capacity.total_cpu_cores
            if utilization > max_utilization_pct:
                return False, [
                    f"Cluster '{cluster.cluster_id}' CPU utilization ({utilization*100:.1f}%) exceeds safety threshold ({max_utilization_pct*100:.1f}%)."
                ]
        return True, []

    @classmethod
    def evaluate_cluster_policy(
        cls,
        cluster: Cluster,
        workload_type: str,
        required_compliance: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
        max_cpu_utilization_threshold: float = 0.90,
    ) -> Tuple[bool, List[str]]:
        reasons: List[str] = []

        # 1. Workload Support
        if workload_type not in cluster.supported_workloads:
            reasons.append(
                f"Cluster '{cluster.cluster_id}' does not support workload type '{workload_type}'."
            )

        # 2. Compliance Profile
        if required_compliance:
            for comp in required_compliance:
                if comp not in cluster.compliance_profiles:
                    reasons.append(
                        f"Cluster '{cluster.cluster_id}' lacks required compliance profile '{comp}'."
                    )

        # 3. Tenant Affinity
        if cluster.tenant_affinity and tenant_id:
            if tenant_id not in cluster.tenant_affinity:
                reasons.append(
                    f"Cluster '{cluster.cluster_id}' is restricted to specific tenants, excluding '{tenant_id}'."
                )

        # 4. Capacity Utilization Bound
        if cluster.capacity.total_cpu_cores > 0:
            utilization = cluster.capacity.utilized_cpu_cores / cluster.capacity.total_cpu_cores
            if utilization > max_cpu_utilization_threshold:
                reasons.append(
                    f"Cluster '{cluster.cluster_id}' CPU utilization ({utilization*100:.1f}%) exceeds safety threshold ({max_cpu_utilization_threshold*100:.1f}%)."
                )

        return len(reasons) == 0, reasons
