"""
Message Validation Guards.
Fail-fast validation for envelopes, correlation IDs, and routing rules.
"""

from app.agents.messaging.envelopes import MessageEnvelope
from app.agents.messaging.exceptions import MessageValidationException


class MessageValidator:
    """Fail-fast validator for messaging envelopes and metadata."""

    @staticmethod
    def validate_envelope(envelope: MessageEnvelope) -> None:
        if not envelope.payload:
            raise MessageValidationException("Message payload cannot be None or empty.")
        if not envelope.metadata.correlation.correlation_id:
            raise MessageValidationException("Message correlation_id cannot be empty.")
