"""
Unified Message Bus Implementation.
Implements EventBus, CommandBus, QueryBus, and UnifiedMessageBus.
"""

from typing import Callable, Coroutine, Dict, List, Optional
from app.agents.messaging.commands import AgentCommand, CommandResult
from app.agents.messaging.dead_letter import DeadLetterQueue
from app.agents.messaging.events import DomainEvent
from app.agents.messaging.exceptions import HandlerNotFoundException
from app.agents.messaging.interfaces import ICommandBus, IEventBus, IQueryBus
from app.agents.messaging.queries import AgentQuery, QueryResult
from app.agents.messaging.registry import HandlerRegistry


class EventBus(IEventBus):
    """Event Bus handling domain event publishing and subscriptions."""

    def __init__(self, registry: Optional[HandlerRegistry] = None):
        self.registry = registry or HandlerRegistry()
        self._history: List[DomainEvent] = []

    async def publish(self, event: DomainEvent) -> None:
        self._history.append(event)
        subscribers = await self.registry.get_event_subscribers(event.event_type)
        for handler in subscribers:
            await handler(event)

    async def subscribe(self, event_type: str, handler: Callable[[DomainEvent], Coroutine]) -> None:
        await self.registry.subscribe_event(event_type, handler)

    def replay_events(self) -> List[DomainEvent]:
        """Replays all published domain events for event sourcing."""

        return list(self._history)


class CommandBus(ICommandBus):
    """Command Bus handling synchronous/asynchronous command dispatching."""

    def __init__(self, registry: Optional[HandlerRegistry] = None, dlq: Optional[DeadLetterQueue] = None):
        self.registry = registry or HandlerRegistry()
        self.dlq = dlq or DeadLetterQueue()

    async def dispatch(self, command: AgentCommand) -> CommandResult:
        handler = await self.registry.get_command_handler(command.command_type)
        if not handler:
            raise HandlerNotFoundException(f"No command handler registered for '{command.command_type}'")
        return await handler.handle_command(command)


class QueryBus(IQueryBus):
    """Query Bus handling request/response queries."""

    def __init__(self, registry: Optional[HandlerRegistry] = None):
        self.registry = registry or HandlerRegistry()

    async def query(self, query: AgentQuery) -> QueryResult:
        handler = await self.registry.get_query_handler(query.query_type)
        if not handler:
            raise HandlerNotFoundException(f"No query handler registered for '{query.query_type}'")
        return await handler.handle_query(query)


class UnifiedMessageBus:
    """Aggregate Unified Message Bus coordinating EventBus, CommandBus, QueryBus."""

    def __init__(self):
        self.registry = HandlerRegistry()
        self.event_bus = EventBus(registry=self.registry)
        self.command_bus = CommandBus(registry=self.registry)
        self.query_bus = QueryBus(registry=self.registry)
