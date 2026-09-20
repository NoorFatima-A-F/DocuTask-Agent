"""
Enterprise Integration Fabric - Webhook Platform package.
"""

from app.connectors.webhooks.engine import WebhookConfig, WebhookEngine

__all__ = [
    "WebhookEngine",
    "WebhookConfig",
]
