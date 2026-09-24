"""Cluster Registry with Persistence and Multi-Criteria Filtering."""

import json
from pathlib import Path
import threading
from typing import Dict, List, Optional, Set, Union

from ..core.exceptions import InfrastructureError
from .capabilities import ClusterCapabilityRegistry
from .health import ClusterHealthAggregator, SubComponentHealth
from .labels import ClusterLabelingSystem
from .lifecycle import ClusterLifecycleStateMachine
from .models import Cluster, ClusterLease, ClusterStatus
from .policies import ClusterPolicyEngine


class ClusterRegistry:
    """Enterprise persistent registry for all global infrastructure clusters."""

    def __init__(
        self,
        capability_registry: Optional[ClusterCapabilityRegistry] = None,
        labeling_system: Optional[ClusterLabelingSystem] = None,
        health_aggregator: Optional[ClusterHealthAggregator] = None,
        storage_path: Optional[Union[str, Path]] = None,
        persistence_path: Optional[Union[str, Path]] = None,
    ) -> None:
        self._clusters: Dict[str, Cluster] = {}
        self.capability_registry = capability_registry or ClusterCapabilityRegistry()
        self.labeling_system = labeling_system or ClusterLabelingSystem()
        self.health_aggregator = health_aggregator or ClusterHealthAggregator()
        self._lock = threading.RLock()

        target_path = persistence_path or storage_path
        self.storage_path = Path(target_path) if target_path else None

        if self.storage_path and self.storage_path.exists():
            self.load_from_storage()

    def register_cluster(self, cluster: Cluster) -> Cluster:
        """Register a new cluster into the platform."""
        with self._lock:
            # Progress through DISCOVERED -> REGISTERING -> REGISTERED -> VALIDATING -> READY -> ACTIVE if discovered
            if cluster.status == ClusterStatus.DISCOVERED:
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.REGISTERING)
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.REGISTERED)
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.VALIDATING)
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.READY)
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.ACTIVE)

            self._clusters[cluster.cluster_id] = cluster

            # Index capabilities & labels
            self.capability_registry.register_capabilities(cluster.cluster_id, cluster.capabilities)
            self.labeling_system.set_labels(cluster.cluster_id, cluster.labels)

            # Initialize heartbeat lease
            lease = self.health_aggregator.report_heartbeat(cluster.cluster_id)
            cluster.active_lease = lease

            self._persist()
            return cluster

    def get_cluster(self, cluster_id: str) -> Optional[Cluster]:
        with self._lock:
            return self._clusters.get(cluster_id)

    def list_clusters(
        self,
        region_id: Optional[str] = None,
        environment: Optional[str] = None,
        status: Optional[ClusterStatus] = None,
    ) -> List[Cluster]:
        with self._lock:
            results = list(self._clusters.values())
            if region_id:
                results = [c for c in results if c.region_id == region_id]
            if environment:
                results = [c for c in results if c.environment == environment]
            if status:
                results = [c for c in results if c.status == status]
            return results

    def transition_state(
        self, cluster_id: str, target_state: ClusterStatus, reason: Optional[str] = None
    ) -> Optional[Cluster]:
        """Transition a cluster lifecycle state."""
        with self._lock:
            cluster = self._clusters.get(cluster_id)
            if not cluster:
                return None
            ClusterLifecycleStateMachine.transition(cluster, target_state, reason=reason or "")
            self._persist()
            return cluster

    def update_cluster_status(self, cluster_id: str, status: ClusterStatus) -> Optional[Cluster]:
        with self._lock:
            cluster = self._clusters.get(cluster_id)
            if not cluster:
                return None
            cluster.status = status
            self._persist()
            return cluster

    def heartbeat(
        self,
        cluster_id: str,
        sub_components: Optional[List[SubComponentHealth]] = None,
        ttl_seconds: int = 60,
    ) -> Optional[ClusterLease]:
        """Record heartbeat and update cluster lease and sub-component health."""
        with self._lock:
            cluster = self._clusters.get(cluster_id)
            if not cluster:
                return None

            lease = self.health_aggregator.create_or_renew_lease(cluster_id, ttl_seconds=ttl_seconds)
            cluster.active_lease = lease

            if sub_components:
                report = self.health_aggregator.evaluate_health(sub_components, cluster_id=cluster_id)
                cluster.health_status = report.status

            self._persist()
            return lease

    def find_eligible_clusters(
        self,
        workload_type: str,
        required_capabilities: Optional[Set[str]] = None,
        required_compliance: Optional[List[str]] = None,
        tenant_id: Optional[str] = None,
        region_id: Optional[str] = None,
    ) -> List[Cluster]:
        """Find all active, healthy clusters matching capabilities and policy requirements."""
        with self._lock:
            eligible: List[Cluster] = []

            for cluster in self._clusters.values():
                if cluster.status != ClusterStatus.ACTIVE:
                    continue

                if region_id and cluster.region_id != region_id:
                    continue

                health = self.health_aggregator.calculate_cluster_health(cluster)
                if health in ["UNHEALTHY", "UNREACHABLE", "MAINTENANCE"]:
                    continue

                if required_capabilities and not self.capability_registry.satisfies_capabilities(
                    cluster.cluster_id, required_capabilities
                ):
                    continue

                satisfied, _ = ClusterPolicyEngine.evaluate_cluster_policy(
                    cluster=cluster,
                    workload_type=workload_type,
                    required_compliance=required_compliance,
                    tenant_id=tenant_id,
                )
                if satisfied:
                    eligible.append(cluster)

            return eligible

    def mark_draining(self, cluster_id: str, reason: str = "") -> Cluster:
        with self._lock:
            cluster = self.get_cluster(cluster_id)
            if not cluster:
                raise InfrastructureError(f"Cluster {cluster_id} not found.")
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.DRAINING, reason=reason)
            self._persist()
            return cluster

    def suspend_cluster(self, cluster_id: str, reason: str = "") -> Cluster:
        with self._lock:
            cluster = self.get_cluster(cluster_id)
            if not cluster:
                raise InfrastructureError(f"Cluster {cluster_id} not found.")
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.SUSPENDED, reason=reason)
            self._persist()
            return cluster

    def enter_maintenance(self, cluster_id: str, reason: str = "") -> Cluster:
        with self._lock:
            cluster = self.get_cluster(cluster_id)
            if not cluster:
                raise InfrastructureError(f"Cluster {cluster_id} not found.")
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.MAINTENANCE, reason=reason)
            self._persist()
            return cluster

    def exit_maintenance(self, cluster_id: str) -> Cluster:
        with self._lock:
            cluster = self.get_cluster(cluster_id)
            if not cluster:
                raise InfrastructureError(f"Cluster {cluster_id} not found.")
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.VALIDATING)
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.READY)
            ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.ACTIVE)
            cluster.maintenance_reason = None
            self._persist()
            return cluster

    def remove_cluster(self, cluster_id: str) -> bool:
        with self._lock:
            cluster = self.get_cluster(cluster_id)
            if not cluster:
                return False
            if cluster.status != ClusterStatus.REMOVED:
                ClusterLifecycleStateMachine.transition(cluster, ClusterStatus.REMOVED)
            del self._clusters[cluster_id]
            self._persist()
            return True

    def delete_cluster(self, cluster_id: str) -> bool:
        return self.remove_cluster(cluster_id)

    def _persist(self) -> None:
        if not self.storage_path:
            return
        try:
            self.storage_path.parent.mkdir(parents=True, exist_ok=True)
            dump = {cid: c.model_dump(mode="json") for cid, c in self._clusters.items()}
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(dump, f, indent=2)
        except Exception:
            pass

    def load_from_storage(self) -> None:
        if not self.storage_path or not self.storage_path.exists():
            return
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._clusters = {cid: Cluster.model_validate(val) for cid, val in data.items()}
        except Exception:
            pass
