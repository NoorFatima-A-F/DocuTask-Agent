"""
Workflow Semantic Versioning.
Provides immutable version models supporting semantic comparison and migration compatibility checks.
"""

from typing import Tuple
from pydantic import BaseModel, Field


class WorkflowVersion(BaseModel):
    """Semantic version (major.minor.patch) representation for workflow definitions."""
    major: int = Field(default=1, ge=0)
    minor: int = Field(default=0, ge=0)
    patch: int = Field(default=0, ge=0)

    @classmethod
    def parse(cls, version_str: str) -> "WorkflowVersion":
        """Parses version string like '1.2.3'."""
        parts = version_str.strip().split(".")
        if len(parts) != 3:
            return cls(major=1, minor=0, patch=0)
        return cls(major=int(parts[0]), minor=int(parts[1]), patch=int(parts[2]))

    def to_string(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}"

    def is_backward_compatible_with(self, older: "WorkflowVersion") -> bool:
        """Major version bumps indicate breaking changes; identical major indicates compatibility."""
        return self.major == older.major and (self.minor >= older.minor)

    def as_tuple(self) -> Tuple[int, int, int]:
        return (self.major, self.minor, self.patch)

    def __lt__(self, other: "WorkflowVersion") -> bool:
        return self.as_tuple() < other.as_tuple()

    model_config = {"frozen": True}
