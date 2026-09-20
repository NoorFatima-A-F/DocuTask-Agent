"""
Security Evidence Collector.
Persists structured attack payloads, request/response records, audit logs, and security telemetry.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone
from ..domain.models import AttackPayload, SecurityFinding, SecurityScorecard


class SecurityEvidenceCollector:
    """Collects, indexes, and seals security test artifacts and attack evidence."""

    def __init__(self, base_evidence_dir: str = "security_evidence"):
        self.base_dir = Path(base_evidence_dir)
        self.attacks_dir = self.base_dir / "attacks"
        self.passed_dir = self.base_dir / "passed_tests"
        self.failed_dir = self.base_dir / "failed_tests"
        self.logs_dir = self.base_dir / "logs"
        self.reports_dir = self.base_dir / "reports"

    def initialize_directories(self) -> None:
        """Creates the required security evidence directory hierarchy."""
        for d in [self.base_dir, self.attacks_dir, self.passed_dir, self.failed_dir, self.logs_dir, self.reports_dir]:
            d.mkdir(parents=True, exist_ok=True)

    def record_attack_evidence(self, attack: AttackPayload, response_data: Dict[str, Any], defended: bool) -> str:
        """Records an individual attack payload and its defensive interception trace."""
        self.initialize_directories()
        target_dir = self.passed_dir if defended else self.failed_dir
        filename = f"{attack.payload_id}_{attack.category.value.lower()}.json"
        target_path = target_dir / filename

        record = {
            "payload_id": attack.payload_id,
            "category": attack.category.value,
            "severity": attack.severity.value,
            "target_component": attack.target_component,
            "raw_payload": attack.raw_payload,
            "expected_action": attack.expected_action,
            "response": response_data,
            "defended": defended,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(record, f, indent=2)

        return str(target_path)

    def export_evidence_package(self, scorecard: SecurityScorecard) -> Dict[str, Any]:
        """Exports the full evidence suite including summary, pillar logs, and SHA-256 checksum manifest."""
        self.initialize_directories()
        generated_files: List[Path] = []

        # 1. Export summary scorecard
        summary_path = self.reports_dir / "security_scorecard.json"
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(scorecard.to_dict(), f, indent=2)
        generated_files.append(summary_path)

        # 2. Export individual pillar evidence files
        for pillar_name, pillar_res in scorecard.pillars.items():
            pillar_path = self.logs_dir / f"{pillar_name.lower()}_evidence.json"
            with open(pillar_path, "w", encoding="utf-8") as f:
                json.dump(pillar_res.to_dict(), f, indent=2)
            generated_files.append(pillar_path)

        # 3. Create SHA-256 Manifest
        manifest_data = {
            "timestamp": scorecard.timestamp,
            "program": "Phase V9 — Enterprise AI Security Validation & Adversarial Assurance Program (EA-SVAAP)",
            "composite_score": scorecard.composite_score,
            "grade": scorecard.grade,
            "production_ready": scorecard.production_ready,
            "critical_vulnerabilities": scorecard.critical_vulnerabilities,
            "total_assertions": scorecard.total_assertions,
            "passed_assertions": scorecard.passed_assertions,
            "checksums": {},
        }

        for path in generated_files:
            with open(path, "rb") as f:
                digest = hashlib.sha256(f.read()).hexdigest()
            manifest_data["checksums"][path.name] = digest

        manifest_path = self.base_dir / "manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2)

        return {
            "evidence_dir": str(self.base_dir),
            "manifest_file": str(manifest_path),
            "summary_scorecard": str(summary_path),
            "total_files": len(generated_files) + 1,
        }
