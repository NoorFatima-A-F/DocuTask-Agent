"""
Phase 3P: Base Evidence Collector.
"""

from abc import ABC, abstractmethod
from typing import List

from ..domain.interfaces import IEvidenceCollector
from ..domain.models import StandardizedEvidenceItem


class BaseEvidenceCollector(IEvidenceCollector, ABC):
    """Base class providing common collection utilities for verification domains."""
    pass
