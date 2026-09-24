"""
Phase 3P: Base Evidence Collector.
"""

from abc import ABC

from ..domain.interfaces import IEvidenceCollector


class BaseEvidenceCollector(IEvidenceCollector, ABC):
    """Base class providing common collection utilities for verification domains."""
    pass
