"""
Delegation Policy.
Enforces security, recursion depth boundaries, and loop prevention on multi-agent delegations.
"""

from typing import List
from uuid import UUID
from pydantic import BaseModel, Field
from app.agents.coordination.exceptions import CircularDelegationError


class DelegationPolicy(BaseModel):
    """Rules governing allowable delegation parameters and depth."""
    max_depth: int = Field(default=4, ge=1)
    allow_recursive: bool = True
    allow_fallback: bool = True
    prohibit_circular_chains: bool = True

    model_config = {"frozen": True}

    def validate_delegation_chain(self, chain: List[UUID], next_agent_id: UUID) -> None:
        """Ensures next agent does not create a circular delegation loop."""
        if self.prohibit_circular_chains and next_agent_id in chain:
            raise CircularDelegationError(
                f"Circular delegation detected: agent {next_agent_id} is already in chain {[str(a) for a in chain]}.",
                next_agent_id
            )
        if len(chain) >= self.max_depth:
            raise CircularDelegationError(
                f"Delegation chain exceeded maximum depth limit of {self.max_depth}.",
                next_agent_id
            )
