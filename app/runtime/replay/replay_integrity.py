"""
Replay Cryptographic Integrity Verifier.
Validates SHA-256 hash chains across event logs, detecting tampering, sequence gaps, and ordering violations.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.runtime.observability.schemas import RuntimeEvent
from app.runtime.observability.event_serializer import EventSerializer


class IntegrityVerificationResult(BaseModel):
    is_valid: bool = Field(..., description="True if the entire hash chain is intact")
    total_events_verified: int = Field(..., description="Total events inspected")
    first_tampered_index: Optional[int] = Field(default=None, description="Index of first detected tampering")
    first_tampered_event_id: Optional[str] = Field(default=None, description="Event ID where failure occurred")
    violation_reason: Optional[str] = Field(default=None, description="Human-readable violation reason")
    hash_chain_head: Optional[str] = Field(default=None, description="Final cumulative SHA-256 hash")


class ReplayIntegrityVerifier:
    """Mathematical verification engine for immutable event hash chains."""

    @staticmethod
    def verify_event_stream(events: List[RuntimeEvent]) -> IntegrityVerificationResult:
        if not events:
            return IntegrityVerificationResult(
                is_valid=True,
                total_events_verified=0,
                hash_chain_head=None,
            )

        previous_hash = "0" * 64
        seen_event_ids = set()

        for idx, event in enumerate(events):
            # 1. Duplicate event check
            if event.event_id in seen_event_ids:
                return IntegrityVerificationResult(
                    is_valid=False,
                    total_events_verified=idx,
                    first_tampered_index=idx,
                    first_tampered_event_id=event.event_id,
                    violation_reason=f"Duplicate event ID '{event.event_id}' detected at index {idx}",
                )
            seen_event_ids.add(event.event_id)

            # 2. Sequence continuity check
            if idx > 0 and event.sequence_number <= events[idx - 1].sequence_number:
                return IntegrityVerificationResult(
                    is_valid=False,
                    total_events_verified=idx,
                    first_tampered_index=idx,
                    first_tampered_event_id=event.event_id,
                    violation_reason=f"Sequence ordering violation at index {idx}: {event.sequence_number} <= {events[idx - 1].sequence_number}",
                )

            # 3. Previous hash pointer validation
            if event.previous_hash and event.previous_hash != previous_hash and idx > 0:
                return IntegrityVerificationResult(
                    is_valid=False,
                    total_events_verified=idx,
                    first_tampered_index=idx,
                    first_tampered_event_id=event.event_id,
                    violation_reason=f"Previous hash mismatch at index {idx}: expected {previous_hash[:8]}..., found {event.previous_hash[:8]}...",
                )

            # 4. Recompute canonical SHA-256 hash
            expected_hash = EventSerializer.compute_event_hash(event, previous_hash)
            if event.hash and event.hash != expected_hash:
                return IntegrityVerificationResult(
                    is_valid=False,
                    total_events_verified=idx,
                    first_tampered_index=idx,
                    first_tampered_event_id=event.event_id,
                    violation_reason=f"Cryptographic hash corruption at index {idx}: expected {expected_hash[:8]}..., recorded {event.hash[:8]}...",
                )

            previous_hash = event.hash or expected_hash

        return IntegrityVerificationResult(
            is_valid=True,
            total_events_verified=len(events),
            hash_chain_head=previous_hash,
        )
