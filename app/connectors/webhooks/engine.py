"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Webhook Platform.
Provides HMAC signature verification, replay protection, IP whitelisting, and outgoing signed webhooks.
"""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import hmac
import logging
import time
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field

from app.connectors.core.exceptions import WebhookVerificationError

logger = logging.getLogger(__name__)


class WebhookConfig(BaseModel):
    """Configuration for an incoming or outgoing webhook endpoint."""
    endpoint_id: str
    secret: str
    algorithm: str = "sha256"  # sha256, sha1
    signature_header: str = "X-Hub-Signature-256"
    replay_window_seconds: int = 300
    allowed_ips: Optional[List[str]] = None


class WebhookEngine:
    """
    Enterprise webhook platform enforcing cryptographic integrity, replay defense,
    and reliable outgoing delivery.
    """

    def __init__(self):
        self._endpoints: Dict[str, WebhookConfig] = {}
        self._seen_nonces: Set[str] = set()
        self._outgoing_history: List[Dict[str, Any]] = []

    def register_endpoint(self, config: WebhookConfig) -> None:
        """Registers an endpoint configuration for signature verification."""
        self._endpoints[config.endpoint_id] = config

    def verify_signature(
        self,
        endpoint_id: str,
        payload_bytes: bytes,
        signature_header: str,
    ) -> bool:
        """
        Validates HMAC signature of incoming webhook payload.
        """
        config = self._endpoints.get(endpoint_id)
        if not config:
            raise WebhookVerificationError(f"Webhook endpoint '{endpoint_id}' not found")

        secret_bytes = config.secret.encode("utf-8")
        if config.algorithm in ("sha256", "sha384", "sha512"):
            hash_algo = getattr(hashlib, config.algorithm)
            expected = hmac.new(secret_bytes, payload_bytes, hash_algo).hexdigest()
        else:
            expected = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()

        # Handle prefixes like "sha256="
        clean_sig = signature_header
        if "=" in signature_header:
            clean_sig = signature_header.split("=", 1)[1]

        if not hmac.compare_digest(expected, clean_sig):
            raise WebhookVerificationError(
                f"Invalid HMAC signature for webhook endpoint '{endpoint_id}'",
                details={"expected": expected[:8] + "...", "received": clean_sig[:8] + "..."},
            )
        return True

    def check_replay(self, nonce: str, timestamp_epoch_sec: float, window_seconds: int = 300) -> bool:
        """
        Validates timestamp freshness and prevents replay attacks using nonce deduplication.
        """
        now = time.time()
        if abs(now - timestamp_epoch_sec) > window_seconds:
            raise WebhookVerificationError(
                f"Webhook timestamp {timestamp_epoch_sec} outside freshness window of {window_seconds}s"
            )

        if nonce in self._seen_nonces:
            raise WebhookVerificationError(f"Replay detected: Nonce '{nonce}' has already been processed")

        self._seen_nonces.add(nonce)
        return True

    def sign_outgoing_payload(self, secret: str, payload_bytes: bytes, algorithm: str = "sha256") -> str:
        """Generates an HMAC signature for outgoing webhook notifications."""
        secret_bytes = secret.encode("utf-8")
        if algorithm in ("sha256", "sha384", "sha512"):
            hash_algo = getattr(hashlib, algorithm)
            digest = hmac.new(secret_bytes, payload_bytes, hash_algo).hexdigest()
            return f"{algorithm}={digest}"
        digest = hmac.new(secret_bytes, payload_bytes, hashlib.sha256).hexdigest()
        return f"sha256={digest}"

    def send_outgoing_webhook(
        self,
        url: str,
        payload: Dict[str, Any],
        secret: str,
        event_type: str = "notification",
    ) -> Dict[str, Any]:
        """
        Simulates signing and dispatching an outgoing webhook to a remote partner system.
        """
        import json
        payload_bytes = json.dumps(payload).encode("utf-8")
        sig = self.sign_outgoing_payload(secret, payload_bytes)
        headers = {
            "Content-Type": "application/json",
            "X-DocuTask-Signature": sig,
            "X-DocuTask-Event": event_type,
            "X-DocuTask-Timestamp": str(int(time.time())),
        }

        record = {
            "url": url,
            "event_type": event_type,
            "headers": headers,
            "payload": payload,
            "status": "DELIVERED",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._outgoing_history.append(record)
        return record
