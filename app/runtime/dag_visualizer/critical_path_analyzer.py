"""
ARTEICP Dynamic DAG - Critical Path Method (CPM) Analyzer
Computes Early Start (ES), Late Start (LS), Total Float/Slack, and identifies critical bottleneck vertices.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class CPMNodeAnalysis:
    node_id: str
    duration_ms: float
    early_start_ms: float
    early_finish_ms: float
    late_start_ms: float
    late_finish_ms: float
    slack_ms: float
    is_critical: bool

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class CriticalPathAnalyzer:
    """Computes rigorous Critical Path Method (CPM) forward and backward passes on execution DAGs."""

    @classmethod
    def analyze_dag(
        cls,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        {n["id"]: n for n in nodes}
        durations = {n["id"]: float(n.get("duration_ms", 10.0)) for n in nodes}

        # Build adjacency lists
        adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}
        rev_adj: Dict[str, List[str]] = {n["id"]: [] for n in nodes}

        for e in edges:
            u, v = e["source"], e["target"]
            if u in adj and v in rev_adj:
                adj[u].append(v)
                rev_adj[v].append(u)

        # 1. Forward Pass (Early Start / Early Finish)
        es: Dict[str, float] = {}
        ef: Dict[str, float] = {}

        for n_id in nodes:
            nid = n_id["id"]
            if not rev_adj[nid]:
                es[nid] = 0.0
                ef[nid] = durations[nid]
            else:
                max_pred = max(ef.get(p, 0.0) for p in rev_adj[nid])
                es[nid] = max_pred
                ef[nid] = max_pred + durations[nid]

        max_project_dur = max(ef.values()) if ef else 0.0

        # 2. Backward Pass (Late Start / Late Finish)
        lf: Dict[str, float] = {}
        ls: Dict[str, float] = {}

        for n_id in reversed(nodes):
            nid = n_id["id"]
            if not adj[nid]:
                lf[nid] = max_project_dur
                ls[nid] = max_project_dur - durations[nid]
            else:
                min_succ = min(ls.get(s, max_project_dur) for s in adj[nid])
                lf[nid] = min_succ
                ls[nid] = min_succ - durations[nid]

        # 3. Slacks & Critical Path (slack == 0)
        cpm_nodes: List[CPMNodeAnalysis] = []
        critical_node_ids: List[str] = []

        for n_id in nodes:
            nid = n_id["id"]
            slack = round(lf[nid] - ef[nid], 2)
            is_crit = abs(slack) < 1e-3

            if is_crit:
                critical_node_ids.append(nid)

            cpm_nodes.append(
                CPMNodeAnalysis(
                    node_id=nid,
                    duration_ms=durations[nid],
                    early_start_ms=round(es[nid], 1),
                    early_finish_ms=round(ef[nid], 1),
                    late_start_ms=round(ls[nid], 1),
                    late_finish_ms=round(lf[nid], 1),
                    slack_ms=slack,
                    is_critical=is_crit,
                )
            )

        return {
            "total_project_duration_ms": round(max_project_dur, 1),
            "critical_path_node_ids": critical_node_ids,
            "critical_path_length": len(critical_node_ids),
            "node_analysis": [c.to_dict() for c in cpm_nodes],
        }
