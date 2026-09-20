"""
Knowledge Compiler for Phase 13.5 (ARLP-KIP).
Compiles rules and strategies into cryptographically sealed knowledge bundles.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import hashlib
import json
import uuid

from app.runtime.learning.learning.lesson_extractor import ExtractedRule
from app.runtime.learning.learning.strategy_builder import ExecutionStrategy


class CompiledKnowledgeBundle(BaseModel):
    bundle_id: str = Field(default_factory=lambda: f"kbundle_{uuid.uuid4().hex[:8]}")
    lesson_id: str
    bundle_hash: str
    rule_count: int
    has_strategy: bool
    payload: Dict[str, Any] = Field(default_factory=dict)


class KnowledgeCompiler:
    """
    Compiles and cryptographically seals knowledge bundles for safe ingestion.
    """

    @classmethod
    def compile_bundle(
        cls,
        lesson_id: str,
        rules: List[ExtractedRule],
        strategy: Optional[ExecutionStrategy] = None,
    ) -> CompiledKnowledgeBundle:
        payload = {
            "rules": [r.model_dump() for r in rules],
            "strategy": strategy.model_dump() if strategy else None,
        }
        serialized = json.dumps(payload, sort_keys=True)
        bundle_hash = hashlib.sha256(serialized.encode("utf-8")).hexdigest()

        return CompiledKnowledgeBundle(
            bundle_id=f"kbundle_{uuid.uuid4().hex[:8]}",
            lesson_id=lesson_id,
            bundle_hash=f"sha256:{bundle_hash}",
            rule_count=len(rules),
            has_strategy=strategy is not None,
            payload=payload,
        )
