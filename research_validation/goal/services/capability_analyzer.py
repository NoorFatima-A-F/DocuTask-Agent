"""
Capability Analyzer Service
===========================
Analyzes required capabilities against available subsystem providers,
detects gaps, and calculates overall capability confidence.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set

from research_validation.goal.models.capability_requirement import (
    CapabilityRequirement, CapabilityCriticality
)
from research_validation.goal.interfaces.capability_provider import (
    ICapabilityProvider, DiscoveredCapability, DefaultSystemCapabilityProvider
)


@dataclass(frozen=True)
class CapabilityAnalysisResult:
    """Consolidated outcome of capability discovery and gap evaluation."""
    is_fully_satisfied: bool
    satisfied_capabilities: List[str]
    missing_mandatory_capabilities: List[str]
    missing_optional_capabilities: List[str]
    capability_gaps: List[str]
    capability_confidence: float  # 0.0 to 1.0
    diagnostic: str = ""


class CapabilityAnalyzer:
    """
    Evaluates goal capability requirements against active environment providers.
    """

    def __init__(self, provider: Optional[ICapabilityProvider] = None):
        self.provider = provider or DefaultSystemCapabilityProvider()

    def analyze_capabilities(
        self,
        requirements: List[CapabilityRequirement],
    ) -> CapabilityAnalysisResult:
        """Evaluates whether requirements are satisfied by the active provider."""
        discovered = {c.capability_name: c for c in self.provider.discover_capabilities() if c.is_available}

        satisfied: List[str] = []
        missing_mandatory: List[str] = []
        missing_optional: List[str] = []
        gaps: List[str] = []
        confidence_scores: List[float] = []

        for req in requirements:
            disc = discovered.get(req.capability_name)
            if disc:
                satisfied.append(req.capability_name)
                confidence_scores.append(disc.confidence)
            else:
                if req.criticality == CapabilityCriticality.MANDATORY:
                    missing_mandatory.append(req.capability_name)
                    gaps.append(f"MANDATORY: Subsystem '{req.capability_name}' is unavailable.")
                    confidence_scores.append(0.0)
                else:
                    missing_optional.append(req.capability_name)
                    gaps.append(f"OPTIONAL: Subsystem '{req.capability_name}' is unavailable.")
                    confidence_scores.append(0.5)

        avg_conf = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 1.0
        fully_satisfied = (len(missing_mandatory) == 0)

        diag = (
            "All mandatory capabilities satisfied."
            if fully_satisfied else
            f"Blocked: Missing mandatory capabilities: {', '.join(missing_mandatory)}"
        )

        return CapabilityAnalysisResult(
            is_fully_satisfied=fully_satisfied,
            satisfied_capabilities=satisfied,
            missing_mandatory_capabilities=missing_mandatory,
            missing_optional_capabilities=missing_optional,
            capability_gaps=gaps,
            capability_confidence=avg_conf,
            diagnostic=diag,
        )
