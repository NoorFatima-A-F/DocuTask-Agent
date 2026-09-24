"""Evidence Tampering & Cryptographic Integrity Verifier."""

import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from ..domain.evidence.models import EvidenceRecord, AuditReportManifest


class EvidenceIntegrityVerifier:
    """Detects modified artifacts, tampered hashes, and missing records in the evidence store."""

    @staticmethod
    def verify_record_integrity(record: EvidenceRecord) -> Tuple[bool, str]:
        """Recalculates the SHA-256 fingerprint of an EvidenceRecord and matches against stored hash."""
        recalculated_hash = record.calculate_hash()
        if record.content_hash != recalculated_hash:
            return False, f"Evidence hash mismatch for {record.id}: expected {record.content_hash}, calculated {recalculated_hash}"
        return True, "Valid"

    @classmethod
    def verify_store_integrity(cls, storage_dir: Path, manifest: AuditReportManifest) -> Dict[str, Any]:
        """Audits the entire evidence directory against the sealed manifest."""
        tampered_records: List[str] = []
        missing_records: List[str] = []
        valid_records: List[str] = []

        for expected_hash in manifest.evidence_hashes:
            found = False
            for file_path in storage_dir.glob("EV-*.json"):
                try:
                    with open(file_path, "r", encoding="utf-8") as fp:
                        data = json.load(fp)
                        rec = EvidenceRecord(**data)
                        if rec.content_hash == expected_hash:
                            is_valid, msg = cls.verify_record_integrity(rec)
                            if is_valid:
                                valid_records.append(rec.id)
                                found = True
                            else:
                                tampered_records.append(f"{rec.id}: {msg}")
                                found = True
                            break
                except Exception as ex:
                    tampered_records.append(f"{file_path.name}: Failed to read/parse ({str(ex)})")

            if not found:
                missing_records.append(expected_hash)

        is_intact = len(tampered_records) == 0 and len(missing_records) == 0

        return {
            "is_intact": is_intact,
            "total_expected": len(manifest.evidence_hashes),
            "valid_count": len(valid_records),
            "tampered_count": len(tampered_records),
            "missing_count": len(missing_records),
            "tampered_details": tampered_records,
            "missing_details": missing_records,
            "status": "SEALED_AND_VALID" if is_intact else "CRITICAL_INTEGRITY_VIOLATION",
        }
