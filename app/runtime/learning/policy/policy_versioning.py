"""
Policy Versioning for Phase 13.5 (ARLP-KIP).
Tracks evolution trees, branches, and semantic version transitions for policies.
"""

from typing import Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class PolicyVersionEntry(BaseModel):
    version_id: str
    policy_id: str
    version: str
    parent_version: Optional[str] = None
    change_summary: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class PolicyBranchVersioner:
    """
    Manages policy evolution branch lineages and semantic version transitions.
    """

    @classmethod
    def next_version(cls, current_version: str) -> str:
        parts = current_version.split(".")
        if len(parts) == 3:
            return f"{parts[0]}.{int(parts[1]) + 1}.0"
        return f"{current_version}.1"
