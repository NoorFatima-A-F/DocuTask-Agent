"""Affinity and Anti-Affinity Evaluation Engine."""

from app.infrastructure.executions.workload import WorkloadRequest
from app.infrastructure.workers.models import Worker
from app.infrastructure.topology.locality import DataLocalityResolver


class AffinityEngine:
    """Calculates affinity bonuses and anti-affinity penalties for worker placement."""

    def calculate_affinity_score(self, worker: Worker, workload: WorkloadRequest) -> float:
        """Calculate composite affinity score (positive = preferred, negative = penalized)."""
        score = 0.0

        # 1. Worker Label Affinity
        if workload.affinity_tags:
            for k, v in workload.affinity_tags.items():
                if worker.labels.get(k) == str(v):
                    score += 20.0

        # 2. Worker Anti-Affinity (Penalize matching anti-affinity labels)
        if workload.anti_affinity_tags:
            for k, v in workload.anti_affinity_tags.items():
                if worker.labels.get(k) == str(v):
                    score -= 50.0

        # 3. Data Locality Affinity
        if workload.data_locality_uri:
            loc_region = DataLocalityResolver.resolve_locality_region(workload.data_locality_uri)
            if loc_region and worker.region_id == loc_region:
                score += 30.0

        # 4. Region Preference Affinity
        if workload.region_preferences and worker.region_id in workload.region_preferences:
            rank = workload.region_preferences.index(worker.region_id)
            score += max(5.0, 25.0 - (rank * 5.0))

        return score
