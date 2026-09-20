"""
Shared Kernel Governance Rules and Invariant Checker.
Ensures that the Shared Kernel remains minimal, framework-independent, domain-independent, and strictly governed.
"""
from typing import List, Set

FORBIDDEN_DEPENDENCY_PATTERNS = {
    "fastapi", "sqlalchemy", "redis", "celery", "temporal",
    "docker", "google.genai", "google.cloud", "openai", "opentelemetry"
}

FORBIDDEN_DOMAIN_CONCEPTS = {
    "VerificationDefinition", "DatasetRecord", "EvidenceArtifact",
    "MetricValue", "QualityGatePolicy", "VerificationCertificate",
    "AuditLedgerEntry"
}

class SharedKernelGovernancePolicy:
    """Architectural Governance Policy for Shared Kernel additions."""
    @staticmethod
    def is_dependency_allowed(module_import_path: str) -> bool:
        for forbidden in FORBIDDEN_DEPENDENCY_PATTERNS:
            if forbidden in module_import_path.lower():
                return False
        return True

    @staticmethod
    def is_concept_allowed(class_name: str) -> bool:
        return class_name not in FORBIDDEN_DOMAIN_CONCEPTS
