"""mTLS 1.3 Transport Security & Session Management."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Optional

from ..identity.certificates import CertificateManager


class MTLSMode(str, Enum):
    STRICT = "STRICT"
    PERMISSIVE = "PERMISSIVE"
    DISABLED = "DISABLED"


class TLSVersion(str, Enum):
    TLS_1_2 = "TLS_1_2"
    TLS_1_3 = "TLS_1_3"


CIPHER_SUITES_TLS_1_3 = [
    "TLS_AES_256_GCM_SHA384",
    "TLS_CHACHA20_POLY1305_SHA256",
    "TLS_AES_128_GCM_SHA256",
]


@dataclass
class MTLSSession:
    session_id: str
    client_cert_serial: str
    server_cert_serial: str
    client_spiffe_uri: str
    server_spiffe_uri: str
    tls_version: TLSVersion = TLSVersion.TLS_1_3
    cipher_suite: str = "TLS_AES_256_GCM_SHA384"
    established_at: float = field(default_factory=time.time)
    active: bool = True


@dataclass
class MTLSHandshakeResult:
    success: bool
    session: Optional[MTLSSession] = None
    error_reason: Optional[str] = None


class MTLSManager:
    """Orchestrates mTLS 1.3 handshakes, cipher negotiation, and session tracking."""

    def __init__(
        self,
        cert_manager: Optional[CertificateManager] = None,
        default_mode: MTLSMode = MTLSMode.STRICT,
    ):
        self.cert_manager = cert_manager or CertificateManager()
        self.default_mode = default_mode
        self._sessions: Dict[str, MTLSSession] = {}

    def perform_handshake(
        self,
        client_cert_serial: str,
        server_cert_serial: str,
        mode: Optional[MTLSMode] = None,
        requested_tls: TLSVersion = TLSVersion.TLS_1_3,
    ) -> MTLSHandshakeResult:
        """Perform mutual TLS handshake validation between client and server certificates."""
        effective_mode = mode or self.default_mode
        if effective_mode == MTLSMode.DISABLED:
            session = MTLSSession(
                session_id=f"session-plain-{uuid.uuid4().hex[:8]}",
                client_cert_serial="",
                server_cert_serial="",
                client_spiffe_uri="",
                server_spiffe_uri="",
                tls_version=TLSVersion.TLS_1_2,
                cipher_suite="PLAINTEXT",
            )
            return MTLSHandshakeResult(success=True, session=session)

        # Validate server certificate
        server_cert = self.cert_manager.get_certificate(server_cert_serial)
        if not server_cert or not server_cert.is_active:
            return MTLSHandshakeResult(success=False, error_reason="Invalid or expired server certificate")

        # Validate client certificate
        client_cert = self.cert_manager.get_certificate(client_cert_serial)
        if not client_cert or not client_cert.is_active:
            if effective_mode == MTLSMode.PERMISSIVE:
                # Permissive allows unauthenticated client
                session = MTLSSession(
                    session_id=f"session-perm-{uuid.uuid4().hex[:8]}",
                    client_cert_serial="",
                    server_cert_serial=server_cert_serial,
                    client_spiffe_uri="",
                    server_spiffe_uri=server_cert.san_uris[0] if server_cert.san_uris else "",
                )
                return MTLSHandshakeResult(success=True, session=session)
            return MTLSHandshakeResult(success=False, error_reason="Client certificate verification failed under STRICT mTLS")

        # Establish verified session
        session_id = f"session-mtls-{uuid.uuid4().hex[:10]}"
        session = MTLSSession(
            session_id=session_id,
            client_cert_serial=client_cert_serial,
            server_cert_serial=server_cert_serial,
            client_spiffe_uri=client_cert.san_uris[0] if client_cert.san_uris else "",
            server_spiffe_uri=server_cert.san_uris[0] if server_cert.san_uris else "",
            tls_version=requested_tls,
            cipher_suite="TLS_AES_256_GCM_SHA384",
        )
        self._sessions[session_id] = session
        return MTLSHandshakeResult(success=True, session=session)

    def invalidate_session(self, session_id: str) -> bool:
        session = self._sessions.get(session_id)
        if session:
            session.active = False
            return True
        return False

    def get_session(self, session_id: str) -> Optional[MTLSSession]:
        session = self._sessions.get(session_id)
        if session and session.active:
            return session
        return None
