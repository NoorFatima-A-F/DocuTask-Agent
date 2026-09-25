"""
DocuTask Agent - Dynamic Blast-Radius Evaluation Engine
Phase 12: Autonomous Production Reliability & Operational Resilience (APRCORP+)
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
import time
from app.runtime.resilience.dependency.graph import dependency_graph


@dataclass
class BlastRadiusAnalysis:
    failed_node_id: str
    failed_node_name: str
    criticality: str
    impacted_nodes: List[str]
    blast_radius_pct: float
    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CATASTROPHIC"
    isolation_recommended: bool
    recommended_mitigation: str
    analyzed_at_utc: float = field(default_factory=time.time)


class BlastRadiusEngine:
    """
    Blast-Radius Analysis Engine.
    Quantifies the exact topological blast radius if any component fails.
    """

    @staticmethod
    def analyze_node_failure(node_id: str) -> BlastRadiusAnalysis:
        node = dependency_graph.get_node(node_id)
        if not node:
            return BlastRadiusAnalysis(
                failed_node_id=node_id,
                failed_node_name="Unknown Node",
                criticality="LOW",
                impacted_nodes=[],
                blast_radius_pct=0.0,
                risk_level="LOW",
                isolation_recommended=False,
                recommended_mitigation="No action required for unknown node.",
            )

        impacted = dependency_graph.get_downstream_impacted(node_id)
        all_nodes = dependency_graph.list_nodes()
        total_count = max(1, len(all_nodes))
        blast_pct = round((len(impacted) / total_count) * 100.0, 2)

        if blast_pct >= 50.0 or node.criticality == "CRITICAL":
            risk = "CATASTROPHIC" if blast_pct >= 70.0 else "HIGH"
            isolation = True
            mitigation = f"Activate circuit breaker on {node_id} and switch to redundant replica pool."
        elif blast_pct >= 25.0:
            risk = "MEDIUM"
            isolation = True
            mitigation = f"Isolate {node_id} and activate warm-start cache fallback."
        else:
            risk = "LOW"
            isolation = False
            mitigation = f"Gracefully retry operations with exponential backoff."

        return BlastRadiusAnalysis(
            failed_node_id=node.id,
            failed_node_name=node.name,
            criticality=node.criticality,
            impacted_nodes=impacted,
            blast_radius_pct=blast_pct,
            risk_level=risk,
            isolation_recommended=isolation,
            recommended_mitigation=mitigation,
        )

    @staticmethod
    def get_full_topology_risk_matrix() -> List[Dict[str, Any]]:
        """Returns blast radius analysis for every node in the graph."""
        nodes = dependency_graph.list_nodes()
        return [BlastRadiusEngine.analyze_node_failure(n.id).__dict__ for n in nodes]


# Global singleton instance
blast_radius_engine = BlastRadiusEngine()
