"""
Report JSON Schemas and Export Serializers.
"""
from dataclasses import asdict
from typing import Dict, Any
from app.platform_verification.container_verification.models.verification_models import ContainerVerificationEvidencePackage


def serialize_evidence_package(package: ContainerVerificationEvidencePackage) -> Dict[str, Any]:
    return asdict(package)
