"""
Evidence Exporter and Cryptographic Manifest Generator for Phase V12.
"""

import os
import json
import hashlib
from datetime import datetime, timezone
from typing import Dict, Any, List
from app.certification.reporting.final_report_generator import FinalReportGenerator
from app.certification.portfolio.system_card_generator import SystemCardGenerator


class EvidenceExporter:
    """Exports all Phase V12 JSON datasets, Markdown reports, and SHA-256 manifests."""

    @staticmethod
    def calculate_sha256(file_path: str) -> str:
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    @classmethod
    def export_all_certification_evidence(
        cls,
        base_dir: str,
        phases_summary: List[Any],
        maturity_assessment: Any,
        readiness_score: Any,
        evidence_graph: List[Any],
        risk_register: List[Any],
        governance_audit: Any,
        portfolio_docs: List[Any],
    ) -> Dict[str, Any]:
        docs_dir = os.path.join(base_dir, "docs")
        evidence_dir = os.path.join(base_dir, "certification_evidence")
        os.makedirs(docs_dir, exist_ok=True)
        os.makedirs(evidence_dir, exist_ok=True)

        generated_files = {}

        # 1. Enterprise Score JSON
        score_data = {
            "readiness_score": readiness_score.to_dict() if hasattr(readiness_score, "to_dict") else readiness_score,
            "phases_summary": [p.to_dict() if hasattr(p, "to_dict") else p for p in phases_summary],
        }
        score_path = os.path.join(docs_dir, "phase_V12_enterprise_score.json")
        with open(score_path, "w", encoding="utf-8") as f:
            json.dump(score_data, f, indent=2)
        generated_files["phase_V12_enterprise_score.json"] = score_path

        # 2. Maturity Assessment JSON
        mat_data = maturity_assessment.to_dict() if hasattr(maturity_assessment, "to_dict") else maturity_assessment
        mat_path = os.path.join(docs_dir, "phase_V12_maturity_assessment.json")
        with open(mat_path, "w", encoding="utf-8") as f:
            json.dump(mat_data, f, indent=2)
        generated_files["phase_V12_maturity_assessment.json"] = mat_path

        # 3. Risk Register JSON
        risk_data = {
            "risk_register": [r.to_dict() if hasattr(r, "to_dict") else r for r in risk_register]
        }
        risk_path = os.path.join(docs_dir, "phase_V12_risk_register.json")
        with open(risk_path, "w", encoding="utf-8") as f:
            json.dump(risk_data, f, indent=2)
        generated_files["phase_V12_risk_register.json"] = risk_path

        # 4. Governance Report JSON
        gov_data = governance_audit.to_dict() if hasattr(governance_audit, "to_dict") else governance_audit
        gov_path = os.path.join(docs_dir, "phase_V12_governance_report.json")
        with open(gov_path, "w", encoding="utf-8") as f:
            json.dump(gov_data, f, indent=2)
        generated_files["phase_V12_governance_report.json"] = gov_path

        # 5. Evidence Graph JSON
        graph_data = {
            "evidence_graph": [e.to_dict() if hasattr(e, "to_dict") else e for e in evidence_graph]
        }
        graph_path = os.path.join(docs_dir, "phase_V12_evidence_graph.json")
        with open(graph_path, "w", encoding="utf-8") as f:
            json.dump(graph_data, f, indent=2)
        generated_files["phase_V12_evidence_graph.json"] = graph_path

        # 6. Portfolio Manifest JSON
        port_data = {
            "portfolio_documents": [p.to_dict() if hasattr(p, "to_dict") else p for p in portfolio_docs]
        }
        port_path = os.path.join(docs_dir, "phase_V12_portfolio_manifest.json")
        with open(port_path, "w", encoding="utf-8") as f:
            json.dump(port_data, f, indent=2)
        generated_files["phase_V12_portfolio_manifest.json"] = port_path

        # 7. AI System Card Markdown
        card_content = SystemCardGenerator.generate_system_card_markdown()
        card_path = os.path.join(docs_dir, "phase_V12_system_card.md")
        with open(card_path, "w", encoding="utf-8") as f:
            f.write(card_content)
        generated_files["phase_V12_system_card.md"] = card_path

        # 8. Final Master Assessment Report Markdown
        final_md = FinalReportGenerator.generate_report_markdown(
            phases_summary,
            maturity_assessment,
            readiness_score,
            evidence_graph,
            risk_register,
            governance_audit,
            portfolio_docs,
        )
        report_path = os.path.join(docs_dir, "phase_V12_final_assessment_report.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(final_md)
        generated_files["phase_V12_final_assessment_report.md"] = report_path

        # 9. Cryptographic Manifest JSON
        manifest = {
            "program": "Phase V12 — Enterprise AI Platform Verification Certification & Readiness Assessment Program (EAP-VCRAP)",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "readiness_score": readiness_score.overall_readiness_score,
            "maturity_tier": maturity_assessment.tier_label,
            "grade": readiness_score.grade,
            "artifacts": {},
        }

        for filename, path in generated_files.items():
            manifest["artifacts"][filename] = {
                "path": path,
                "sha256": cls.calculate_sha256(path),
                "size_bytes": os.path.getsize(path),
            }

        manifest_path = os.path.join(evidence_dir, "manifest.json")
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)

        return manifest
