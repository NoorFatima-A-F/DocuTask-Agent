"""
Semantic Versioning and Version Models.
Standardizes version management across artifacts, schemas, configurations, datasets, and plugins.
"""
from dataclasses import dataclass
from typing import Optional, Tuple
import re

SEMVER_REGEX = re.compile(
    r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
    r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
    r"(?:\+(?P<buildmetadata>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
)

@dataclass(frozen=True)
class SemanticVersion:
    """Immutable Semantic Versioning (SemVer 2.0.0) implementation."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    def __str__(self) -> str:
        res = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            res += f"-{self.prerelease}"
        if self.build:
            res += f"+{self.build}"
        return res

    def __repr__(self) -> str:
        return f"SemanticVersion({str(self)!r})"

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        match = SEMVER_REGEX.match(version_str.strip())
        if not match:
            raise ValueError(f"Invalid Semantic Version string: {version_str}")
        groups = match.groupdict()
        return cls(
            major=int(groups["major"]),
            minor=int(groups["minor"]),
            patch=int(groups["patch"]),
            prerelease=groups.get("prerelease"),
            build=groups.get("buildmetadata")
        )

    def _sort_key(self) -> Tuple[int, int, int, int, str]:
        # Prereleases sort lower than normal releases
        has_pre = 0 if self.prerelease else 1
        return (self.major, self.minor, self.patch, has_pre, self.prerelease or "")

    def __lt__(self, other: "SemanticVersion") -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._sort_key() < other._sort_key()

    def __le__(self, other: "SemanticVersion") -> bool:
        return self == other or self < other

    def __gt__(self, other: "SemanticVersion") -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented
        return self._sort_key() > other._sort_key()

    def __ge__(self, other: "SemanticVersion") -> bool:
        return self == other or self > other

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return False
        return (self.major, self.minor, self.patch, self.prerelease) == (other.major, other.minor, other.patch, other.prerelease)

    def is_compatible_with(self, other: "SemanticVersion") -> bool:
        """Major version breaking rule."""
        if self.major != other.major:
            return False
        return self >= other

    def bump_patch(self) -> "SemanticVersion":
        return SemanticVersion(self.major, self.minor, self.patch + 1)

    def bump_minor(self) -> "SemanticVersion":
        return SemanticVersion(self.major, self.minor + 1, 0)

    def bump_major(self) -> "SemanticVersion":
        return SemanticVersion(self.major + 1, 0, 0)

@dataclass(frozen=True)
class VersionModel:
    semver: SemanticVersion
    label: Optional[str] = None

@dataclass(frozen=True)
class SchemaVersion(VersionModel):
    pass

@dataclass(frozen=True)
class ArtifactVersion(VersionModel):
    pass

@dataclass(frozen=True)
class ModelVersion(VersionModel):
    pass

@dataclass(frozen=True)
class ConfigurationVersion(VersionModel):
    pass

@dataclass(frozen=True)
class DatasetVersion(VersionModel):
    pass

@dataclass(frozen=True)
class PluginVersion(VersionModel):
    pass

@dataclass(frozen=True)
class EnvironmentVersion(VersionModel):
    pass
