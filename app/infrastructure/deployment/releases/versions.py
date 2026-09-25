"""Semantic Versioning, Compatibility, and Changelog Models."""

from dataclasses import dataclass
import re
from typing import Optional


@dataclass
class ReleaseVersion:
    """Semantic version (SemVer 2.0.0)."""
    major: int
    minor: int
    patch: int
    prerelease: Optional[str] = None
    build: Optional[str] = None

    @classmethod
    def parse(cls, version_str: str) -> "ReleaseVersion":
        """Parse semver string e.g. '1.2.3-rc.1+build.42'."""
        pattern = r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.-]+))?(?:\+([0-9A-Za-z.-]+))?$"
        match = re.match(pattern, version_str.strip())
        if not match:
            raise ValueError(f"Invalid SemVer string: {version_str}")

        major, minor, patch, prerelease, build = match.groups()
        return cls(
            major=int(major),
            minor=int(minor),
            patch=int(patch),
            prerelease=prerelease,
            build=build,
        )

    def is_backward_compatible_with(self, previous: "ReleaseVersion") -> bool:
        """Major version change breaks backward compatibility."""
        return self.major == previous.major

    def __str__(self) -> str:
        s = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            s += f"-{self.prerelease}"
        if self.build:
            s += f"+{self.build}"
        return s
