"""
Research Governance Policy (Phase 93C)
=====================================
Formal declarations of scientific integrity, provenance, privacy,
and statistical power policies.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class PolicyCategory(str, Enum):
    ZERO_FABRICATION = "ZERO_FABRICATION"
    PROVENANCE_INTEGRITY = "PROVENANCE_INTEGRITY"
    STATISTICAL_RIGOR = "STATISTICAL_RIGOR"
    PRIVACY_DATA_MINIMIZATION = "PRIVACY_DATA_MINIMIZATION"
    SAFETY_RISK_LIMIT = "SAFETY_RISK_LIMIT"


class PolicyEnforcementAction(str, Enum):
    ALLOW = "ALLOW"
    FLAG_WARNING = "FLAG_WARNING"
    BLOCK_EXECUTION = "BLOCK_EXECUTION"


@dataclass(frozen=True)
class GovernancePolicyRule:
    """A formal rule in the research governance policy."""
    rule_id: str
    category: PolicyCategory
    name: str
    description: str
    enforcement_action: PolicyEnforcementAction
    is_mandatory: bool = True
