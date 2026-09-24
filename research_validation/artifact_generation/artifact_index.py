"""
Artifact Index & Master Manifest (Phase 82B.5)
==============================================
Maintains the centralized index of all synthesized publication figures, tables,
raw CSV datasets, LaTeX snippets, and markdown reports.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple

from research_validation.artifact_generation.paper_figures import GeneratedFigure
from research_validation.artifact_generation.publication_tables import PublicationTable
from research_validation.provenance.hashing import hash_canonical_json


@dataclass(frozen=True)
class IndexedArtifactEntry:
    artifact_id: str
    artifact_type: str  # "FIGURE", "TABLE", "REPORT", "DATASET", "LATEX"
    title: str
    format: str
    sha256_digest: str
    originating_experiment_ids: Tuple[str, ...]
    relative_path: str


@dataclass(frozen=True)
class MasterArtifactIndex:
    index_id: str
    timestamp_utc: str
    total_artifacts: int
    artifacts_by_type: Dict[str, int]
    entries: Tuple[IndexedArtifactEntry, ...]
    master_index_root_hash: str


class ArtifactIndexer:
    """
    Builds the master manifest index for research publication artifacts.
    """

    def __init__(self):
        self._entries: List[IndexedArtifactEntry] = []

    def register_figure(self, figure: GeneratedFigure, relative_path: str) -> IndexedArtifactEntry:
        entry = IndexedArtifactEntry(
            artifact_id=figure.figure_id,
            artifact_type="FIGURE",
            title=figure.title,
            format=figure.figure_format,
            sha256_digest=figure.figure_sha256,
            originating_experiment_ids=figure.originating_experiment_ids,
            relative_path=relative_path,
        )
        self._entries.append(entry)
        return entry

    def register_table(self, table: PublicationTable, relative_path: str) -> IndexedArtifactEntry:
        entry = IndexedArtifactEntry(
            artifact_id=table.table_id,
            artifact_type="TABLE",
            title=table.title,
            format="TABLE_DATACLASS",
            sha256_digest=table.table_digest_sha256,
            originating_experiment_ids=table.originating_experiment_ids,
            relative_path=relative_path,
        )
        self._entries.append(entry)
        return entry

    def register_generic(
        self,
        artifact_id: str,
        artifact_type: str,
        title: str,
        fmt: str,
        sha256_digest: str,
        originating_exp_ids: List[str],
        relative_path: str,
    ) -> IndexedArtifactEntry:
        entry = IndexedArtifactEntry(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            title=title,
            format=fmt,
            sha256_digest=sha256_digest,
            originating_experiment_ids=tuple(originating_exp_ids),
            relative_path=relative_path,
        )
        self._entries.append(entry)
        return entry

    def build_master_index(self, index_id: Optional[str] = None) -> MasterArtifactIndex:
        now_str = datetime.now(timezone.utc).isoformat()
        idx_id = index_id or f"idx_{int(datetime.now(timezone.utc).timestamp())}"

        type_counts: Dict[str, int] = {}
        for e in self._entries:
            type_counts[e.artifact_type] = type_counts.get(e.artifact_type, 0) + 1

        payload = {
            "index_id": idx_id,
            "entries": [
                {
                    "id": e.artifact_id,
                    "type": e.artifact_type,
                    "sha": e.sha256_digest,
                    "path": e.relative_path,
                }
                for e in self._entries
            ]
        }
        root_h = hash_canonical_json(payload)

        return MasterArtifactIndex(
            index_id=idx_id,
            timestamp_utc=now_str,
            total_artifacts=len(self._entries),
            artifacts_by_type=type_counts,
            entries=tuple(self._entries),
            master_index_root_hash=root_h,
        )
