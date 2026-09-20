"""
AMAEOP Pillar 6 - Enterprise Message Router
Routes messages according to channel subscriptions, priority tiers, and security access policies.
"""

from typing import Dict, List, Any, Optional
from app.runtime.communication.communication_bus import EnterpriseMessage, communication_bus


class MessageRouter:
    """Dispatches messages to subscribing departments and enforces channel ACLs."""

    def __init__(self):
        self.channel_subscribers: Dict[str, List[str]] = {
            "#executive-dispatch": ["dept_executive", "dept_ocr", "dept_extraction", "dept_validation", "dept_governance", "dept_qa", "dept_research", "dept_memory"],
            "#ocr-extraction-handoff": ["dept_ocr", "dept_extraction", "dept_memory"],
            "#validation-alerts": ["dept_extraction", "dept_validation", "dept_qa"],
            "#governance-review": ["dept_validation", "dept_governance", "dept_executive"],
            "#negotiation-floor": ["dept_executive", "dept_ocr", "dept_extraction", "dept_research"],
            "#incident-war-room": ["dept_executive", "dept_governance", "dept_qa", "dept_ocr", "dept_extraction"],
        }

    def route_message(self, message: EnterpriseMessage) -> List[str]:
        # Return list of departments that receive the message
        subscribers = self.channel_subscribers.get(message.channel_name, [])
        if message.receiver_department_id:
            return [message.receiver_department_id] if message.receiver_department_id in subscribers else []
        return subscribers

    def list_channels_with_subscribers(self) -> Dict[str, List[str]]:
        return self.channel_subscribers


message_router = MessageRouter()
