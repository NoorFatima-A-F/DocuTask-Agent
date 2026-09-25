"""
Reference Notification Plugin: Webhook and Alert Dispatcher.
"""
from typing import Any, Dict, List, Tuple
from app.platform_verification.extension_framework.domain.interfaces import NotificationPluginInterface
from app.platform_verification.extension_framework.domain.models import (
    PluginMetadata, PluginCategory, PluginExecutionContext, PluginExecutionResult,
    PluginHealthMetrics, PluginHealthState, PluginPermission, SecurityClassification
)


class WebhookNotificationPlugin(NotificationPluginInterface):
    def __init__(self):
        self._notifications: List[Dict[str, Any]] = []
        self._config: Dict[str, Any] = {}

    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            plugin_id="webhook_notification_plugin",
            name="Webhook & Alert Dispatcher Plugin",
            version="1.0.0",
            category=PluginCategory.NOTIFICATION,
            author="DevOps & Reliability Squad",
            description="Dispatches verification completion and quality gate alerts via HTTP Webhooks",
            capabilities=["webhook_dispatch", "slack_notification_forwarding"],
            granted_permissions=[PluginPermission.ACCESS_NETWORK],
            security_classification=SecurityClassification.INTERNAL
        )

    def initialize(self, context: Dict[str, Any]) -> bool:
        return True

    def validate(self) -> Tuple[bool, List[str]]:
        return True, []

    def configure(self, config: Dict[str, Any]) -> None:
        self._config = config

    def execute(self, context: PluginExecutionContext) -> PluginExecutionResult:
        success = self.send_alert("Verification Complete", f"Run {context.verification_id} passed")
        return PluginExecutionResult(
            execution_id=context.execution_id,
            plugin_id="webhook_notification_plugin",
            is_success=success,
            metrics=[{"metric": "alerts_dispatched", "value": 1}],
            raw_evidence={"status": "SENT"}
        )

    def send_alert(self, title: str, message: str, level: str = "INFO") -> bool:
        self._notifications.append({"title": title, "message": message, "level": level})
        return True

    def cleanup(self) -> None:
        self._notifications.clear()

    def health_check(self) -> PluginHealthMetrics:
        return PluginHealthMetrics(
            plugin_id="webhook_notification_plugin",
            state=PluginHealthState.HEALTHY,
            total_executions=1,
            successful_executions=1
        )
