"""
Knowledge Versioning for Phase 13.5 (ARLP-KIP).
Semantic versioning and history tracking for knowledge artifacts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class KnowledgeVersionRecord(BaseModel):
    record_id: str
    version: str
    previous_version: Optional[str] = None
    change_summary: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class KnowledgeVersioning:
    """
    Manages semantic version increments and historical diffs.
    """

    @classmethod
    def increment_patch(cls, version: str) -> str:
        parts = version.split(".")
        if len(parts) == 3:
            return f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"
        return f"{version}.1"

    @classmethod
    def increment_minor(cls, version: str) -> str:
        parts = version.split(".")
        if len(parts) == 3:
            return f"{parts[0]}.{int(parts[1]) + 1}.0"
        return f"{version}.1"
