"""
Capability Resolver Component.
Evaluates capability requirements against registered tools, filters candidates by constraints,
calculates fitness scores, and returns ranked candidate matches.
"""

from typing import List
from app.agents.tools.capabilities import (
    CapabilityMatch,
    CapabilityRequirement,
    CapabilityScore,
)
from app.agents.tools.interfaces import ICapabilityResolver, IToolRegistry


class CapabilityResolver(ICapabilityResolver):
    """Engine resolving capability requirement queries into ranked tool candidate matches."""

    def __init__(self, registry: IToolRegistry):
        self.registry = registry

    async def resolve(self, requirement: CapabilityRequirement) -> List[CapabilityMatch]:
        """Resolves capability query, applies constraint filters, scores candidates, and ranks results."""
        tools = await self.registry.list_tools()
        matches: List[CapabilityMatch] = []

        req_cap = requirement.capability_name.upper()

        for desc in tools:
            # Check capability support
            supported_caps = [c.upper() for c in desc.metadata.supported_capabilities]
            if req_cap not in supported_caps:
                continue

            # Document Type Filter
            if requirement.document_type:
                supported_docs = [d.lower() for d in desc.metadata.supported_document_types]
                if supported_docs and requirement.document_type.lower() not in supported_docs:
                    continue

            # MIME Type Filter
            if requirement.mime_type:
                supported_mimes = [m.lower() for m in desc.metadata.supported_mime_types]
                if supported_mimes and requirement.mime_type.lower() not in supported_mimes:
                    continue

            # Cost Filter
            cost = desc.metadata.cost_profile.cost_per_call_usd
            if requirement.max_cost_usd is not None and cost > requirement.max_cost_usd:
                continue

            # Latency Filter
            latency = desc.metadata.latency_profile.p50_latency_ms
            if requirement.max_latency_ms is not None and latency > requirement.max_latency_ms:
                continue

            # Calculate Scores
            confidence = desc.statistics.confidence_score
            if confidence < requirement.min_confidence:
                continue

            cost_score = max(0.0, 1.0 - (cost / 0.05)) if cost > 0 else 1.0
            latency_score = max(0.0, 1.0 - (latency / 5000.0))
            overall = (confidence * 0.4) + (cost_score * 0.3) + (latency_score * 0.3)

            score = CapabilityScore(
                overall_score=round(overall, 4),
                confidence_score=round(confidence, 4),
                cost_score=round(cost_score, 4),
                latency_score=round(latency_score, 4),
                health_score=1.0
            )

            match = CapabilityMatch(
                tool_id=desc.identity.tool_id,
                tool_name=desc.identity.name,
                provider_name=desc.identity.provider_name,
                score=score,
                reasons=[f"Matched capability '{requirement.capability_name}' with overall score {score.overall_score}"]
            )
            matches.append(match)

        # Rank candidates by overall score descending
        matches.sort(key=lambda m: m.score.overall_score, reverse=True)
        return matches
