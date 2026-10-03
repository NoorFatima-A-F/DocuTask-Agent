"""
Publication Diff Engine (Phase 92C)
==================================
Calculates structured differences between publication versions across
claims, tables, figures, confidence intervals, and limitations.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass(frozen=True)
class PublicationDiffItem:
    """A specific change between two publication versions."""
    section: str
    item_key: str
    old_value: str
    new_value: str
    change_type: str  # "UPDATED", "ADDED", "REMOVED"
    evidence_citation_sha256: str


@dataclass(frozen=True)
class PublicationEvolutionReport:
    """Consolidated summary of publication evolution."""
    from_version: str
    to_version: str
    changes: List[PublicationDiffItem]
    timestamp_utc: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    has_significant_changes: bool = False
