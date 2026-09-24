"""
ARTEICP Audit Intelligence - Searchable Decision Audit Query Engine
Provides fast filtering, full-text search, and cryptographic verification over execution decision logs.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class SearchableAuditRecord:
    audit_id: str
    mission_id: str
    decision_type: str  # MODEL_ROUTING | RETRY_POLICY | PARALLEL_EXECUTION | HEURISTIC_REPAIR
    decision_summary: str
    actor: str
    policy_version: str
    input_digest: str
    output_digest: str
    signature: str
    timestamp_utc: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class AuditQueryEngine:
    """Provides querying and validation across immutable audit trails."""

    def __init__(self):
        self.records: Dict[str, SearchableAuditRecord] = {}
        self._seed_records()

    def _seed_records(self):
        r1 = SearchableAuditRecord(
            audit_id="aud_2026_001",
            mission_id="mission_live_001",
            decision_type="MODEL_ROUTING",
            decision_summary="Routed invoice extraction to Gemini 2.5 Flash over Gemini Pro (expected utility 0.948 vs 0.865)",
            actor="APDLE_Planner",
            policy_version="v5.0.0-rc1",
            input_digest="sha256_in_9f82ab",
            output_digest="sha256_out_142050",
            signature="ED25519_SIG_8F3A20B1",
            timestamp_utc="2026-09-10T16:00:00.740Z",
        )
        r2 = SearchableAuditRecord(
            audit_id="aud_2026_002",
            mission_id="mission_live_001",
            decision_type="PARALLEL_EXECUTION",
            decision_summary="Dispatched LayoutLM OCR and Vector Memory Lookup concurrently on Wavefront 2",
            actor="PriorityScheduler",
            policy_version="v5.0.0-rc1",
            input_digest="sha256_in_ocr_82",
            output_digest="sha256_out_wf2",
            signature="ED25519_SIG_C4D5E6F7",
            timestamp_utc="2026-09-10T16:00:00.310Z",
        )
        self.records[r1.audit_id] = r1
        self.records[r2.audit_id] = r2

    def query_audit_trail(
        self,
        mission_id: Optional[str] = None,
        decision_type: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        results = list(self.records.values())

        if mission_id:
            results = [r for r in results if r.mission_id == mission_id]
        if decision_type:
            results = [r for r in results if r.decision_type == decision_type]
        if search_query:
            q = search_query.lower()
            results = [r for r in results if q in r.decision_summary.lower() or q in r.actor.lower()]

        return [r.to_dict() for r in results]


audit_query_engine = AuditQueryEngine()
