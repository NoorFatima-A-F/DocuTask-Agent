"""
Evidence Requirement Model
==========================
Defines required SLSA provenance level, raw telemetry bindings, and cryptographic signing requirements.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class EvidenceRequirement:
    """Specifies evidence depth, SLSA provenance tier, and cryptographic requirements."""
    target_quality_level: str = "LEVEL_A"  # LEVEL_A to LEVEL_E
    min_slsa_level: int = 3
    require_merkle_dag_lineage: bool = True
    require_w3c_prov_export: bool = True
    require_digital_signatures: bool = True
    require_independent_replay: bool = False
    required_artifact_types: List[str] = field(default_factory=lambda: ["SVG_CHART", "LATEX_TABLE", "CSV", "PARQUET"])
