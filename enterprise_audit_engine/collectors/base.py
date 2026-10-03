"""Abstract Base Collector for Audit Engine."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List
from ..domain.evidence.models import EvidenceRecord


class BaseCollector(ABC):
    """Abstract collector enforcing consistent evidence generation."""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the collector."""
        pass

    @property
    @abstractmethod
    def category(self) -> str:
        """Category of collected evidence."""
        pass

    @abstractmethod
    async def collect(self) -> List[EvidenceRecord]:
        """Executes collection and returns structured evidence records."""
        pass
