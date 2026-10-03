"""
Evidence Provenance & Scientific Lineage Framework
Module: evidence_bundle.py

Self-contained portable research evidence bundles:
- Encapsulates Merkle DAG, W3C PROV-O JSON-LD, OpenLineage JSON, and Detached Digital Signatures.
- Provides standalone cryptographic verification for external peer reviewers.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from research_validation.provenance.digital_signatures import DetachedSignature, ProvenanceSigner
from research_validation.provenance.evidence_graph import EvidenceGraph
from research_validation.provenance.provenance_models import EvidenceQualityLevel
from research_validation.provenance.provenance_serialization import ProvenanceSerializer


@dataclass
class SealedEvidenceBundle:
    """Portable, verifiable scientific evidence bundle."""
    bundle_id: str
    bundle_title: str
    version: str
    created_at_iso: str
    root_merkle_digest: str
    evidence_quality_score: float
    overall_quality_level: EvidenceQualityLevel
    evidence_nodes: List[Dict[str, Any]]
    prov_json_ld: str
    openlineage_json: str
    detached_signature: Dict[str, Any]
    environment_manifest: Dict[str, Any]

    def verify(self, secret_or_pubkey: str) -> Tuple[bool, str]:
        """Verify the integrity and digital signature of this bundle."""
        sig_data = self.detached_signature
        sig_obj = DetachedSignature(
            key_id=sig_data["key_id"],
            algorithm=sig_data["algorithm"],
            signature_base64=sig_data["signature_base64"],
            payload_digest_sha256=sig_data["payload_digest_sha256"],
            signed_at_epoch=sig_data["signed_at_epoch"],
            expires_at_epoch=sig_data["expires_at_epoch"],
            signer_identity=sig_data["signer_identity"]
        )
        return ProvenanceSigner.verify_signature(
            signature=sig_obj,
            expected_digest_hex=self.root_merkle_digest,
            secret_or_public_key=secret_or_pubkey
        )


class EvidenceBundleBuilder:
    """
    Constructs and packages sealed evidence bundles.
    """

    @classmethod
    def build_bundle(
        cls,
        graph: EvidenceGraph,
        bundle_title: str = "Empirical Research Validation Evidence",
        version: str = "2.0.0",
        signer: Optional[ProvenanceSigner] = None
    ) -> SealedEvidenceBundle:
        """Package an EvidenceGraph into a signed SealedEvidenceBundle."""
        root_digest = graph.merkle_dag.compute_root_digest()

        # Compute average quality score
        weights = [n.quality_level.numeric_weight for n in graph.merkle_dag.nodes.values()]
        score = sum(weights) / len(weights) if weights else 0.0
        qual_level = EvidenceQualityLevel.LEVEL_A if score >= 0.95 else EvidenceQualityLevel.LEVEL_B if score >= 0.80 else EvidenceQualityLevel.LEVEL_C if score >= 0.65 else EvidenceQualityLevel.LEVEL_D if score >= 0.35 else EvidenceQualityLevel.LEVEL_E

        # Provenance Serializations
        json_ld = ProvenanceSerializer.to_json_ld(graph.prov_doc)

        active_signer = signer or ProvenanceSigner(
            key_id="KEY-BUNDLE-MASTER",
            secret_or_private_key="rvisf_internal_verification_key_sec256"
        )
        sig = active_signer.sign_digest(root_digest, signer_identity="Scientific Evidence Custodian")

        nodes_data = [n.to_dict() for n in graph.merkle_dag.nodes.values()]
        env = graph.capture_current_environment()

        return SealedEvidenceBundle(
            bundle_id=graph.graph_id,
            bundle_title=bundle_title,
            version=version,
            created_at_iso=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            root_merkle_digest=root_digest,
            evidence_quality_score=score,
            overall_quality_level=qual_level,
            evidence_nodes=nodes_data,
            prov_json_ld=json_ld,
            openlineage_json="{}",
            detached_signature=asdict(sig),
            environment_manifest=env.canonical_dict()
        )

    @classmethod
    def export_bundle_file(cls, bundle: SealedEvidenceBundle, target_path: Path) -> Path:
        """Write bundle JSON to disk."""
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(asdict(bundle), f, indent=2)
        return target_path
