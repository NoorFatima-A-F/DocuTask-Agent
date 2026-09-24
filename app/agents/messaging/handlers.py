"""
Message Handler Abstractions.
"""

from abc import ABC, abstractmethod
from app.agents.messaging.commands import AgentCommand, CommandResult
from app.agents.messaging.events import DomainEvent
from app.agents.messaging.queries import AgentQuery, QueryResult


class CommandHandler(ABC):
    @abstractmethod
    async def handle_command(self, command: AgentCommand) -> CommandResult:
        pass


class EventHandler(ABC):
    @abstractmethod
    async def handle_event(self, event: DomainEvent) -> None:
        pass


class QueryHandler(ABC):
    @abstractmethod
    async def handle_query(self, query: AgentQuery) -> QueryResult:
        pass
