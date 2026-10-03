"""
Enterprise Dataset Card Specification for Scientific Benchmarks.
Complies with HuggingFace, MLCommons, and ACM Artifact guidelines:
- Dataset origin, license, collection methodology
- Annotation protocol & Inter-Annotator Agreement (IAA)
- Difficulty distribution & ground truth verification
- Known biases, limitations, and ethical considerations
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


@dataclass
class AnnotationProtocol:
    """Guidelines and procedures used during ground truth creation."""

    annotator_count: int
    primary_guideline: str
    adjudication_procedure: str
    inter_annotator_agreement_kappa: float
    quality_control_checks: List[str]


@dataclass
class DatasetCard:
    """Standardized metadata specification for a research dataset."""

    dataset_name: str
    domain: str  # Healthcare, Legal, Finance, Insurance, Government, etc.
    version: str  # e.g. "1.0.0"
    license_type: str  # e.g. "CC-BY-4.0", "Apache-2.0", "Enterprise-Proprietary"
    origin_organization: str
    collection_process: str
    sample_count: int
    difficulty_distribution: Dict[str, float]  # {"EASY": 0.4, "MEDIUM": 0.4, "HARD": 0.2}
    annotation_protocol: AnnotationProtocol
    known_biases: List[str]
    known_limitations: List[str]
    ethical_considerations: str
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "dataset_name": self.dataset_name,
            "domain": self.domain,
            "version": self.version,
            "license": self.license_type,
            "origin": self.origin_organization,
            "collection_process": self.collection_process,
            "sample_count": self.sample_count,
            "difficulty_distribution": self.difficulty_distribution,
            "annotation": asdict(self.annotation_protocol),
            "known_biases": self.known_biases,
            "known_limitations": self.known_limitations,
            "ethical_considerations": self.ethical_considerations,
            "created_at": self.created_at,
        }
