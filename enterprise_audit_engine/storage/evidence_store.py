"""Immutable Evidence Storage Engine."""

import json
from pathlib import Path
from typing import List, Optional
from ..domain.evidence.models import EvidenceRecord, AuditReportManifest


class EvidenceStore:
    """Persists immutable evidence records and manages audit manifests."""

    def __init__(self, storage_dir: Path):
        self.storage_dir = storage_dir
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_evidence(self, record: EvidenceRecord) -> Path:
        """Saves an immutable evidence record to disk."""
        sanitized_id = "".join(c for c in record.id if c.isalnum() or c in ("-", "_"))
        sanitized_cat = "".join(c for c in record.category if c.isalnum() or c in ("-", "_"))
        filename = f"{sanitized_id}_{sanitized_cat}.json"
        base_dir = self.storage_dir.resolve()
        target_path = (base_dir / filename).resolve()
        try:
            is_rel = target_path.is_relative_to(base_dir)
        except AttributeError:
            is_rel = True
        if not is_rel:
            raise ValueError("Security violation: Path traversal detected in evidence store.")
        data = record.model_dump()
        with open(target_path, "w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=2, sort_keys=True)
        return target_path

    def load_all_evidence(self) -> List[EvidenceRecord]:
        """Loads all stored evidence records from storage."""
        records: List[EvidenceRecord] = []
        for file_path in self.storage_dir.glob("EV-*.json"):
            try:
                with open(file_path, "r", encoding="utf-8") as fp:
                    data = json.load(fp)
                    record = EvidenceRecord(**data)
                    records.append(record)
            except Exception:
                pass
        return sorted(records, key=lambda r: r.id)

    def save_manifest(self, manifest: AuditReportManifest) -> Path:
        """Saves run manifest."""
        manifest_path = self.storage_dir / "audit_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as fp:
            json.dump(manifest.model_dump(), fp, indent=2, sort_keys=True)
        return manifest_path
