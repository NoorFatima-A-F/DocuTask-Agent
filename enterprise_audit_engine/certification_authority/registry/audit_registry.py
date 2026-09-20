"""Historical Audit Registry & Certificate Store."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from enterprise_audit_engine.certification_authority.domain.models import CertificationRecord


class AuditRegistry:
    """Stores and retrieves historical certification records across repository versions."""

    def __init__(self, registry_root: Path):
        self.registry_root = registry_root
        self.certifications_dir = self.registry_root / "certifications"
        self.certifications_dir.mkdir(parents=True, exist_ok=True)

    def register_certificate(self, record: CertificationRecord) -> Path:
        """Stores a certified release record under its semantic version directory."""
        sanitized_version = "".join(c for c in record.release_version if c.isalnum() or c in (".", "-", "_"))
        base_dir = self.certifications_dir.resolve()
        version_dir = (base_dir / sanitized_version).resolve()
        if not (version_dir == base_dir or version_dir.is_relative_to(base_dir)):
            raise ValueError(f"Security violation: Invalid release version path '{record.release_version}'")
        version_dir.mkdir(parents=True, exist_ok=True)
        cert_file = version_dir / "certificate.json"
        
        with open(cert_file, "w", encoding="utf-8") as fp:
            json.dump(record.model_dump(), fp, indent=2, sort_keys=True)
        
        # Also maintain index in registry
        self._update_index(record)
        return cert_file

    def get_certificate(self, release_version: str) -> Optional[CertificationRecord]:
        """Loads a certification record for a specific release version."""
        sanitized_version = "".join(c for c in release_version if c.isalnum() or c in (".", "-", "_"))
        base_dir = self.certifications_dir.resolve()
        cert_file = (base_dir / sanitized_version / "certificate.json").resolve()
        if not (cert_file.is_relative_to(base_dir)):
            raise ValueError(f"Security violation: Invalid release version path '{release_version}'")
        if not cert_file.exists():
            return None
        with open(cert_file, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            return CertificationRecord.model_validate(data)

    def list_versions(self) -> List[str]:
        """Lists all registered release versions."""
        if not self.certifications_dir.exists():
            return []
        versions = []
        for p in self.certifications_dir.iterdir():
            if p.is_dir() and (p / "certificate.json").exists():
                versions.append(p.name)
        return sorted(versions)

    def _update_index(self, record: CertificationRecord):
        index_file = self.registry_root / "registry_index.json"
        index = {}
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as fp:
                    index = json.load(fp)
            except Exception:
                index = {}
        
        index[record.release_version] = {
            "certificate_id": record.certificate_id,
            "issued_timestamp": record.issued_timestamp,
            "expiry_timestamp": record.expiry_timestamp,
            "status": record.status.value,
            "merkle_root": record.merkle_root,
            "eqi_score": record.eqi_score,
            "policy": record.policy_name,
        }
        with open(index_file, "w", encoding="utf-8") as fp:
            json.dump(index, fp, indent=2, sort_keys=True)
