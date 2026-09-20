"""Webhook Event Dispatcher with Cryptographic Signatures and Delivery Tracking."""

from datetime import datetime, timezone
import hashlib
import hmac
import json
import logging
import secrets
import time
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from .subscriptions import WebhookEndpoint, WebhookSubscriptionManager

logger = logging.getLogger(__name__)


class WebhookDeliveryAttempt(BaseModel):
    """Record of a webhook dispatch attempt."""

    delivery_id: str
    webhook_id: str
    event_type: str
    payload: Dict[str, Any]
    status_code: Optional[int] = None
    success: bool
    error_message: Optional[str] = None
    attempt_number: int = 1
    duration_ms: float = 0.0
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class WebhookDispatcher:
    """Delivers governance events to registered endpoints with HMAC signatures."""

    def __init__(
        self,
        subscription_mgr: Optional[WebhookSubscriptionManager] = None,
        http_poster: Optional[Callable[[str, Dict[str, str], str], int]] = None,
    ) -> None:
        self.subscription_mgr = subscription_mgr or WebhookSubscriptionManager()
        self._http_poster = http_poster or self._default_mock_poster
        self.delivery_history: List[WebhookDeliveryAttempt] = []

    @staticmethod
    def _default_mock_poster(url: str, headers: Dict[str, str], body_str: str) -> int:
        """Simulate HTTP POST for testing environments."""
        return 200

    @staticmethod
    def generate_signature(payload_bytes: bytes, secret_key: str) -> str:
        """Compute HMAC-SHA256 signature for webhook payload."""
        mac = hmac.new(secret_key.encode("utf-8"), payload_bytes, hashlib.sha256)
        return f"sha256={mac.hexdigest()}"

    def dispatch_event(
        self,
        tenant_id: str,
        event_type: str,
        payload: Dict[str, Any],
        max_retries: int = 2,
    ) -> List[WebhookDeliveryAttempt]:
        """Deliver event to all matching webhook subscriptions for tenant."""
        endpoints = self.subscription_mgr.list_by_tenant(tenant_id)
        matching = [
            ep for ep in endpoints
            if ep.is_active and ("*" in ep.events or event_type in ep.events)
        ]

        results: List[WebhookDeliveryAttempt] = []
        payload_data = {
            "id": f"evt_{secrets.token_hex(8)}",
            "event": event_type,
            "tenant_id": tenant_id,
            "data": payload,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        body_bytes = json.dumps(payload_data, sort_keys=True).encode("utf-8")
        body_str = body_bytes.decode("utf-8")

        for ep in matching:
            signature = self.generate_signature(body_bytes, ep.secret_key)
            headers = {
                "Content-Type": "application/json",
                "X-Governance-Signature": signature,
                "X-Governance-Event": event_type,
                "User-Agent": "DocuTask-Governance-Webhooks/1.0",
            }

            attempt_success = False
            last_code = None
            last_err = None
            start_time = time.time()

            for attempt in range(1, max_retries + 2):
                try:
                    status_code = self._http_poster(ep.url, headers, body_str)
                    last_code = status_code
                    if 200 <= status_code < 300:
                        attempt_success = True
                        break
                    else:
                        last_err = f"Non-2xx HTTP status: {status_code}"
                except Exception as ex:
                    last_err = str(ex)

            duration_ms = (time.time() - start_time) * 1000.0
            delivery = WebhookDeliveryAttempt(
                delivery_id=f"del_{secrets.token_hex(8)}",
                webhook_id=ep.webhook_id,
                event_type=event_type,
                payload=payload_data,
                status_code=last_code,
                success=attempt_success,
                error_message=last_err if not attempt_success else None,
                attempt_number=attempt,
                duration_ms=round(duration_ms, 2),
            )
            self.delivery_history.append(delivery)
            results.append(delivery)

        return results
