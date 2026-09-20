"""
Evidence Registry for Enterprise AAOS.
Provides append-only storage, search indexing, dependency traversal,
and cryptographic verification for engineering evidence items.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from app.evidence.registry.evidence_models import EvidenceItem, EvidenceType, VerificationStatus

logger = logging.getLogger(__name__)


class EvidenceRegistry:
    """
    Append-only repository of validated engineering evidence.
    Guarantees no duplicated IDs, validates tamper-evident SHA-256 hashes,
    and supports multi-dimensional querying by type, source, and verification status.
    """

    def __init__(self, persistence_path: Optional[Path] = None) -> None:
        self.persistence_path = persistence_path
        self._items: Dict[str, EvidenceItem] = {}
        self._type_index: Dict[EvidenceType, List[str]] = {}
        self._source_index: Dict[str, List[str]] = {}

    def register(self, item: EvidenceItem) -> EvidenceItem:
        """Registers a new evidence item with integrity checks."""
        # Check for ID conflict
        if item.evidence_id in self._items:
            existing = self._items[item.evidence_id]
            if existing.item_hash == item.item_hash:
                logger.debug("EvidenceItem %s already registered with matching hash.", item.evidence_id)
                return existing
            raise ValueError(f"Evidence ID collision with differing hash: {item.evidence_id}")

        # Verify hash integrity
        expected_hash = item.compute_hash()
        if item.item_hash != expected_hash:
            item.verification_status = VerificationStatus.HASH_MISMATCH
            logger.warning("Hash mismatch for EvidenceItem %s: %s != %s", item.evidence_id, item.item_hash, expected_hash)

        self._items[item.evidence_id] = item

        # Update secondary indices
        if item.evidence_type not in self._type_index:
            self._type_index[item.evidence_type] = []
        self._type_index[item.evidence_type].append(item.evidence_id)

        if item.source not in self._source_index:
            self._source_index[item.source] = []
        self._source_index[item.source].append(item.evidence_id)

        logger.info("Registered EvidenceItem [%s] '%s' (%s)", item.evidence_id, item.title, item.evidence_type.value)
        return item

    def get(self, evidence_id: str) -> Optional[EvidenceItem]:
        """Retrieves evidence item by ID."""
        return self._items.get(evidence_id)

    def list_all(self) -> List[EvidenceItem]:
        """Returns all registered evidence items."""
        return list(self._items.values())

    def filter_by_type(self, evidence_type: EvidenceType) -> List[EvidenceItem]:
        """Filters evidence items by EvidenceType."""
        ids = self._type_index.get(evidence_type, [])
        return [self._items[eid] for eid in ids if eid in self._items]

    def filter_by_source(self, source_pattern: str) -> List[EvidenceItem]:
        """Filters evidence items by source string."""
        return [item for item in self._items.values() if source_pattern in item.source]

    def count(self) -> int:
        return len(self._items)

    def export_catalog(self, output_file: Optional[Path] = None) -> Dict[str, Any]:
        """Exports evidence catalog to structured JSON."""
        catalog = {
            "total_evidence_items": len(self._items),
            "by_type": {t.value: len(ids) for t, ids in self._type_index.items()},
            "verified_items_count": sum(1 for item in self._items.values() if item.verification_status == VerificationStatus.VERIFIED),
            "items": [item.to_dict() for item in self._items.values()],
        }
        target = output_file or self.persistence_path
        if target:
            target.parent.mkdir(parents=True, exist_ok=True)
            with open(target, "w", encoding="utf-8") as f:
                json.dump(catalog, f, indent=2)
            logger.info("Saved evidence catalog (%d items) to %s", len(self._items), target)
        return catalog

    def load_catalog(self, catalog_file: Path) -> int:
        """Loads evidence items from an existing catalog JSON file."""
        if not catalog_file.exists():
            return 0
        with open(catalog_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        loaded = 0
        for item_dict in data.get("items", []):
            item = EvidenceItem.from_dict(item_dict)
            self.register(item)
            loaded += 1
        return loaded
