"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_engine.py

Master orchestrator coordinating:
- Lineage Tracking across all 7 canonical stages
- Merkle DAG recursive hash verification
- W3C PROV and OpenLineage compliance
- Evidence Quality Level Grading (Levels A, B, C, D, E)
- Quality-Weighted Production Readiness Evaluation
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.provenance.digital_signatures import ProvenanceSigner
from research_validation.provenance.evidence_bundle import EvidenceBundleBuilder, SealedEvidenceBundle
from research_validation.provenance.evidence_graph import EvidenceGraph, LineageAncestryTrace
from research_validation.provenance.evidence_store import EvidenceStore
from research_validation.provenance.lineage_tracker import CompleteLineageChain, LineageTracker
from research_validation.provenance.provenance_api import ProvenanceAPI
from research_validation.provenance.provenance_models import (
    EvidenceNode, EvidenceQualityLevel, LineageStage
)
from research_validation.provenance.provenance_validator import ProvenanceAuditReport, ProvenanceValidator


class ProvenanceEngine:
    """
    Master Facade for Scientific Evidence Provenance and Quality Scoring.
    """

    def __init__(self, storage_dir: Optional[Path] = None):
        self.storage_dir = storage_dir
        self.graph = EvidenceGraph()
        self.store = EvidenceStore(storage_dir=storage_dir)
        self.tracker = LineageTracker(evidence_graph=self.graph)
        self.api = ProvenanceAPI(graph=self.graph, store=self.store)

    def record_empirical_pipeline(
        self,
        chain_name: str,
        raw_samples: List[float],
        transformation_fn: Callable[[List[float]], List[float]],
        aggregation_fn: Callable[[List[float]], float],
        metric_name: str,
        report_title: str,
        quality_level: EvidenceQualityLevel = EvidenceQualityLevel.LEVEL_B,
        signer_key: Optional[str] = None
    ) -> CompleteLineageChain:
        """
        Record a full 7-stage verifiable lineage pipeline and store each node immutably.
        """
        signer = ProvenanceSigner(
            key_id="KEY-PROV-MASTER",
            secret_or_private_key=signer_key or "rvisf_internal_verification_key_sec256"
        )
        chain = self.tracker.create_canonical_lineage_chain(
            chain_name=chain_name,
            raw_data=raw_samples,
            transformation_fn=transformation_fn,
            aggregation_fn=aggregation_fn,
            metric_name=metric_name,
            report_title=report_title,
            quality_level=quality_level,
            signer=signer
        )

        # Append all nodes to the immutable evidence store
        for node in [
            chain.raw_observation_node,
            chain.transformation_node,
            chain.intermediate_artifact_node,
            chain.aggregation_node,
            chain.final_metric_node,
            chain.scientific_report_node,
            chain.digital_signature_node
        ]:
            self.store.store_evidence_node(node)

        return chain

    def compute_quality_weighted_readiness(self) -> Dict[str, Any]:
        """
        Calculates quality-weighted readiness score where higher evidence tiers
        (Level A = 1.0, Level B = 0.85, Level C = 0.70, Level D = 0.40, Level E = 0.0)
        determine empirical credibility.
        """
        nodes = list(self.graph.merkle_dag.nodes.values())
        if not nodes:
            return {
                "total_evidence_nodes": 0,
                "weighted_readiness_score": 0.0,
                "overall_quality_grade": EvidenceQualityLevel.LEVEL_E.value,
                "quality_distribution": {},
                "is_ready_for_external_review": False
            }

        counts: Dict[str, int] = {}
        total_weight = 0.0
        for n in nodes:
            lvl = n.quality_level
            counts[lvl.value] = counts.get(lvl.value, 0) + 1
            total_weight += lvl.numeric_weight

        mean_weight = total_weight / len(nodes)
        grade = (
            EvidenceQualityLevel.LEVEL_A if mean_weight >= 0.95
            else EvidenceQualityLevel.LEVEL_B if mean_weight >= 0.80
            else EvidenceQualityLevel.LEVEL_C if mean_weight >= 0.65
            else EvidenceQualityLevel.LEVEL_D if mean_weight >= 0.35
            else EvidenceQualityLevel.LEVEL_E
        )

        # Audit integrity
        audit = self.api.audit_graph_integrity()

        return {
            "total_evidence_nodes": len(nodes),
            "weighted_readiness_score": mean_weight,
            "overall_quality_grade": grade.value,
            "quality_distribution": counts,
            "merkle_dag_integrity": audit.is_valid,
            "is_ready_for_external_review": audit.is_valid and mean_weight >= 0.65
        }
