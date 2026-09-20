"""Repository Inventory & File Structure Collector."""

import os
from pathlib import Path
from typing import List, Dict, Any
from ..domain.evidence.models import (
    EvidenceRecord,
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceSourceType,
)
from ..base import BaseCollector


class RepositoryCollector(BaseCollector):
    """Inspects root layout, counts files, measures LOC, and verifies tree hygiene."""

    @property
    def name(self) -> str:
        return "RepositoryCollector"

    @property
    def category(self) -> str:
        return "RepositoryStructure"

    async def collect(self) -> List[EvidenceRecord]:
        records: List[EvidenceRecord] = []

        total_files = 0
        total_dirs = 0
        total_loc = 0
        extension_counts: Dict[str, int] = {}
        root_items: List[str] = []

        # Inspect root directory items
        try:
            root_items = [p.name for p in self.repo_root.iterdir()]
        except Exception:
            root_items = []

        # Traverse repository tree ignoring typical caches
        ignored_dirs = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", "node_modules"}

        for root, dirs, files in os.walk(self.repo_root):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]
            total_dirs += len(dirs)

            for f in files:
                ext = Path(f).suffix.lower() or "no_ext"
                extension_counts[ext] = extension_counts.get(ext, 0) + 1
                total_files += 1

                if ext in {".py", ".md", ".yml", ".yaml", ".json", ".toml"}:
                    file_path = Path(root) / f
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                            lines = fp.readlines()
                            total_loc += len(lines)
                    except Exception:
                        pass

        inventory_payload: Dict[str, Any] = {
            "total_files": total_files,
            "total_dirs": total_dirs,
            "total_loc": total_loc,
            "extension_counts": extension_counts,
            "root_items": sorted(root_items),
        }

        # Check root cleanliness (should not contain test dumps)
        has_cluttered_root = any(item.startswith("test_") or "dump" in item for item in root_items if os.path.isdir(self.repo_root / item))

        classification = (
            EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS
            if not has_cluttered_root
            else EvidenceClassification.PARTIALLY_VERIFIED
        )

        record = EvidenceRecord.create(
            category=self.category,
            collector=self.name,
            source_type=EvidenceSourceType.STATIC_SOURCE_CODE,
            raw_payload=inventory_payload,
            summary=f"Scanned {total_files} tracked files across {total_dirs} directories ({total_loc:,} LOC). Root clean: {not has_cluttered_root}.",
            confidence=EvidenceConfidence.MEDIUM,
            classification=classification,
        )
        records.append(record)
        return records
