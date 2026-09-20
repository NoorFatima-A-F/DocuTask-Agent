"""
Evidence Provenance & Scientific Lineage Framework
Module: lineage_tracker.py

Tracks continuous pipeline transformations across 7 canonical stages:
1. RAW_OBSERVATION (Hardware counters, raw latencies, raw model responses)
2. TRANSFORMATION (Normalization, tokenization, filtering)
3. INTERMEDIATE_ARTIFACT (Cleaned tokens, bounding boxes, intermediate embeddings)
4. AGGREGATION (Mean, P99, standard deviation, F1, ULP)
5. FINAL_METRIC (Key claim metrics, e.g. Macro F1 = 0.96)
6. SCIENTIFIC_REPORT (Markdown report, readiness evaluation table)
7. DIGITAL_SIGNATURE (Cryptographic detached signature envelope)
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple

from research_validation.provenance.digital_signatures import DetachedSignature, ProvenanceSigner
from research_validation.provenance.evidence_graph import EvidenceGraph, LineageAncestryTrace
from research_validation.provenance.provenance_models import (
    EvidenceNode, EvidenceQualityLevel, LineageStage
)


@dataclass
class CompleteLineageChain:
    """A fully materialized, 7-stage verifiable lineage pipeline."""
    chain_id: str
    raw_observation_node: EvidenceNode
    transformation_node: EvidenceNode
    intermediate_artifact_node: EvidenceNode
    aggregation_node: EvidenceNode
    final_metric_node: EvidenceNode
    scientific_report_node: EvidenceNode
    digital_signature_node: EvidenceNode
    detached_signature: DetachedSignature
    ancestry_trace: LineageAncestryTrace
    is_replayable: bool
    quality_level: EvidenceQualityLevel
    quality_score: float


class LineageTracker:
    """
    Constructs unbroken, replayable lineage chains for scientific metrics.
    """

    def __init__(self, evidence_graph: Optional[EvidenceGraph] = None):
        self.graph = evidence_graph or EvidenceGraph()

    def create_canonical_lineage_chain(
        self,
        chain_name: str,
        raw_data: List[float],
        transformation_fn: Callable[[List[float]], List[float]],
        aggregation_fn: Callable[[List[float]], float],
        metric_name: str,
        report_title: str,
        quality_level: EvidenceQualityLevel = EvidenceQualityLevel.LEVEL_B,
        signer: Optional[ProvenanceSigner] = None
    ) -> CompleteLineageChain:
        """
        Record and link all 7 stages from raw data to digital signature.
        """
        cid = f"chain_{uuid.uuid4().hex[:8]}"

        # 1. Raw Observation
        raw_id = f"raw_{cid}"
        raw_node = self.graph.record_node(
            node_id=raw_id,
            stage=LineageStage.RAW_OBSERVATION,
            name=f"Raw Data: {chain_name}",
            description=f"Direct empirical observations ({len(raw_data)} samples)",
            payload={"raw_samples": raw_data, "sample_count": len(raw_data)},
            parent_node_ids=[],
            quality_level=quality_level
        )

        # 2. Transformation
        trans_id = f"trans_{cid}"
        transformed_data = transformation_fn(raw_data)
        trans_node = self.graph.record_node(
            node_id=trans_id,
            stage=LineageStage.TRANSFORMATION,
            name=f"Transform: {chain_name}",
            description="Normalized & sanitized data transform",
            payload={"input_count": len(raw_data), "output_count": len(transformed_data)},
            parent_node_ids=[raw_id],
            quality_level=quality_level
        )

        # 3. Intermediate Artifact
        inter_id = f"inter_{cid}"
        inter_node = self.graph.record_node(
            node_id=inter_id,
            stage=LineageStage.INTERMEDIATE_ARTIFACT,
            name=f"Intermediate Matrix: {chain_name}",
            description="Intermediate feature matrix array",
            payload={"features": transformed_data[:10]},
            parent_node_ids=[trans_id],
            quality_level=quality_level
        )

        # 4. Aggregation
        agg_id = f"agg_{cid}"
        aggregated_val = aggregation_fn(transformed_data)
        agg_node = self.graph.record_node(
            node_id=agg_id,
            stage=LineageStage.AGGREGATION,
            name=f"Aggregation: {chain_name}",
            description="Statistical reduction & moment calculation",
            payload={"aggregated_value": aggregated_val},
            parent_node_ids=[inter_id],
            quality_level=quality_level
        )

        # 5. Final Metric
        metric_id = f"metric_{cid}"
        metric_node = self.graph.record_node(
            node_id=metric_id,
            stage=LineageStage.FINAL_METRIC,
            name=metric_name,
            description=f"Published scientific metric value: {aggregated_val:.4f}",
            payload={"metric_name": metric_name, "value": aggregated_val},
            parent_node_ids=[agg_id],
            quality_level=quality_level
        )

        # 6. Scientific Report
        report_id = f"report_{cid}"
        report_node = self.graph.record_node(
            node_id=report_id,
            stage=LineageStage.SCIENTIFIC_REPORT,
            name=report_title,
            description="Consolidated peer-review summary report",
            payload={"report_title": report_title, "primary_metric": metric_name, "value": aggregated_val},
            parent_node_ids=[metric_id],
            quality_level=quality_level
        )

        # 7. Digital Signature
        sig_id = f"sig_{cid}"
        active_signer = signer or ProvenanceSigner(
            key_id="KEY-PROV-MASTER",
            secret_or_private_key="rvisf_internal_verification_key_sec256"
        )
        detached_sig = active_signer.sign_digest(
            digest_hex=report_node.node_hash,
            signer_identity="Principal Research Systems Engineer"
        )

        sig_node = self.graph.record_node(
            node_id=sig_id,
            stage=LineageStage.DIGITAL_SIGNATURE,
            name=f"Signature: {report_title}",
            description="Cryptographically sealed detached signature",
            payload={
                "key_id": detached_sig.key_id,
                "signature_b64": detached_sig.signature_base64,
                "signed_digest": detached_sig.payload_digest_sha256,
                "expires_at": detached_sig.expires_at_epoch
            },
            parent_node_ids=[report_id],
            quality_level=quality_level
        )

        # Trace complete ancestry back to raw observation
        trace = self.graph.trace_ancestry(sig_id)

        return CompleteLineageChain(
            chain_id=cid,
            raw_observation_node=raw_node,
            transformation_node=trans_node,
            intermediate_artifact_node=inter_node,
            aggregation_node=agg_node,
            final_metric_node=metric_node,
            scientific_report_node=report_node,
            digital_signature_node=sig_node,
            detached_signature=detached_sig,
            ancestry_trace=trace,
            is_replayable=True,
            quality_level=trace.overall_quality_level,
            quality_score=trace.evidence_quality_score
        )
