"""
Agent Metrics Collector Interface.
Defines abstract metric tracking hooks for execution latency, planning latency,
retries, failure rates, and reflection performance.
"""

from abc import ABC, abstractmethod


class AgentMetricsCollector(ABC):
    """Abstract interface for recording agent operational metrics."""

    @abstractmethod
    def record_execution_duration(self, agent_name: str, duration_seconds: float) -> None:
        """Records total agent execution duration in seconds."""
        pass

    @abstractmethod
    def record_planning_latency(self, agent_name: str, duration_seconds: float) -> None:
        """Records agent goal planning phase latency."""
        pass

    @abstractmethod
    def record_execution_latency(self, agent_name: str, duration_seconds: float) -> None:
        """Records agent execution phase latency."""
        pass

    @abstractmethod
    def record_reflection_latency(self, agent_name: str, duration_seconds: float) -> None:
        """Records agent reflection phase latency."""
        pass

    @abstractmethod
    def increment_retries(self, agent_name: str) -> None:
        """Increments agent execution retry counter."""
        pass

    @abstractmethod
    def increment_failures(self, agent_name: str, failure_reason: str) -> None:
        """Increments agent execution failure counter."""
        pass

    @abstractmethod
    def increment_successes(self, agent_name: str) -> None:
        """Increments agent execution success counter."""
        pass


class NoOpAgentMetricsCollector(AgentMetricsCollector):
    """Default non-operational metrics collector implementation."""

    def record_execution_duration(self, agent_name: str, duration_seconds: float) -> None:
        pass

    def record_planning_latency(self, agent_name: str, duration_seconds: float) -> None:
        pass

    def record_execution_latency(self, agent_name: str, duration_seconds: float) -> None:
        pass

    def record_reflection_latency(self, agent_name: str, duration_seconds: float) -> None:
        pass

    def increment_retries(self, agent_name: str) -> None:
        pass

    def increment_failures(self, agent_name: str, failure_reason: str) -> None:
        pass

    def increment_successes(self, agent_name: str) -> None:
        pass
