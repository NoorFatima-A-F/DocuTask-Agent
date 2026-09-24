"""
ARTEICP Feedback Pipeline - Versioned Knowledge Manager
Maintains versioned semantic rules and memory trees with commit hashes and rollback capabilities.
"""

from typing import Dict, List, Any
from dataclasses import dataclass, asdict, field
import hashlib
import time


@dataclass
class VersionedKnowledgeRule:
    rule_id: str
    version: str
    rule_statement: str
    origin_feedback_id: str
    provenance_hash: str
    is_active: bool = True
    committed_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class KnowledgeVersioner:
    """Stores versioned semantic knowledge derived from validated human feedback loops."""

    def __init__(self):
        self.rules: Dict[str, VersionedKnowledgeRule] = {}
        self._seed_rules()

    def _seed_rules(self):
        r1 = VersionedKnowledgeRule(
            rule_id="rule_eu_vat_01",
            version="v1.2.0",
            rule_statement="When document locale is EU, anchor total_tax_amount to line-item sum.",
            origin_feedback_id="fb_inv_001",
            provenance_hash="e4b2a198c7d3410f",
        )
        self.rules[r1.rule_id] = r1

    def commit_rule(
        self,
        rule_statement: str,
        origin_feedback_id: str,
        version: str = "v1.3.0",
    ) -> VersionedKnowledgeRule:
        h = hashlib.sha256(f"{rule_statement}{time.time()}".encode("utf-8")).hexdigest()[:16]
        rule_id = f"rule_{h[:8]}"
        rule = VersionedKnowledgeRule(
            rule_id=rule_id,
            version=version,
            rule_statement=rule_statement,
            origin_feedback_id=origin_feedback_id,
            provenance_hash=h,
        )
        self.rules[rule_id] = rule
        return rule

    def list_rules(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.rules.values()]


knowledge_versioner = KnowledgeVersioner()
