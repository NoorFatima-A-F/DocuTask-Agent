"""Evidence Builder Factory.

Provides a fluent, verifiable builder API to construct and seal EvidenceNodes
from any runtime execution event in the DocuTask platform.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from app.runtime.evidence.execution_evidence import (
    CryptoProof,
    EvidenceNode,
    EvidenceStatus,
    EvidenceType,
)


class EvidenceBuilder:
    def __init__(self, evidence_type: EvidenceType, evidence_id: Optional[str] = None):
        self.evidence_id = evidence_id or f"ev-{uuid.uuid4().hex[:12]}"
        self.evidence_type = evidence_type
        self.parent_hashes: List[str] = []
        self.timestamp: float = time.time()
        self.source_agent: str = "docutask-agent-runtime"
        self.execution_context: Dict[str, Any] = {}
        self.inputs: Dict[str, Any] = {}
        self.outputs: Dict[str, Any] = {}
        self.metrics: Dict[str, float] = {}

    def with_parent(self, parent_hash: str) -> EvidenceBuilder:
        if parent_hash and parent_hash not in self.parent_hashes:
            self.parent_hashes.append(parent_hash)
        return self

    def with_parents(self, parent_hashes: List[str]) -> EvidenceBuilder:
        for p in parent_hashes:
            self.with_parent(p)
        return self

    def with_source(self, source_agent: str) -> EvidenceBuilder:
        self.source_agent = source_agent
        return self

    def with_context(self, context: Dict[str, Any]) -> EvidenceBuilder:
        self.execution_context.update(context)
        return self

    def with_inputs(self, inputs: Dict[str, Any]) -> EvidenceBuilder:
        self.inputs.update(inputs)
        return self

    def with_outputs(self, outputs: Dict[str, Any]) -> EvidenceBuilder:
        self.outputs.update(outputs)
        return self

    def with_metrics(self, metrics: Dict[str, float]) -> EvidenceBuilder:
        self.metrics.update(metrics)
        return self

    def with_timestamp(self, timestamp: float) -> EvidenceBuilder:
        self.timestamp = timestamp
        return self

    def build_and_seal(self, private_seed: str = "docutask-aeeerp-root-key-2026") -> EvidenceNode:
        node = EvidenceNode(
            evidence_id=self.evidence_id,
            evidence_type=self.evidence_type,
            parent_hashes=list(self.parent_hashes),
            timestamp=self.timestamp,
            source_agent=self.source_agent,
            execution_context=self.execution_context,
            inputs=self.inputs,
            outputs=self.outputs,
            metrics=self.metrics,
        )
        return node.seal(private_seed=private_seed)
