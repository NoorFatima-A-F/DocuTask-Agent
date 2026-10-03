"""
Experiment Manifest (Phase 82B.1)
=================================
Strongly-typed, immutable scientific experiment manifest providing complete
specification of experiment parameters, environment fingerprints, dataset
hashes, and cryptographic validation digests.
"""

from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json
from research_validation.provenance.provenance_models import EvidenceQualityLevel


class ExperimentStatus(str, Enum):
    REGISTERED = "REGISTERED"
    SCHEDULED = "SCHEDULED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    INVALIDATED = "INVALIDATED"
    NOT_EXECUTED = "NOT_EXECUTED"


@dataclass(frozen=True)
class ExperimentParameters:
    sample_count: int
    seed: int
    batch_size: int = 32
    target_metrics: Tuple[str, ...] = ("f1", "precision", "recall", "latency_p99_ms")
    custom_parameters: Dict[str, Any] = field(default_factory=dict)

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "sample_count": self.sample_count,
            "seed": self.seed,
            "batch_size": self.batch_size,
            "target_metrics": list(self.target_metrics),
            "custom_parameters": self.custom_parameters,
        }


@dataclass(frozen=True)
class DatasetFingerprint:
    dataset_name: str
    dataset_version: str
    expected_sample_count: int
    sha256_checksum: str
    split: str = "test"
    canonical_source_url: str = ""

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "dataset_version": self.dataset_version,
            "expected_sample_count": self.expected_sample_count,
            "sha256_checksum": self.sha256_checksum,
            "split": self.split,
            "canonical_source_url": self.canonical_source_url,
        }


@dataclass(frozen=True)
class ExperimentManifest:
    experiment_id: str
    title: str
    description: str
    semantic_version: str
    created_at_utc: str
    author: str
    git_commit_sha: str
    parameters: ExperimentParameters
    dataset: DatasetFingerprint
    environment: Dict[str, Any]
    quality_level: EvidenceQualityLevel
    tags: Tuple[str, ...] = ()
    manifest_digest_sha256: str = field(default="")

    @classmethod
    def create(
        cls,
        title: str,
        description: str,
        parameters: ExperimentParameters,
        dataset: DatasetFingerprint,
        environment: Dict[str, Any],
        author: str = "Research Engineering Team",
        semantic_version: str = "1.0.0",
        git_commit_sha: str = "HEAD",
        quality_level: EvidenceQualityLevel = EvidenceQualityLevel.LEVEL_A,
        tags: Tuple[str, ...] = (),
        experiment_id: Optional[str] = None,
    ) -> ExperimentManifest:
        """Create an immutable ExperimentManifest and compute its cryptographic SHA-256 digest."""
        exp_id = experiment_id or f"exp_{uuid.uuid4().hex[:12]}"
        now_str = datetime.now(timezone.utc).isoformat()

        payload = {
            "experiment_id": exp_id,
            "title": title,
            "description": description,
            "semantic_version": semantic_version,
            "created_at_utc": now_str,
            "author": author,
            "git_commit_sha": git_commit_sha,
            "parameters": parameters.canonical_dict(),
            "dataset": dataset.canonical_dict(),
            "environment": environment,
            "quality_level": quality_level.value,
            "tags": list(tags),
        }
        digest = hash_canonical_json(payload)

        return cls(
            experiment_id=exp_id,
            title=title,
            description=description,
            semantic_version=semantic_version,
            created_at_utc=now_str,
            author=author,
            git_commit_sha=git_commit_sha,
            parameters=parameters,
            dataset=dataset,
            environment=environment,
            quality_level=quality_level,
            tags=tags,
            manifest_digest_sha256=digest,
        )

    def to_canonical_dict(self) -> Dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "title": self.title,
            "description": self.description,
            "semantic_version": self.semantic_version,
            "created_at_utc": self.created_at_utc,
            "author": self.author,
            "git_commit_sha": self.git_commit_sha,
            "parameters": self.parameters.canonical_dict(),
            "dataset": self.dataset.canonical_dict(),
            "environment": self.environment,
            "quality_level": self.quality_level.value,
            "tags": list(self.tags),
            "manifest_digest_sha256": self.manifest_digest_sha256,
        }
