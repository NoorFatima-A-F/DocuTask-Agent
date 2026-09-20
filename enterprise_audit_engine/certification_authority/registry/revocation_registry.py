"""Certification Revocation Registry & CRL Manager."""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from enterprise_audit_engine.certification_authority.domain.models import (
    CertificationRecord,
    CertificationStatus,
    RevocationRecord,
    RevocationReason,
)


class CertificationRevocationRegistry:
    """Manages the Certificate Revocation List (CRL) and revocation lifecycles."""

    def __init__(self, registry_root: Path):
        self.registry_root = registry_root
        self.revocations_file = self.registry_root / "revocations.json"
        self._ensure_registry()

    def _ensure_registry(self):
        if not self.revocations_file.exists():
            self.registry_root.mkdir(parents=True, exist_ok=True)
            with open(self.revocations_file, "w", encoding="utf-8") as fp:
                json.dump([], fp)

    def load_revocations(self) -> List[RevocationRecord]:
        if not self.revocations_file.exists():
            return []
        with open(self.revocations_file, "r", encoding="utf-8") as fp:
            data = json.load(fp)
            return [RevocationRecord.model_validate(item) for item in data]

    def is_revoked(self, certificate_id: str) -> bool:
        records = self.load_revocations()
        return any(r.certificate_id == certificate_id for r in records)

    def get_revocation(self, certificate_id: str) -> Optional[RevocationRecord]:
        records = self.load_revocations()
        for r in records:
            if r.certificate_id == certificate_id:
                return r
        return None

    def revoke_certificate(
        self,
        certificate_id: str,
        reason: RevocationReason,
        details: str,
        revoked_by: str = "Enterprise-Audit-Certification-Authority",
    ) -> RevocationRecord:
        """Issues a revocation record and appends it to the registry."""
        rec = RevocationRecord(
            certificate_id=certificate_id,
            revocation_timestamp=datetime.now(timezone.utc).isoformat(),
            reason=reason,
            details=details,
            revoked_by=revoked_by,
            signature=f"REVOKED-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        )
        existing = self.load_revocations()
        # Remove any existing revocation for the same id if updating
        existing = [r for r in existing if r.certificate_id != certificate_id]
        existing.append(rec)

        with open(self.revocations_file, "w", encoding="utf-8") as fp:
            json.dump([r.model_dump() for r in existing], fp, indent=2, sort_keys=True)

        return rec
