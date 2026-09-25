"""
Enterprise Messaging Exception Hierarchy.
Provides domain exceptions for message routing, bus dispatching, serialization, dead-lettering, and handler errors.
"""

from app.agents.exceptions import AgentException


class MessagingException(AgentException):
    """Base exception for all messaging subsystem errors."""
    pass


class MessageRoutingException(MessagingException):
    """Raised when message routing fails or no route is found."""
    pass


class HandlerNotFoundException(MessagingException):
    """Raised when no command or query handler is registered."""
    pass


class DeadLetterException(MessagingException):
    """Raised when message delivery fails repeatedly and is sent to dead letter queue."""
    pass


class MessageValidationException(MessagingException):
    """Raised when a message envelope or payload fails validation."""
    pass


class MessageSerializationException(MessagingException):
    """Raised when message serialization or deserialization fails."""
    pass
