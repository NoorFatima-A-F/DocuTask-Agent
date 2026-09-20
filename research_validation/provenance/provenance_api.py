"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_api.py

Clean programmatic interface for external reviewers, audit scripts, and automated evaluation tools.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.evidence_bundle import EvidenceBundleBuilder, SealedEvidenceBundle
from research_validation.provenance.evidence_diff import EvidenceBundleDiffReport, EvidenceDiffer
from research_validation.provenance.evidence_graph import EvidenceGraph, LineageAncestryTrace
from research_validation.provenance.evidence_store import EvidenceStore
from research_validation.provenance.provenance_models import EvidenceNode, EvidenceQualityLevel
from research_validation.provenance.provenance_serialization import ProvenanceSerializer
from research_validation.provenance.provenance_validator import ProvenanceAuditReport, ProvenanceValidator
from research_validation.provenance.provenance_visualizer import ProvenanceVisualizer


class ProvenanceAPI:
    """
    Public query and verification API for scientific evidence graphs and bundles.
    """

    def __init__(self, graph: Optional[EvidenceGraph] = None, store: Optional[EvidenceStore] = None):
        self.graph = graph or EvidenceGraph()
        self.store = store or EvidenceStore()

    def get_metric_ancestry(self, metric_node_id: str) -> LineageAncestryTrace:
        """Trace unbroken ancestry chain from metric back to root observations."""
        return self.graph.trace_ancestry(metric_node_id)

    def audit_graph_integrity(self, secret_key: Optional[str] = None) -> ProvenanceAuditReport:
        """Run full zero-trust audit across evidence graph."""
        return ProvenanceValidator.audit_graph(self.graph, expected_secret_or_pubkey=secret_key)

    def export_sealed_bundle(self, title: str = "Research Lineage Bundle") -> SealedEvidenceBundle:
        """Build and seal a portable evidence bundle."""
        return EvidenceBundleBuilder.build_bundle(self.graph, bundle_title=title)

    def export_json_ld(self) -> str:
        """Export W3C PROV graph as JSON-LD."""
        return ProvenanceSerializer.to_json_ld(self.graph.prov_doc)

    def export_prov_n(self) -> str:
        """Export W3C PROV graph in PROV-N notation."""
        return ProvenanceSerializer.to_prov_n(self.graph.prov_doc)

    def export_prov_xml(self) -> str:
        """Export W3C PROV graph in PROV-XML."""
        return ProvenanceSerializer.to_prov_xml(self.graph.prov_doc)

    def export_svg(self) -> str:
        """Render standalone SVG diagram of lineage."""
        return ProvenanceVisualizer.to_svg(self.graph)

    def export_interactive_html(self) -> str:
        """Render interactive HTML explorer."""
        return ProvenanceVisualizer.to_interactive_html(self.graph)

    def compare_evidence_nodes(self, baseline_id: str, comparison_id: str) -> EvidenceBundleDiffReport:
        """Diff two evidence nodes in the store or graph."""
        n1 = self.graph.merkle_dag.get_node(baseline_id)
        n2 = self.graph.merkle_dag.get_node(comparison_id)
        if not n1 or not n2:
            raise KeyError(f"Both nodes must exist for diff: '{baseline_id}', '{comparison_id}'")
        return EvidenceDiffer.compare_nodes(n1, n2)
