"""
ID Generator Interface
======================
Generates strongly typed, unique, and deterministic identifiers for goals, missions, and tasks.
"""

import uuid
from abc import ABC, abstractmethod
from typing import Optional


class IIdGenerator(ABC):
    """Abstract interface for ID generation."""

    @abstractmethod
    def generate_id(self, prefix: str = "") -> str:
        """Generate a unique identifier, optionally with a prefix."""
        raise NotImplementedError


class Uuid4IdGenerator(IIdGenerator):
    """Standard random UUIDv4 identifier generator."""

    def generate_id(self, prefix: str = "") -> str:
        uid = uuid.uuid4().hex[:12]
        return f"{prefix}_{uid}" if prefix else uid


class DeterministicIdGenerator(IIdGenerator):
    """Deterministic sequential counter ID generator for testing and reproduction."""

    def __init__(self, seed_prefix: str = "det"):
        self.seed_prefix = seed_prefix
        self._counter = 0

    def generate_id(self, prefix: str = "") -> str:
        self._counter += 1
        p = prefix or self.seed_prefix
        return f"{p}_{self._counter:06d}"
