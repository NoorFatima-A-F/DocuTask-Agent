"""Network Flow Logs and Security Event Emission."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Dict, List, Optional
import logging
import threading
import uuid

logger = logging.getLogger("app.infrastructure.networking.telemetry.flow_logs")


class NetworkSecurityEventType(str, Enum):
    """Network security event categories."""
    CERTIFICATE_ISSUED = "CertificateIssued"
    CERTIFICATE_ROTATED = "CertificateRotated"
    CERTIFICATE_EXPIRED = "CertificateExpired"
    UNAUTHORIZED_REQUEST = "UnauthorizedRequest"
    POLICY_DENIED = "PolicyDenied"
    MTLS_FAILURE = "mTLSFailure"
    SERVICE_REGISTERED = "ServiceRegistered"
    SERVICE_REMOVED = "ServiceRemoved"
    ROUTING_CHANGED = "RoutingChanged"
    TRAFFIC_SHIFTED = "TrafficShifted"
    NETWORK_POLICY_UPDATED = "NetworkPolicyUpdated"


@dataclass
class NetworkFlowRecord:
    """Standardized VPC/Mesh flow log entry."""
    flow_id: str
    source_address: str
    destination_address: str
    source_spiffe: Optional[str]
    destination_spiffe: Optional[str]
    protocol: str
    action: str  # ALLOW, DENY
    bytes_transferred: int
    packets_transferred: int
    duration_ms: float
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    tenant_id: Optional[str] = None
    rule_id: Optional[str] = None


@dataclass
class NetworkSecurityEvent:
    """Published network security event."""
    event_id: str
    event_type: NetworkSecurityEventType
    source: str
    details: Dict[str, Any]
    severity: str = "INFO"  # INFO, WARN, ERROR, CRITICAL
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class NetworkFlowLogger:
    """Generates structured flow logs and dispatches security events."""

    def __init__(self, max_buffer: int = 5000) -> None:
        self.max_buffer = max_buffer
        self._flow_logs: List[NetworkFlowRecord] = []
        self._security_events: List[NetworkSecurityEvent] = []
        self._event_listeners: List[Callable[[NetworkSecurityEvent], None]] = []
        self._lock = threading.RLock()

    def record_flow(
        self,
        source_address: str,
        destination_address: str,
        action: str = "ALLOW",
        source_spiffe: Optional[str] = None,
        destination_spiffe: Optional[str] = None,
        protocol: str = "https",
        bytes_transferred: int = 0,
        packets_transferred: int = 1,
        duration_ms: float = 1.0,
        tenant_id: Optional[str] = None,
        rule_id: Optional[str] = None,
    ) -> NetworkFlowRecord:
        """Create and buffer a flow log entry."""
        record = NetworkFlowRecord(
            flow_id=uuid.uuid4().hex,
            source_address=source_address,
            destination_address=destination_address,
            source_spiffe=source_spiffe,
            destination_spiffe=destination_spiffe,
            protocol=protocol,
            action=action,
            bytes_transferred=bytes_transferred,
            packets_transferred=packets_transferred,
            duration_ms=duration_ms,
            tenant_id=tenant_id,
            rule_id=rule_id,
        )
        with self._lock:
            self._flow_logs.append(record)
            if len(self._flow_logs) > self.max_buffer:
                self._flow_logs.pop(0)

        return record

    def emit_security_event(
        self,
        event_type: NetworkSecurityEventType,
        source: str,
        details: Dict[str, Any],
        severity: str = "INFO",
    ) -> NetworkSecurityEvent:
        """Emit a network security audit event."""
        event = NetworkSecurityEvent(
            event_id=uuid.uuid4().hex,
            event_type=event_type,
            source=source,
            details=details,
            severity=severity,
        )
        with self._lock:
            self._security_events.append(event)
            if len(self._security_events) > self.max_buffer:
                self._security_events.pop(0)
            listeners = list(self._event_listeners)

        for listener in listeners:
            try:
                listener(event)
            except Exception as e:
                logger.error("Error executing network security event listener: %s", e)

        return event

    def add_event_listener(self, listener: Callable[[NetworkSecurityEvent], None]) -> None:
        """Register subscriber for network security events."""
        with self._lock:
            self._event_listeners.append(listener)

    def get_recent_flows(self, limit: int = 100) -> List[NetworkFlowRecord]:
        """Retrieve recent flow logs."""
        with self._lock:
            return self._flow_logs[-limit:]

    def get_recent_events(self, limit: int = 100) -> List[NetworkSecurityEvent]:
        """Retrieve recent security events."""
        with self._lock:
            return self._security_events[-limit:]
