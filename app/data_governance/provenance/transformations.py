"""Provenance Transformation Records (Phase 8B)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ProvenanceTransformationRecord(BaseModel):
    """Detailed audit record of an AI or pipeline transformation step."""
    transformation_id: str
    asset_id: str
    step_name: str
    input_artifacts: List[Dict[str, str]] = Field(default_factory=list)  # [{"asset_id": "...", "version": "..."}]
    output_artifacts: List[Dict[str, str]] = Field(default_factory=list)
    model_version: Optional[str] = None
    prompt_version: Optional[str] = None
    agent_id: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    policy_decision_id: Optional[str] = None
    actor_id: str = "system"
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
