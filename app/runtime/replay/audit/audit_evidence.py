"""
Audit Evidence for Phase 13.4.
Extracts and packages evidence items into audit-ready proofs.
"""

from typing import Dict, Any, List


class AuditEvidenceExtractor:
    """
    Extracts verified evidence records from replay event history.
    """

    @classmethod
    def extract_evidence(cls, events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        evidences = []
        for ev in events:
            evt_type = ev.get("event_type", "")
            if "evidence" in evt_type or "truth.invariant" in evt_type:
                evidences.append({
                    "event_id": ev.get("event_id"),
                    "type": evt_type,
                    "payload": ev.get("payload", {}),
                    "timestamp": ev.get("timestamp"),
                })
        return evidences
