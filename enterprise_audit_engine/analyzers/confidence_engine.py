"""Deterministic Confidence & Evidence Classification Engine."""

from typing import List, Set
from ..domain.evidence.models import (
    EvidenceClassification,
    EvidenceConfidence,
    EvidenceRecord,
    EvidenceSourceType,
)


class ConfidenceEngine:
    """Calculates deterministic confidence level based on multi-source evidence depth."""

    @staticmethod
    def calculate_confidence(records: List[EvidenceRecord]) -> EvidenceConfidence:
        """Determines confidence from the set of evidence source types."""
        if not records:
            return EvidenceConfidence.NONE

        source_types: Set[EvidenceSourceType] = {r.source_type for r in records}

        # Highest tier: Runtime Execution
        if EvidenceSourceType.RUNTIME_EXECUTION in source_types:
            return EvidenceConfidence.VERY_HIGH

        # High tier: Both Static Source and Automated Test Execution
        if (
            EvidenceSourceType.STATIC_SOURCE_CODE in source_types
            and EvidenceSourceType.AUTOMATED_TEST_EXECUTION in source_types
        ):
            return EvidenceConfidence.HIGH

        # High tier: Automated Test Execution alone with pass status
        if EvidenceSourceType.AUTOMATED_TEST_EXECUTION in source_types:
            return EvidenceConfidence.HIGH

        # Medium tier: Static Source Code inspection
        if EvidenceSourceType.STATIC_SOURCE_CODE in source_types:
            return EvidenceConfidence.MEDIUM

        # Low tier: Configuration or Documentation only
        if EvidenceSourceType.CONFIGURATION_FILE in source_types:
            return EvidenceConfidence.LOW

        return EvidenceConfidence.LOW

    @staticmethod
    def classify_subsystem(records: List[EvidenceRecord]) -> EvidenceClassification:
        """Determines subsystem maturity strictly bounded by the weakest required link."""
        if not records:
            return EvidenceClassification.NOT_VERIFIED

        # Check for critical errors or test failures
        for r in records:
            if r.classification == EvidenceClassification.CRITICAL_FINDING:
                return EvidenceClassification.CRITICAL_FINDING
            if r.exit_code is not None and r.exit_code != 0:
                return EvidenceClassification.PARTIALLY_VERIFIED

        source_types = {r.source_type for r in records}

        if EvidenceSourceType.RUNTIME_EXECUTION in source_types:
            return EvidenceClassification.VERIFIED_BY_EXECUTION

        if (
            EvidenceSourceType.STATIC_SOURCE_CODE in source_types
            and EvidenceSourceType.AUTOMATED_TEST_EXECUTION in source_types
        ):
            return EvidenceClassification.VERIFIED

        if EvidenceSourceType.AUTOMATED_TEST_EXECUTION in source_types:
            return EvidenceClassification.VERIFIED

        if EvidenceSourceType.STATIC_SOURCE_CODE in source_types:
            return EvidenceClassification.VERIFIED_BY_STATIC_ANALYSIS

        if EvidenceSourceType.CONFIGURATION_FILE in source_types:
            return EvidenceClassification.CONFIGURATION_PRESENT_RUNTIME_NOT_VERIFIED

        return EvidenceClassification.EVIDENCE_FOUND
