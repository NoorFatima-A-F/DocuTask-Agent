"""
Audit Log Builder.
Synthesizes hash-chained AuditRecord logs from raw immutable EventStore records.
"""

from typing import List
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.audit.audit_record import AuditRecord
from app.runtime.audit.audit_signature import AuditSignatureEngine


class AuditLogBuilder:
    @staticmethod
    def build_audit_records_from_events(mission_id: str, events: List[RuntimeEvent]) -> List[AuditRecord]:
        records: List[AuditRecord] = []
        previous_hash = "0" * 64

        for idx, event in enumerate(events):
            raw_dict = {
                "audit_id": f"audit_{mission_id}_{idx}",
                "mission_id": mission_id,
                "trace_id": event.trace_context.trace_id if event.trace_context else None,
                "actor": "HUMAN_OPERATOR" if "human" in str(event.category).lower() else "SYSTEM",
                "component": str(event.category.value if hasattr(event.category, "value") else event.category).upper(),
                "action": str(event.event_type.value if hasattr(event.event_type, "value") else event.event_type),
                "reason": event.payload.get("rationale", event.payload.get("reason", f"Execution in stage '{event.stage}'")),
                "evidence_ids": [event.event_id],
                "input_payload": event.payload.get("inputs", {}),
                "output_payload": event.payload.get("outputs", {}),
                "parent_event_id": event.parent_event_id,
                "planner_generation": int(event.payload.get("generation", 1)),
                "worker_id": event.worker_id,
                "system_version": "v2.1-ESMR",
                "timestamp": str(event.timestamp),
                "previous_sha256": previous_hash,
            }

            rec_hash = AuditSignatureEngine.compute_sha256(raw_dict, previous_hash)
            sig = AuditSignatureEngine.sign_record(raw_dict, rec_hash)

            raw_dict["sha256"] = rec_hash
            raw_dict["signature"] = sig

            record = AuditRecord.model_validate(raw_dict)
            records.append(record)
            previous_hash = rec_hash

        return records
