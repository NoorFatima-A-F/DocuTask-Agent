"""Golden Baseline Manifest Models."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class PolicyBaseline(BaseModel):
    policy_name: str
    minimum_confidence: str
    required_domains: List[str]
    forbidden_critical_findings: bool
    minimum_eqi: float


class RuleBaseline(BaseModel):
    rule_name: str
    expected_classification: str
    required_evidence_type: str


class GoldenBaselineManifest(BaseModel):
    """Immutable snapshot of a certified baseline release."""
    baseline_version: str = "1.0.0"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    engine_version: str = "2.1.0"
    engine_source_hash: str
    policies: Dict[str, PolicyBaseline] = Field(default_factory=dict)
    rules: List[RuleBaseline] = Field(default_factory=list)
    file_hashes: Dict[str, str] = Field(default_factory=dict)
    approved_by: str = "Enterprise-Architecture-Board"
