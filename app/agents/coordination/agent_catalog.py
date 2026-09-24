"""
Agent Catalog.
Standardized templates and archetypes for creating autonomous agents in the platform.
"""

from app.agents.coordination.agent_profile import AgentProfile
from app.agents.coordination.capability import AgentSkill, CapabilityProfile
from app.agents.coordination.agent_identity import AgentIdentity


class AgentCatalog:
    """Pre-configured agent archetypes for rapid team and swarm provisioning."""

    @staticmethod
    def supervisor_template(name: str = "SupervisorAgent") -> AgentProfile:
        return AgentProfile(
            identity=AgentIdentity(name=name, role="supervisor"),
            capabilities=CapabilityProfile(
                skills=[AgentSkill(name="coordination", domain="orchestration")],
                execution_domains=["orchestration", "governance"],
                confidence_rating=0.99
            )
        )

    @staticmethod
    def extraction_worker_template(name: str = "ExtractionWorker") -> AgentProfile:
        return AgentProfile(
            identity=AgentIdentity(name=name, role="worker"),
            capabilities=CapabilityProfile(
                skills=[
                    AgentSkill(name="pdf_parsing", domain="document_processing"),
                    AgentSkill(name="table_extraction", domain="document_processing")
                ],
                supported_tools=["pdf_parser", "table_extractor"],
                execution_domains=["document_processing", "financial"],
                confidence_rating=0.95
            )
        )

    @staticmethod
    def reasoning_specialist_template(name: str = "ReasoningSpecialist") -> AgentProfile:
        return AgentProfile(
            identity=AgentIdentity(name=name, role="specialist"),
            capabilities=CapabilityProfile(
                skills=[
                    AgentSkill(name="financial_analysis", domain="financial"),
                    AgentSkill(name="risk_assessment", domain="compliance")
                ],
                supported_tools=["calculator", "compliance_checker"],
                execution_domains=["financial", "compliance"],
                confidence_rating=0.97
            )
        )
