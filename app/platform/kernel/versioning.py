"""
Platform Semantic Versioning Specification.
Implements SemVer 2.0.0 parsing, comparison, and version range matching.
"""

from dataclasses import dataclass
import re
from typing import Optional, Tuple


@dataclass(frozen=True, order=True)
class SemanticVersion:
    """Immutable SemVer 2.0.0 implementation."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    _SEMVER_REGEX = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?"
        r"(?:\+(?P<build>[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$"
    )

    @classmethod
    def parse(cls, version_str: str) -> "SemanticVersion":
        """Parse a semver string into a SemanticVersion object."""
        match = cls._SEMVER_REGEX.match(version_str.strip())
        if not match:
            # Fallback for simple '1.0' or single digit '1'
            parts = version_str.strip().split(".")
            try:
                major = int(parts[0])
                minor = int(parts[1]) if len(parts) > 1 else 0
                patch = int(parts[2]) if len(parts) > 2 else 0
                return cls(major=major, minor=minor, patch=patch)
            except Exception:
                raise ValueError(f"Invalid semantic version string: '{version_str}'")

        data = match.groupdict()
        return cls(
            major=int(data["major"]),
            minor=int(data["minor"]),
            patch=int(data["patch"]),
            prerelease=data.get("prerelease"),
            build=data.get("build"),
        )

    def is_compatible_with(self, required: "SemanticVersion") -> bool:
        """Check if this version is backward compatible with required version (SemVer rules)."""
        if self.major != required.major:
            return False
        if self.minor < required.minor:
            return False
        if self.minor == required.minor and self.patch < required.patch:
            return False
        return True

    def __str__(self) -> str:
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            s += f"-{self.prerelease}"
        if self.build:
            s += f"+{self.build}"
        return s


@dataclass(frozen=True)
class VersionRange:
    """Specifies minimum and optional maximum version compatibility bounds."""
    min_version: SemanticVersion
    max_version: Optional[SemanticVersion] = None
    include_min: bool = True
    include_max: bool = True

    def satisfies(self, version: SemanticVersion) -> bool:
        """Check whether a given version satisfies this range."""
        if self.include_min:
            if version < self.min_version:
                return False
        else:
            if version <= self.min_version:
                return False

        if self.max_version:
            if self.include_max:
                if version > self.max_version:
                    return False
            else:
                if version >= self.max_version:
                    return False

        return True

    @classmethod
    def parse(cls, range_str: str) -> "VersionRange":
        """Parse simple range strings like '>=1.0.0,<2.0.0' or '^1.2.0'."""
        range_str = range_str.strip()
        if range_str.startswith("^"):
            base = SemanticVersion.parse(range_str[1:])
            next_major = SemanticVersion(major=base.major + 1, minor=0, patch=0)
            return cls(min_version=base, max_version=next_major, include_min=True, include_max=False)
        elif range_str.startswith(">="):
            base = SemanticVersion.parse(range_str[2:])
            return cls(min_version=base, include_min=True)
        else:
            base = SemanticVersion.parse(range_str)
            return cls(min_version=base, max_version=base, include_min=True, include_max=True)
