"""
Core Messaging Interfaces.
Defines IEventBus, ICommandBus, IQueryBus, and IMessageBroker contracts.
"""

from abc import ABC, abstractmethod
from typing import Callable, Coroutine
from app.agents.messaging.commands import AgentCommand, CommandResult
from app.agents.messaging.events import DomainEvent
from app.agents.messaging.queries import AgentQuery, QueryResult


class IEventBus(ABC):
    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        pass

    @abstractmethod
    async def subscribe(self, event_type: str, handler: Callable[[DomainEvent], Coroutine]) -> None:
        pass


class ICommandBus(ABC):
    @abstractmethod
    async def dispatch(self, command: AgentCommand) -> CommandResult:
        pass


class IQueryBus(ABC):
    @abstractmethod
    async def query(self, query: AgentQuery) -> QueryResult:
        pass
