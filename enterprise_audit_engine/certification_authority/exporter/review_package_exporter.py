"""External Auditor Review Package Exporter."""

import json
import shutil
from pathlib import Path
from typing import Dict, Any, List
from enterprise_audit_engine.certification_authority.domain.models import CertificationRecord


class ExternalReviewPackageExporter:
    """Packages certified audit artifacts into a portable bundle for external auditors."""

    @classmethod
    def export_review_package(
        cls,
        output_dir: Path,
        record: CertificationRecord,
        public_key_pem: str,
        evidence_dir: Path,
        reports_dir: Path,
        merkle_manifest_path: Path,
    ) -> Dict[str, Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        created_paths: Dict[str, Path] = {}

        # 1. Certificate and Public Key
        cert_file = output_dir / "certificate.json"
        with open(cert_file, "w", encoding="utf-8") as fp:
            json.dump(record.model_dump(), fp, indent=2, sort_keys=True)
        created_paths["certificate.json"] = cert_file

        pub_file = output_dir / "public_key.pem"
        pub_file.write_text(public_key_pem or record.public_key_pem, encoding="utf-8")
        created_paths["public_key.pem"] = pub_file

        # 2. Manifest and Merkle Root
        if merkle_manifest_path.exists():
            merkle_dest = output_dir / "merkle_root.json"
            shutil.copy2(merkle_manifest_path, merkle_dest)
            created_paths["merkle_root.json"] = merkle_dest

        manifest_src = evidence_dir / "audit_manifest.json"
        if manifest_src.exists():
            manifest_dest = output_dir / "evidence_manifest.json"
            shutil.copy2(manifest_src, manifest_dest)
            created_paths["evidence_manifest.json"] = manifest_dest

        # 3. Selected Evidence Directory
        selected_evidence_dir = output_dir / "selected_evidence"
        selected_evidence_dir.mkdir(exist_ok=True)
        for ev_file in evidence_dir.glob("EV-*.json"):
            shutil.copy2(ev_file, selected_evidence_dir / ev_file.name)
        created_paths["selected_evidence"] = selected_evidence_dir

        # 4. Reports Directory
        reports_dest_dir = output_dir / "reports"
        reports_dest_dir.mkdir(exist_ok=True)
        for rpt in reports_dir.glob("*.md"):
            shutil.copy2(rpt, reports_dest_dir / rpt.name)
        created_paths["reports"] = reports_dest_dir

        # 5. Verification Instructions
        instructions_file = output_dir / "verification_instructions.md"
        instructions_text = f"""# External Auditor Verification Instructions

## Overview
This package contains cryptographically signed audit evidence and certification for **{record.system_name} (Release {record.release_version})**.
Third-party auditors can independently verify all claims, signatures, and evidence integrity without access to the source code repository.

## Step 1: Verify Digital Signature & Certificate Integrity
Run the standalone verifier CLI against the signed certificate and public key:
```bash
python -m enterprise_audit_engine.cli.main verify-certificate \\
    --certificate certificate.json \\
    --public-key public_key.pem \\
    --merkle-manifest merkle_root.json
```

## Step 2: Validate Cryptographic Merkle Root
Verify that the `merkle_root` inside `certificate.json` matches the root calculated in `merkle_root.json`.

- **Expected Merkle Root**: `{record.merkle_root}`
- **Evidence Quality Index (EQI)**: `{record.eqi_score} / 100`
- **Certification Status**: `{record.status.value}`
- **Expiry Date**: `{record.expiry_timestamp}`

## Step 3: Inspect Raw Evidence & Findings
All individual evidence records supporting every report statement are archived in `selected_evidence/`.
Inspect the executive and technical due diligence reports in `reports/`.
"""
        instructions_file.write_text(instructions_text, encoding="utf-8")
        created_paths["verification_instructions.md"] = instructions_file

        return created_paths
