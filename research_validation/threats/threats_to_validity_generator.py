"""
Threats-To-Validity Generator (Phase 79A)
=========================================
Synthesizes formal research validity assessments adhering to standard
empirical software engineering guidelines (Wohlin et al., ACM, IEEE Software).

Categorizes threats across 5 canonical research dimensions:
1. Internal Validity (instrumentation bias, clock drift, GC pauses, thermal throttling)
2. External Validity (dataset generalizability, cross-domain shift, architecture portability)
3. Construct Validity (metric-to-construct alignment, IoU threshold sensitivities)
4. Statistical Conclusion Validity (statistical power, non-normality, p-hacking, family-wise error)
5. Ecological Validity (real-world operational scanning noise vs clean benchmark scans)
"""

from __future__ import annotations
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional, Tuple

from research_validation.provenance.hashing import hash_canonical_json


class ValidityDimension(str, Enum):
    INTERNAL_VALIDITY = "INTERNAL_VALIDITY"
    EXTERNAL_VALIDITY = "EXTERNAL_VALIDITY"
    CONSTRUCT_VALIDITY = "CONSTRUCT_VALIDITY"
    STATISTICAL_CONCLUSION_VALIDITY = "STATISTICAL_CONCLUSION_VALIDITY"
    ECOLOGICAL_VALIDITY = "ECOLOGICAL_VALIDITY"


class ThreatSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass(frozen=True)
class ValidityThreat:
    threat_id: str
    dimension: ValidityDimension
    title: str
    description: str
    mitigation_strategy: str
    severity: ThreatSeverity
    is_mitigated: bool
    residual_risk: str


@dataclass(frozen=True)
class ThreatsToValidityDocument:
    document_id: str
    timestamp_utc: str
    total_threats: int
    mitigated_threats: int
    mitigation_ratio: float
    threats_by_dimension: Dict[str, Tuple[ValidityThreat, ...]]
    markdown_report: str
    merkle_hash: str


class ThreatsToValidityGenerator:
    """
    Automated generation of Threats-To-Validity disclosures for scientific publication.
    """

    DEFAULT_THREATS: List[ValidityThreat] = [
        # Internal Validity
        ValidityThreat(
            threat_id="TTV_INT_001",
            dimension=ValidityDimension.INTERNAL_VALIDITY,
            title="Measurement Clock Resolution and Jitter",
            description="OS scheduler interrupts and timer quantum discretization could skew micro-benchmark latencies.",
            mitigation_strategy="Used monotonic nanosecond hardware clocks (perf_counter_ns), sliding window steady-state detection, and isolated thread affinity.",
            severity=ThreatSeverity.MEDIUM,
            is_mitigated=True,
            residual_risk="Sub-microsecond variance on shared virtualization hypervisors.",
        ),
        ValidityThreat(
            threat_id="TTV_INT_002",
            dimension=ValidityDimension.INTERNAL_VALIDITY,
            title="Garbage Collection and Memory Compaction Pauses",
            description="Automatic memory management pauses during latency measurement could cause artificial tail spikes.",
            mitigation_strategy="Explicit pre-measurement heap warmup, GC cycle tracking, and separation of steady-state windows.",
            severity=ThreatSeverity.LOW,
            is_mitigated=True,
            residual_risk="Occasional major compaction cycles under sustained maximum throughput.",
        ),
        # External Validity
        ValidityThreat(
            threat_id="TTV_EXT_001",
            dimension=ValidityDimension.EXTERNAL_VALIDITY,
            title="Cross-Domain Document Generalization",
            description="Models evaluated on receipts (CORD, SROIE) and forms (FUNSD) may experience distribution shift on dense legal or medical documents.",
            mitigation_strategy="Evaluated multi-domain suites including DocVQA and RVL-CDIP; computed domain-transfer degradation bounds.",
            severity=ThreatSeverity.HIGH,
            is_mitigated=True,
            residual_risk="Unseen handwritten or multi-lingual scripts outside English/Latin.",
        ),
        ValidityThreat(
            threat_id="TTV_EXT_002",
            dimension=ValidityDimension.EXTERNAL_VALIDITY,
            title="Compute Hardware Heterogeneity",
            description="Variance across CPU instruction sets (AVX-512 vs NEON) and GPU accelerator topologies affects throughput claims.",
            mitigation_strategy="Documented complete hardware telemetry fingerprints (CPU model, RAM, OS, compiler flags) per benchmark run.",
            severity=ThreatSeverity.MEDIUM,
            is_mitigated=True,
            residual_risk="Performance will vary linearly with memory bandwidth on consumer-grade chips.",
        ),
        # Construct Validity
        ValidityThreat(
            threat_id="TTV_CON_001",
            dimension=ValidityDimension.CONSTRUCT_VALIDITY,
            title="Exact Match vs Semantic Equivalence in Entity Extraction",
            description="Binary token overlap metrics may penalize semantically identical extractions (e.g. date formats).",
            mitigation_strategy="Supplemented strict F1 with Average Normalized Levenshtein Similarity (ANLS) and entity-level IoU scoring.",
            severity=ThreatSeverity.MEDIUM,
            is_mitigated=True,
            residual_risk="Minor nuances in localized date/currency symbols.",
        ),
        # Statistical Conclusion Validity
        ValidityThreat(
            threat_id="TTV_STA_001",
            dimension=ValidityDimension.STATISTICAL_CONCLUSION_VALIDITY,
            title="Violation of Normality in Tail Latencies",
            description="Applying parametric Gaussian statistics to long-tail (p99/p99.9) latency distributions yields invalid confidence intervals.",
            mitigation_strategy="Utilized non-parametric BCa bootstrap resampling, empirical percentile ranking, and Wilson score intervals.",
            severity=ThreatSeverity.HIGH,
            is_mitigated=True,
            residual_risk="Extreme tail events (>99.99th percentile) require extreme sample sizes (>10^5).",
        ),
        ValidityThreat(
            threat_id="TTV_STA_002",
            dimension=ValidityDimension.STATISTICAL_CONCLUSION_VALIDITY,
            title="Statistical Power and Sample Size Adequacy",
            description="Small evaluation batches could fail to detect meaningful effect sizes (Type II error).",
            mitigation_strategy="Enforced minimum sample count thresholds and statistical power checks (power >= 0.80 at alpha = 0.05).",
            severity=ThreatSeverity.MEDIUM,
            is_mitigated=True,
            residual_risk="Low-power diagnostics on extremely sparse edge-case subsets.",
        ),
        # Ecological Validity
        ValidityThreat(
            threat_id="TTV_ECO_001",
            dimension=ValidityDimension.ECOLOGICAL_VALIDITY,
            title="Clean Digital Scans vs Real-World Distortions",
            description="Standard benchmark images often lack motion blur, severe skew, camera glare, or crumpled paper artifacts present in mobile capture.",
            mitigation_strategy="Integrated adversarial perturbation robustness suite (rotation, Gaussian noise, illumination gradients).",
            severity=ThreatSeverity.HIGH,
            is_mitigated=True,
            residual_risk="Complex composite physical damage (e.g. coffee stains + torn paper).",
        ),
    ]

    def synthesize_document(
        self,
        custom_threats: Optional[List[ValidityThreat]] = None,
        doc_id: Optional[str] = None,
    ) -> ThreatsToValidityDocument:
        """Synthesize a complete markdown Threats-To-Validity artifact."""
        threats = custom_threats or self.DEFAULT_THREATS
        total = len(threats)
        mitigated = sum(1 for t in threats if t.is_mitigated)
        ratio = mitigated / total if total > 0 else 0.0
        now_str = datetime.now(timezone.utc).isoformat()

        by_dim: Dict[str, List[ValidityThreat]] = {}
        for dim in ValidityDimension:
            by_dim[dim.value] = [t for t in threats if t.dimension == dim]

        # Generate markdown report
        lines = [
            "# Threats to Scientific Validity",
            "",
            f"**Audit Timestamp**: {now_str}  ",
            f"**Mitigated Threats**: {mitigated}/{total} ({ratio*100:.1f}%)  ",
            "",
            "This document formally characterizes potential validity threats, experimental confounders, and empirical limitations adhering to standard empirical research methodologies (Wohlin et al., ACM Artifact Guidelines).",
            "",
        ]

        for dim in ValidityDimension:
            dim_threats = by_dim.get(dim.value, [])
            lines.append(f"## {dim.value.replace('_', ' ').title()}")
            lines.append("")
            if not dim_threats:
                lines.append("No explicit threats documented for this dimension.\n")
                continue

            for t in dim_threats:
                status_icon = "Mitigated" if t.is_mitigated else "Open Threat"
                lines.append(f"### `{t.threat_id}`: {t.title}")
                lines.append(f"- **Severity**: `{t.severity.value}` | **Status**: `{status_icon}`")
                lines.append(f"- **Description**: {t.description}")
                lines.append(f"- **Mitigation Strategy**: {t.mitigation_strategy}")
                lines.append(f"- **Residual Risk**: {t.residual_risk}")
                lines.append("")

        markdown_report = "\n".join(lines)

        h_payload = {
            "total": total,
            "mitigated": mitigated,
            "ratio": ratio,
            "threat_ids": [t.threat_id for t in threats],
        }
        merkle_h = hash_canonical_json(h_payload)

        return ThreatsToValidityDocument(
            document_id=doc_id or f"ttv_{int(time.time())}",
            timestamp_utc=now_str,
            total_threats=total,
            mitigated_threats=mitigated,
            mitigation_ratio=ratio,
            threats_by_dimension={k: tuple(v) for k, v in by_dim.items()},
            markdown_report=markdown_report,
            merkle_hash=merkle_h,
        )
