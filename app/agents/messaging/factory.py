"""
Messaging Injectable Factory.
Instantiates and wires UnifiedMessageBus, DeadLetterQueue, and MessagingMetricsCollector.
"""

from app.agents.messaging.bus import UnifiedMessageBus
from app.agents.messaging.dead_letter import DeadLetterQueue
from app.agents.messaging.metrics import MessagingMetricsCollector


class MessagingFactory:
    """Factory wiring messaging foundation components."""

    @staticmethod
    def create_messaging_subsystem():
        bus = UnifiedMessageBus()
        dlq = DeadLetterQueue()
        metrics = MessagingMetricsCollector()
        return bus, dlq, metrics
