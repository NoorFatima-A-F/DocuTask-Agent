"""Causal Experience Graph for DocuTask ADIP Collective Intelligence.

Indexes past mission executions, causal dependency outcomes, strategy performance signatures,
and failure recovery patterns to enable lifelong organizational learning.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ExperienceNode(BaseModel):
    """Causal node in the global experience graph."""
    node_id: str = Field(default_factory=lambda: f"exp_{uuid.uuid4().hex[:8]}")
    mission_id: str
    document_signature: str
    strategy_archetype: str
    observed_latency_ms: float
    observed_cost_usd: float
    observed_accuracy: float
    success: bool
    failure_mode: Optional[str] = None
    applied_recovery_path: Optional[str] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CausalExperienceGraph:
    """Graph structure connecting missions, document signatures, strategies, and outcomes."""

    def __init__(self) -> None:
        self._nodes: Dict[str, ExperienceNode] = {}
        self._by_signature: Dict[str, List[str]] = {}
        self._seed_sample_experiences()

    def _seed_sample_experiences(self) -> None:
        sample_data = [
            ("inv_financial_p2", "DELTA_PARETO", 1850.0, 0.0035, 0.985, True, None, None),
            ("inv_financial_p4", "BETA_ACCURATE", 3400.0, 0.0150, 0.994, True, None, None),
            ("receipt_retail_p1", "ALPHA_FAST", 520.0, 0.0008, 0.910, True, None, None),
            ("tax_1040_p5", "BETA_ACCURATE", 4100.0, 0.0185, 0.998, True, None, None),
            ("corrupted_scan_p1", "ALPHA_FAST", 1200.0, 0.0012, 0.650, False, "OCR_BLUR", "ESCALATE_CLOUD_VISION"),
            ("bill_lading_p3", "DELTA_PARETO", 2200.0, 0.0048, 0.982, True, None, None),
        ]
        for sig, arch, lat, cost, acc, succ, fail, rec in sample_data:
            self.record_experience(
                mission_id=f"hist_m_{uuid.uuid4().hex[:6]}",
                document_signature=sig,
                strategy_archetype=arch,
                observed_latency_ms=lat,
                observed_cost_usd=cost,
                observed_accuracy=acc,
                success=succ,
                failure_mode=fail,
                applied_recovery_path=rec,
            )

    def record_experience(
        self,
        mission_id: str,
        document_signature: str,
        strategy_archetype: str,
        observed_latency_ms: float,
        observed_cost_usd: float,
        observed_accuracy: float,
        success: bool,
        failure_mode: Optional[str] = None,
        applied_recovery_path: Optional[str] = None,
    ) -> ExperienceNode:
        node = ExperienceNode(
            mission_id=mission_id,
            document_signature=document_signature,
            strategy_archetype=strategy_archetype,
            observed_latency_ms=observed_latency_ms,
            observed_cost_usd=observed_cost_usd,
            observed_accuracy=observed_accuracy,
            success=success,
            failure_mode=failure_mode,
            applied_recovery_path=applied_recovery_path,
        )
        self._nodes[node.node_id] = node
        if document_signature not in self._by_signature:
            self._by_signature[document_signature] = []
        self._by_signature[document_signature].append(node.node_id)
        return node

    def query_similar_experiences(self, signature_prefix: str) -> List[ExperienceNode]:
        results: List[ExperienceNode] = []
        for sig, node_ids in self._by_signature.items():
            if signature_prefix.lower() in sig.lower():
                for nid in node_ids:
                    results.append(self._nodes[nid])
        return results

    def get_total_indexed(self) -> int:
        return len(self._nodes)
