"""
Software Bill of Materials (SBOM) Generator (CycloneDX 1.5 and SPDX 2.3).
"""
import hashlib
import json
from typing import Dict, Any
from app.platform_verification.config_versioning.domain.models import SBOMManifest
from app.platform_verification.config_versioning.core.dependency_registry import dependency_registry

class SBOMGenerator:
    @staticmethod
    def generate_cyclonedx_sbom() -> SBOMManifest:
        deps = dependency_registry.list_dependencies()
        direct_count = sum(1 for d in deps if d.is_direct)
        transitive_count = len(deps) - direct_count

        raw_payload = json.dumps([d.model_dump() for d in deps], sort_keys=True, default=str).encode("utf-8")
        bom_hash = hashlib.sha256(raw_payload).hexdigest()

        return SBOMManifest(
            format="CycloneDX_1.5",
            spec_version="1.5",
            components_count=len(deps),
            direct_dependencies_count=direct_count,
            transitive_dependencies_count=transitive_count,
            components=deps,
            sha256_bom_hash=bom_hash
        )

    @staticmethod
    def generate_spdx_sbom() -> SBOMManifest:
        deps = dependency_registry.list_dependencies()
        direct_count = sum(1 for d in deps if d.is_direct)
        transitive_count = len(deps) - direct_count

        raw_payload = json.dumps([d.model_dump() for d in deps], sort_keys=True, default=str).encode("utf-8")
        bom_hash = hashlib.sha256(raw_payload).hexdigest()

        return SBOMManifest(
            format="SPDX_2.3",
            spec_version="2.3",
            components_count=len(deps),
            direct_dependencies_count=direct_count,
            transitive_dependencies_count=transitive_count,
            components=deps,
            sha256_bom_hash=bom_hash
        )

    @staticmethod
    def export_cyclonedx_json() -> Dict[str, Any]:
        manifest = SBOMGenerator.generate_cyclonedx_sbom()
        return {
            "bomFormat": "CycloneDX",
            "specVersion": manifest.spec_version,
            "serialNumber": manifest.serial_number,
            "version": 1,
            "metadata": {
                "timestamp": manifest.timestamp,
                "tools": [{"name": "DocuTask Enterprise SBOM Generator", "version": "2.0.0"}],
                "component": {
                    "name": "DocuTask Agent Enterprise Platform",
                    "version": "2.0.0",
                    "type": "application"
                }
            },
            "components": [
                {
                    "name": c.name,
                    "version": c.version,
                    "type": "library" if c.category.value == "PYTHON_PACKAGE" else "application",
                    "purl": f"pkg:pypi/{c.name}@{c.version}",
                    "licenses": [{"license": {"id": c.license}}]
                }
                for c in manifest.components
            ]
        }

sbom_generator = SBOMGenerator()
