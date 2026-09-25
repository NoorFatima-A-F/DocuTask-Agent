"""Semantic Versioning Engine for Artifacts and Releases."""
import re
from functools import total_ordering
from typing import Optional, Tuple


@total_ordering
class ArtifactVersion:
    """Strict SemVer 2.0 parser and comparator."""

    SEMVER_PATTERN = re.compile(
        r"^(?P<major>0|[1-9]\d*)\.(?P<minor>0|[1-9]\d*)\.(?P<patch>0|[1-9]\d*)"
        r"(?:-(?P<prerelease>[0-9A-Za-z.-]+))?"
        r"(?:\+(?P<build>[0-9A-Za-z.-]+))?$"
    )

    def __init__(self, version_str: str):
        self.raw_version = version_str.strip()
        match = self.SEMVER_PATTERN.match(self.raw_version)
        if not match:
            # Fallback for simple single/double digit numbers e.g. "v1.0" or "1.0"
            clean = self.raw_version.lstrip("v")
            parts = clean.split(".")
            if len(parts) == 1 and parts[0].isdigit():
                self.major = int(parts[0])
                self.minor = 0
                self.patch = 0
                self.prerelease: Optional[str] = None
                self.build: Optional[str] = None
            elif len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                self.major = int(parts[0])
                self.minor = int(parts[1])
                self.patch = 0
                self.prerelease = None
                self.build = None
            else:
                raise ValueError(f"Invalid semantic version string: '{version_str}'")
        else:
            self.major = int(match.group("major"))
            self.minor = int(match.group("minor"))
            self.patch = int(match.group("patch"))
            self.prerelease = match.group("prerelease")
            self.build = match.group("build")

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            base += f"-{self.prerelease}"
        if self.build:
            base += f"+{self.build}"
        return base

    def __repr__(self) -> str:
        return f"ArtifactVersion('{str(self)}')"

    def _as_tuple(self) -> Tuple[int, int, int, str]:
        # Pre-release versions have lower precedence than normal versions
        prerelease_key = self.prerelease if self.prerelease is not None else "~"
        return (self.major, self.minor, self.patch, prerelease_key)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, str):
            other = ArtifactVersion(other)
        if not isinstance(other, ArtifactVersion):
            return NotImplemented
        return (self.major, self.minor, self.patch, self.prerelease) == (
            other.major,
            other.minor,
            other.patch,
            other.prerelease,
        )

    def __lt__(self, other: object) -> bool:
        if isinstance(other, str):
            other = ArtifactVersion(other)
        if not isinstance(other, ArtifactVersion):
            return NotImplemented
        if (self.major, self.minor, self.patch) != (other.major, other.minor, other.patch):
            return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)
        
        # When normal version numbers are equal, release without prerelease > release with prerelease
        if self.prerelease is None and other.prerelease is not None:
            return False
        if self.prerelease is not None and other.prerelease is None:
            return True
        return (self.prerelease or "") < (other.prerelease or "")

    def __hash__(self) -> int:
        return hash((self.major, self.minor, self.patch, self.prerelease))

    def bump_patch(self) -> "ArtifactVersion":
        """Returns new ArtifactVersion with incremented patch."""
        return ArtifactVersion(f"{self.major}.{self.minor}.{self.patch + 1}")

    def bump_minor(self) -> "ArtifactVersion":
        """Returns new ArtifactVersion with incremented minor."""
        return ArtifactVersion(f"{self.major}.{self.minor + 1}.0")

    def bump_major(self) -> "ArtifactVersion":
        """Returns new ArtifactVersion with incremented major."""
        return ArtifactVersion(f"{self.major + 1}.0.0")
