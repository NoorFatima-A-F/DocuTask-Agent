"""Immutable Append-Only Audit Store with Automatic Hash Chaining."""

from typing import Dict, List, Optional
from ..core.events import AuditEvent
from ..integrity.hashing import HashChainCalculator
from ..integrity.signatures import AuditSigner
from .partitions import AuditPartitionManager


class ImmutableAuditStore:
    """Tamper-resistant append-only storage engine for audit events."""

    def __init__(self, signer: Optional[AuditSigner] = None):
        self.signer = signer or AuditSigner()
        self.calculator = HashChainCalculator()
        # Storage: partition_key -> list of events
        self._partitions: Dict[str, List[AuditEvent]] = {}
        # Chain tracking: tenant_id -> last_hash
        self._tenant_last_hash: Dict[str, str] = {}
        # Global lookup by event_id
        self._event_index: Dict[str, AuditEvent] = {}

    def append(self, event: AuditEvent) -> AuditEvent:
        """Appends an event to the immutable store, chaining its cryptographic hash."""
        if event.event_id in self._event_index:
            raise ValueError(f"Immutability violation: Event '{event.event_id}' already exists and cannot be overwritten")

        tenant_id = event.tenant_id
        previous_hash = self._tenant_last_hash.get(tenant_id, HashChainCalculator.GENESIS_HASH)

        event.previous_hash = previous_hash
        event.integrity_hash = self.calculator.compute_event_hash(event, previous_hash=previous_hash)
        event.signature = self.signer.sign_hash(event.integrity_hash)

        # Record in partition
        partition_key = AuditPartitionManager.get_partition_key(
            tenant_id=tenant_id,
            timestamp=event.timestamp,
            category=event.category.value if hasattr(event.category, "value") else str(event.category),
        )
        if partition_key not in self._partitions:
            self._partitions[partition_key] = []
        self._partitions[partition_key].append(event)

        # Update global index and last hash
        self._event_index[event.event_id] = event
        self._tenant_last_hash[tenant_id] = event.integrity_hash

        return event

    def get_event(self, event_id: str) -> Optional[AuditEvent]:
        return self._event_index.get(event_id)

    def get_tenant_events(self, tenant_id: str) -> List[AuditEvent]:
        """Retrieves all events for a tenant in exact sequential append order."""
        tenant_events = [e for e in self._event_index.values() if e.tenant_id == tenant_id]
        return tenant_events
