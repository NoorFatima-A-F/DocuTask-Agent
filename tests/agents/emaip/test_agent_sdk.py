"""
Tests for Agent SDK and AgentBuilder fluent API.
"""

from app.agents.domain.agent_entity import AgentLifecycleState, AgentType, TrustLevel
from app.agents.sdk.builder import AgentBuilder


def test_agent_builder_fluent_api():
    agent = (
        AgentBuilder("LegalContractReviewer")
        .type(AgentType.LEGAL)
        .version("1.2.0")
        .organization("org-acme-corp")
        .workspace("ws-legal")
        .owner("chief-counsel")
        .skill("analysis")
        .skills(["compliance", "summarization"])
        .capability("document.legal_review")
        .model("gemini-2.5-pro")
        .prompt_version("2.0.0")
        .memory_namespace("legal_contracts")
        .policy_set("strict_legal_policy")
        .trust_level(TrustLevel.HIGH)
        .budget(max_cost_usd=2.5, max_tokens=200000)
        .metadata(jurisdiction="US-CA")
        .build()
    )

    assert agent.name == "LegalContractReviewer"
    assert agent.type == AgentType.LEGAL
    assert agent.version == "1.2.0"
    assert agent.organization_id == "org-acme-corp"
    assert agent.workspace_id == "ws-legal"
    assert agent.owner == "chief-counsel"
    assert "analysis" in agent.skills
    assert "compliance" in agent.skills
    assert "summarization" in agent.skills
    assert "document.legal_review" in agent.capabilities
    assert agent.model == "gemini-2.5-pro"
    assert agent.prompt_version == "2.0.0"
    assert agent.memory_namespace == "legal_contracts"
    assert agent.policy_set == "strict_legal_policy"
    assert agent.trust_level == TrustLevel.HIGH
    assert agent.budget["max_cost_usd"] == 2.5
    assert agent.metadata["jurisdiction"] == "US-CA"
    assert agent.status == AgentLifecycleState.CREATED
