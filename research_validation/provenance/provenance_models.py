"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_models.py

Core domain models conforming to W3C PROV, OpenLineage, and FAIR principles.
Includes the 5-Tier Evidence Quality Scoring system.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Tuple

from research_validation.provenance.hashing import HashAlgorithm, ProvenanceHasher


class EvidenceQualityLevel(str, Enum):
    """
    5-Tier Evidence Quality Classification:
    - LEVEL_A: Independently reproduced by external reviewers using public datasets.
    - LEVEL_B: Cross-validated against trusted reference implementations and public benchmarks.
    - LEVEL_C: Internally measured with complete provenance, Merkle chain, and reproducibility.
    - LEVEL_D: Simulated, synthetic, or model-estimated.
    - LEVEL_E: Unsupported, unverified, or missing lineage.
    """
    LEVEL_A = "LEVEL_A"
    LEVEL_B = "LEVEL_B"
    LEVEL_C = "LEVEL_C"
    LEVEL_D = "LEVEL_D"
    LEVEL_E = "LEVEL_E"

    @property
    def numeric_weight(self) -> float:
        weights = {
            EvidenceQualityLevel.LEVEL_A: 1.0,
            EvidenceQualityLevel.LEVEL_B: 0.85,
            EvidenceQualityLevel.LEVEL_C: 0.70,
            EvidenceQualityLevel.LEVEL_D: 0.40,
            EvidenceQualityLevel.LEVEL_E: 0.0,
        }
        return weights[self]

    @property
    def description(self) -> str:
        descriptions = {
            EvidenceQualityLevel.LEVEL_A: "Independently reproduced by external reviewers on public benchmark datasets.",
            EvidenceQualityLevel.LEVEL_B: "Cross-validated against authoritative reference implementations (SciPy, NumPy, R) and canonical datasets.",
            EvidenceQualityLevel.LEVEL_C: "Internally measured with complete unbroken Merkle provenance, hardware telemetry, and environment manifests.",
            EvidenceQualityLevel.LEVEL_D: "Simulated, synthetic, or estimated via theoretical model bounds.",
            EvidenceQualityLevel.LEVEL_E: "Unsupported, unverified, incomplete, or broken lineage trail.",
        }
        return descriptions[self]


class LineageStage(str, Enum):
    """Canonical lineage progression stages."""
    RAW_OBSERVATION = "RAW_OBSERVATION"
    TRANSFORMATION = "TRANSFORMATION"
    INTERMEDIATE_ARTIFACT = "INTERMEDIATE_ARTIFACT"
    AGGREGATION = "AGGREGATION"
    FINAL_METRIC = "FINAL_METRIC"
    SCIENTIFIC_REPORT = "SCIENTIFIC_REPORT"
    DIGITAL_SIGNATURE = "DIGITAL_SIGNATURE"


class ProvRelationType(str, Enum):
    """Standard W3C PROV relationship types."""
    USED = "used"
    WAS_GENERATED_BY = "wasGeneratedBy"
    WAS_DERIVED_FROM = "wasDerivedFrom"
    WAS_ATTRIBUTED_TO = "wasAttributedTo"
    WAS_ASSOCIATED_WITH = "wasAssociatedWith"
    ACTED_ON_BEHALF_OF = "actedOnBehalfOf"
    WAS_INFORMED_BY = "wasInformedBy"


@dataclass
class EnvironmentFingerprint:
    """Rigorous hardware and runtime execution environment snapshot."""
    machine_id: str
    os_name: str
    os_version: str
    architecture: str
    cpu_model: str
    cpu_count: int
    memory_total_bytes: int
    python_version: str
    python_compiler: str
    package_versions: Dict[str, str]
    git_commit_sha: str
    git_branch: str
    repository_url: str
    author: str
    random_seed: Optional[int] = None
    dataset_version: Optional[str] = None
    model_version: Optional[str] = None
    config_hash: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "machine_id": self.machine_id,
            "os_name": self.os_name,
            "os_version": self.os_version,
            "architecture": self.architecture,
            "cpu_model": self.cpu_model,
            "cpu_count": self.cpu_count,
            "memory_total_bytes": self.memory_total_bytes,
            "python_version": self.python_version,
            "python_compiler": self.python_compiler,
            "package_versions": self.package_versions,
            "git_commit_sha": self.git_commit_sha,
            "git_branch": self.git_branch,
            "repository_url": self.repository_url,
            "author": self.author,
            "random_seed": self.random_seed,
            "dataset_version": self.dataset_version,
            "model_version": self.model_version,
            "config_hash": self.config_hash,
        }


@dataclass
class ProvEntity:
    """W3C PROV Entity representation."""
    entity_id: str
    label: str
    attributes: Dict[str, Any]
    generated_at_time: float = field(default_factory=time.time)
    was_derived_from_ids: List[str] = field(default_factory=list)
    was_generated_by_id: Optional[str] = None
    was_attributed_to_id: Optional[str] = None


@dataclass
class ProvActivity:
    """W3C PROV Activity representation."""
    activity_id: str
    label: str
    start_time: float
    end_time: float
    used_entity_ids: List[str] = field(default_factory=list)
    was_associated_with_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ProvAgent:
    """W3C PROV Agent representation."""
    agent_id: str
    name: str
    agent_type: str  # "Person", "SoftwareAgent", "Organization"
    acted_on_behalf_of_id: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EvidenceNode:
    """
    Immutable node in the scientific evidence lineage graph.
    Every node is a Merkle vertex containing its payload hash and parent hashes.
    """
    node_id: str
    stage: LineageStage
    name: str
    description: str
    payload: Dict[str, Any]
    parent_node_ids: List[str]
    parent_hashes: List[str]
    environment: EnvironmentFingerprint
    quality_level: EvidenceQualityLevel
    algorithm: HashAlgorithm = HashAlgorithm.SHA256
    created_at_epoch: float = field(default_factory=time.time)
    node_hash: str = field(init=False)

    def __post_init__(self):
        # Calculate Merkle node hash combining payload, environment, and parent hashes
        content_to_hash = {
            "node_id": self.node_id,
            "stage": self.stage.value,
            "name": self.name,
            "description": self.description,
            "payload": self.payload,
            "parent_hashes": sorted(self.parent_hashes),
            "environment": self.environment.canonical_dict(),
            "quality_level": self.quality_level.value,
            "created_at_epoch": self.created_at_epoch,
        }
        self.node_hash = ProvenanceHasher.hash_canonical_json(content_to_hash, algorithm=self.algorithm)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "node_id": self.node_id,
            "stage": self.stage.value,
            "name": self.name,
            "description": self.description,
            "payload": self.payload,
            "parent_node_ids": self.parent_node_ids,
            "parent_hashes": self.parent_hashes,
            "node_hash": self.node_hash,
            "environment": self.environment.canonical_dict(),
            "quality_level": self.quality_level.value,
            "quality_weight": self.quality_level.numeric_weight,
            "algorithm": self.algorithm.value,
            "created_at_epoch": self.created_at_epoch,
        }
