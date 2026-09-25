"""Provenance Integrity and Builder Identity Verification."""
from typing import Optional, Set
from .builder import SLSAProvenanceStatement


class ProvenanceVerifier:
    """Verifies that provenance matches trusted source repositories and builder identities."""

    def __init__(
        self,
        trusted_repos: Optional[Set[str]] = None,
        trusted_builders: Optional[Set[str]] = None,
        min_slsa_level: int = 2,
    ):
        self.trusted_repos = trusted_repos or {"github.com/docutask/ai-document-platform"}
        self.trusted_builders = trusted_builders or {"https://github.com/docutask/actions/runner@v1"}
        self.min_slsa_level = min_slsa_level

    def verify_provenance(self, provenance: Optional[SLSAProvenanceStatement]) -> bool:
        if not provenance:
            return False
        if provenance.slsa_level < self.min_slsa_level:
            return False
        if provenance.source_repo not in self.trusted_repos:
            return False
        if provenance.builder_id not in self.trusted_builders:
            return False
        return True
