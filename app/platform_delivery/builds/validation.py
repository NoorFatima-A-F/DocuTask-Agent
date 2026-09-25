"""Build Validation and Test Evidence Certification."""
from typing import Optional
from .models import BuildResult, TestEvidence


class BuildValidator:
    """Verifies that a build output is completely verified and backed by proof."""

    @classmethod
    def validate_test_evidence(cls, evidence: Optional[TestEvidence]) -> bool:
        """Validates that claims of test success are backed by positive test collection."""
        if not evidence:
            return False
        if evidence.tests_collected <= 0:
            return False
        if evidence.failed > 0:
            return False
        if evidence.passed + evidence.skipped != evidence.tests_collected:
            return False
        return True

    @classmethod
    def validate_build_for_release(cls, build: BuildResult) -> bool:
        """Enforces that build succeeded, has valid digest, and certified test evidence."""
        if not build.success:
            return False
        if not build.artifact_digest or not build.artifact_digest.startswith("sha256:"):
            return False
        if not cls.validate_test_evidence(build.test_evidence):
            return False
        return True
