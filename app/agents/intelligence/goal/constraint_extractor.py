"""Constraint Extractor for Autonomous Agent Platform.

Extracts operational constraints such as SLA thresholds, minimum accuracy,
budget caps, compliance frameworks (SOX, GDPR, HIPAA), and output formats.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExtractedConstraints:
    """Structured constraints extracted from goal description and context."""

    min_accuracy: float = 0.90
    max_latency_seconds: Optional[float] = None
    cost_budget_usd: Optional[float] = None
    compliance_frameworks: List[str] = field(default_factory=list)
    require_human_review: bool = False
    output_format: str = "JSON"
    max_retries: int = 3
    pii_redaction: bool = False
    custom_rules: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "min_accuracy": self.min_accuracy,
            "max_latency_seconds": self.max_latency_seconds,
            "cost_budget_usd": self.cost_budget_usd,
            "compliance_frameworks": self.compliance_frameworks,
            "require_human_review": self.require_human_review,
            "output_format": self.output_format,
            "max_retries": self.max_retries,
            "pii_redaction": self.pii_redaction,
            "custom_rules": self.custom_rules,
        }


class ConstraintExtractor:
    """Extracts operational constraints using deterministic regex and schema inference."""

    def __init__(self) -> None:
        self._accuracy_pattern = re.compile(
            r"(?:accuracy|precision|confidence)\s*(?:>=|>|of|at least)?\s*(\d+(?:\.\d+)?)\s*(?:%|percent)",
            re.IGNORECASE,
        )
        self._accuracy_ratio_pattern = re.compile(
            r"(?:accuracy|precision|confidence)\s*(?:>=|>|of|at least)?\s*(0\.\d+)",
            re.IGNORECASE,
        )
        self._sla_pattern = re.compile(
            r"(?:sla|within|latency|time limit|deadline|under)\s*(?:of|under|<=|<)?\s*(\d+(?:\.\d+)?)\s*(milliseconds|ms|seconds|sec|s|minutes|min|m)",
            re.IGNORECASE,
        )
        self._cost_pattern = re.compile(
            r"(?:budget\s*(?:cap)?|cost|max cost|price limit)\s*(?:<=|<|under|of)?\s*\$?\s*(\d+(?:\.\d+)?)",
            re.IGNORECASE,
        )
        self._format_pattern = re.compile(
            r"\b(json|csv|xml|pdf|parquet|markdown)\b",
            re.IGNORECASE,
        )

    def extract(self, text: str, context: Optional[Dict[str, Any]] = None) -> ExtractedConstraints:
        """Extract all constraints from text and optional context parameters."""
        constraints = ExtractedConstraints()

        if text:
            # Parse accuracy
            acc_pct = self._accuracy_pattern.search(text)
            if acc_pct:
                val = float(acc_pct.group(1)) / 100.0
                constraints.min_accuracy = max(0.1, min(1.0, val))
            else:
                acc_ratio = self._accuracy_ratio_pattern.search(text)
                if acc_ratio:
                    val = float(acc_ratio.group(1))
                    constraints.min_accuracy = max(0.1, min(1.0, val))

            # Parse SLA / latency
            sla = self._sla_pattern.search(text)
            if sla:
                val = float(sla.group(1))
                unit = sla.group(2).lower()
                if unit in ("s", "sec", "seconds"):
                    constraints.max_latency_seconds = val
                elif unit in ("m", "min", "minutes"):
                    constraints.max_latency_seconds = val * 60.0
                elif unit in ("ms", "milliseconds"):
                    constraints.max_latency_seconds = val / 1000.0

            # Parse cost
            cost = self._cost_pattern.search(text)
            if cost:
                constraints.cost_budget_usd = float(cost.group(1))

            # Parse format
            fmt = self._format_pattern.search(text)
            if fmt:
                constraints.output_format = fmt.group(1).upper()

            # Parse compliance flags
            upper_text = text.upper()
            for standard in ["SOX", "GDPR", "HIPAA", "PCI-DSS", "SOC2", "ISO27001"]:
                if standard in upper_text and standard not in constraints.compliance_frameworks:
                    constraints.compliance_frameworks.append(standard)

            # Parse human review requirement
            if any(w in upper_text for w in ["HUMAN IN THE LOOP", "HUMAN REVIEW", "APPROVAL REQUIRED", "MANUAL CHECK"]):
                constraints.require_human_review = True

            # Parse PII redaction
            if any(w in upper_text for w in ["PII", "REDACT", "MASK SENSITIVE", "ANONYMIZE", "PRIVACY"]):
                constraints.pii_redaction = True

        # Context overrides take ultimate precedence
        if context:
            if "min_accuracy" in context:
                constraints.min_accuracy = float(context["min_accuracy"])
            if "max_latency_seconds" in context:
                constraints.max_latency_seconds = float(context["max_latency_seconds"])
            if "cost_budget_usd" in context:
                constraints.cost_budget_usd = float(context["cost_budget_usd"])
            if "compliance_frameworks" in context:
                constraints.compliance_frameworks = list(set(constraints.compliance_frameworks + context["compliance_frameworks"]))
            if "require_human_review" in context:
                constraints.require_human_review = bool(context["require_human_review"])
            if "output_format" in context:
                constraints.output_format = str(context["output_format"]).upper()
            if "pii_redaction" in context:
                constraints.pii_redaction = bool(context["pii_redaction"])

        return constraints
