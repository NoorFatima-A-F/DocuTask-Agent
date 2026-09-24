"""
Agent Factory.
Instantiates agents using standard templates or custom definitions.
"""

from app.agents.coordination.agent import Agent
from app.agents.coordination.agent_builder import AgentBuilder
from app.agents.coordination.agent_catalog import AgentCatalog


class AgentFactory:
    """Factory creating configured Agent instances."""

    @staticmethod
    def create_supervisor(name: str = "PrimarySupervisor") -> Agent:
        profile = AgentCatalog.supervisor_template(name)
        return Agent(profile=profile)

    @staticmethod
    def create_extraction_worker(name: str = "ExtractionWorker") -> Agent:
        profile = AgentCatalog.extraction_worker_template(name)
        return Agent(profile=profile)

    @staticmethod
    def create_reasoning_specialist(name: str = "ReasoningSpecialist") -> Agent:
        profile = AgentCatalog.reasoning_specialist_template(name)
        return Agent(profile=profile)

    @staticmethod
    def custom_agent(name: str) -> AgentBuilder:
        return AgentBuilder(name)
