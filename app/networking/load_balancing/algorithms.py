"""Load Balancing Algorithms and Node Selection."""

from __future__ import annotations

import bisect
import hashlib
import random
from typing import Dict, List, Optional

from ..discovery.registry import ServiceEndpoint
from ..routing.policies import LoadBalancingAlgorithm


class LoadBalancerEngine:
    """Implements enterprise multi-algorithm load balancing over service endpoints."""

    def __init__(self):
        self._round_robin_indices: Dict[str, int] = {}
        self._active_connections: Dict[str, int] = {}

    def record_connection_start(self, endpoint_id: str) -> None:
        self._active_connections[endpoint_id] = self._active_connections.get(endpoint_id, 0) + 1

    def record_connection_end(self, endpoint_id: str) -> None:
        if endpoint_id in self._active_connections:
            self._active_connections[endpoint_id] = max(0, self._active_connections[endpoint_id] - 1)

    def select_endpoint(
        self,
        endpoints: List[ServiceEndpoint],
        algorithm: LoadBalancingAlgorithm = LoadBalancingAlgorithm.ROUND_ROBIN,
        hash_key: Optional[str] = None,
        caller_region: Optional[str] = None,
        caller_zone: Optional[str] = None,
    ) -> Optional[ServiceEndpoint]:
        """Select an endpoint from the candidate list according to the specified algorithm."""
        if not endpoints:
            return None

        healthy_endpoints = [ep for ep in endpoints if ep.is_healthy]
        if not healthy_endpoints:
            # If all are marked unhealthy, fallback to all endpoints
            healthy_endpoints = endpoints

        if len(healthy_endpoints) == 1:
            return healthy_endpoints[0]

        if algorithm == LoadBalancingAlgorithm.ROUND_ROBIN:
            return self._select_round_robin(healthy_endpoints)
        elif algorithm == LoadBalancingAlgorithm.WEIGHTED_ROUND_ROBIN:
            return self._select_weighted_round_robin(healthy_endpoints)
        elif algorithm == LoadBalancingAlgorithm.LEAST_REQUEST:
            return self._select_least_request(healthy_endpoints)
        elif algorithm == LoadBalancingAlgorithm.CONSISTENT_HASH:
            return self._select_consistent_hash(healthy_endpoints, hash_key or "default_key")
        elif algorithm == LoadBalancingAlgorithm.LOCALITY_PRIORITIZED:
            return self._select_locality_prioritized(healthy_endpoints, caller_region, caller_zone)
        else:
            return self._select_round_robin(healthy_endpoints)

    def _select_round_robin(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        service_key = f"{endpoints[0].namespace}/{endpoints[0].service_name}"
        idx = self._round_robin_indices.get(service_key, 0)
        selected = endpoints[idx % len(endpoints)]
        self._round_robin_indices[service_key] = (idx + 1) % len(endpoints)
        return selected

    def _select_weighted_round_robin(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        total_weight = sum(ep.weight for ep in endpoints)
        if total_weight <= 0:
            return self._select_round_robin(endpoints)

        rand_val = random.uniform(0, total_weight)
        cumulative = 0.0
        for ep in endpoints:
            cumulative += ep.weight
            if rand_val <= cumulative:
                return ep
        return endpoints[-1]

    def _select_least_request(self, endpoints: List[ServiceEndpoint]) -> ServiceEndpoint:
        min_conns = float("inf")
        best_ep = endpoints[0]
        for ep in endpoints:
            conns = self._active_connections.get(ep.endpoint_id, 0)
            if conns < min_conns:
                min_conns = conns
                best_ep = ep
        return best_ep

    def _select_consistent_hash(self, endpoints: List[ServiceEndpoint], hash_key: str) -> ServiceEndpoint:
        # Build consistent hashing ring with virtual nodes
        ring: List[tuple[int, ServiceEndpoint]] = []
        for ep in endpoints:
            for v_idx in range(50):  # 50 virtual nodes per endpoint
                v_key = f"{ep.endpoint_id}#{v_idx}".encode("utf-8")
                node_hash = int(hashlib.sha256(v_key).hexdigest(), 16)
                ring.append((node_hash, ep))

        ring.sort(key=lambda x: x[0])
        req_hash = int(hashlib.sha256(hash_key.encode("utf-8")).hexdigest(), 16)

        # Binary search for the first node with hash >= req_hash
        ring_hashes = [r[0] for r in ring]
        pos = bisect.bisect_left(ring_hashes, req_hash)
        if pos == len(ring):
            pos = 0  # wrap around the ring
        return ring[pos][1]

    def _select_locality_prioritized(
        self,
        endpoints: List[ServiceEndpoint],
        caller_region: Optional[str],
        caller_zone: Optional[str],
    ) -> ServiceEndpoint:
        if caller_zone:
            same_zone = [ep for ep in endpoints if ep.zone == caller_zone]
            if same_zone:
                return self._select_round_robin(same_zone)

        if caller_region:
            same_region = [ep for ep in endpoints if ep.region == caller_region]
            if same_region:
                return self._select_round_robin(same_region)

        return self._select_round_robin(endpoints)
