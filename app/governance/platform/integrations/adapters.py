"""Payload Normalization Adapters for Enterprise Integrations."""

from typing import Any, Dict


class IntegrationAdapter:
    """Transforms external payloads into canonical governance platform formats."""

    @staticmethod
    def to_siem_event(governance_event: Dict[str, Any]) -> Dict[str, Any]:
        """Convert a governance event into Common Event Format (CEF) / ECS JSON."""
        return {
            "source": "DocuTask-Governance-Platform",
            "event_type": governance_event.get("event_type", "SECURITY_ALERT"),
            "severity": governance_event.get("severity", "MEDIUM"),
            "tenant_id": governance_event.get("tenant_id", "default"),
            "details": governance_event.get("payload", {}),
            "timestamp": governance_event.get("timestamp"),
        }

    @staticmethod
    def to_slack_message(event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Format governance event for Slack webhook delivery."""
        decision = payload.get("decision", "UNKNOWN")
        risk = payload.get("risk_level", "LOW")
        return {
            "text": f":shield: *AI Governance Alert: {event_type}*",
            "attachments": [
                {
                    "color": "#D32F2F" if risk in ["HIGH", "CRITICAL"] else "#388E3C",
                    "fields": [
                        {"title": "Action", "value": payload.get("action", "N/A"), "short": True},
                        {"title": "Decision", "value": decision, "short": True},
                        {"title": "Risk Level", "value": risk, "short": True},
                        {"title": "Reason", "value": payload.get("reason", "None provided"), "short": False},
                    ],
                }
            ],
        }
