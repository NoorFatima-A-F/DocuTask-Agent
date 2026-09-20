"""CLI Entrypoint for Enterprise Audit Engine."""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from ..orchestration.audit_runner import AuditRunner
from ..domain.evidence.models import AuditReportManifest
from ..governance.integrity_verifier import EvidenceIntegrityVerifier


def parse_args():
    parser = argparse.ArgumentParser(description="Enterprise Audit Engine: Automated Due Diligence Platform")
    subparsers = parser.add_subparsers(dest="subcommand", help="Audit subcommands")

    # Command: run-all
    run_parser = subparsers.add_parser("run-all", help="Execute all evidence collectors and generate reports")
    run_parser.add_argument("--repo-root", type=str, default=".", help="Path to repository root")
    run_parser.add_argument("--output-dir", type=str, default="audit_output", help="Directory for output evidence and reports")

    # Command: verify-enterprise
    ent_parser = subparsers.add_parser("verify-enterprise", help="Run full enterprise due diligence verification and gate audit")
    ent_parser.add_argument("--repo-root", type=str, default=".", help="Path to repository root")
    ent_parser.add_argument("--output-dir", type=str, default="audit_output", help="Directory for output evidence and reports")

    # Command: verify-integrity
    integ_parser = subparsers.add_parser("verify-integrity", help="Verify evidence store cryptographic hashes against manifest")
    integ_parser.add_argument("--output-dir", type=str, default="audit_output", help="Directory containing evidence and manifest")

    # Command: verify-gate
    gate_parser = subparsers.add_parser("verify-gate", help="Check if evidence meets minimum release gates")
    gate_parser.add_argument("--repo-root", type=str, default=".", help="Path to repository root")
    gate_parser.add_argument("--output-dir", type=str, default="audit_output", help="Directory for output evidence and reports")

    return parser.parse_args()


def main():
    args = parse_args()
    if not args.subcommand:
        args.subcommand = "verify-enterprise"

    repo_root = Path(getattr(args, "repo_root", ".")).resolve()
    output_dir = Path(getattr(args, "output_dir", "audit_output")).resolve()

    if args.subcommand == "verify-integrity":
        evidence_dir = output_dir / "audit-evidence"
        manifest_file = evidence_dir / "audit_manifest.json"
        if not manifest_file.exists():
            print(f"[-] Manifest not found at {manifest_file}. Run an audit first.")
            sys.exit(1)

        with open(manifest_file, "r", encoding="utf-8") as fp:
            manifest_data = json.load(fp)
            manifest = AuditReportManifest(**manifest_data)

        res = EvidenceIntegrityVerifier.verify_store_integrity(evidence_dir, manifest)
        print("\n[*] Evidence Store Integrity Verification:")
        print(f"    - Status:          {res['status']}")
        print(f"    - Valid Records:   {res['valid_count']} / {res['total_expected']}")
        print(f"    - Tampered Records: {res['tampered_count']}")
        print(f"    - Missing Records:  {res['missing_count']}")

        if not res["is_intact"]:
            print(f"\n[-] Critical Integrity Violations Detected: {res['tampered_details']}")
            sys.exit(1)
        else:
            print("\n[+] Integrity Verified: All evidence records match cryptographically sealed SHA-256 hashes.")
            sys.exit(0)

    runner = AuditRunner(repo_root=repo_root, output_dir=output_dir)

    print(f"[*] Starting Enterprise Evidence Verification for: {repo_root}")
    results = asyncio.run(runner.run_full_audit())

    print("\n[+] Verification Run Complete!")
    print(f"    - Audit Run ID:              {results['run_id']}")
    print(f"    - Total Evidence Collected:  {results['total_evidence']}")
    print(f"    - Subsystem Classification:  {results['overall_classification']}")
    print(f"    - Evidence Confidence:       {results['overall_confidence']}")
    print(f"    - Reports Directory:         {results['reports_dir']}")
    print(f"    - Evidence Directory:        {results['evidence_dir']}\n")

    if args.subcommand in {"verify-gate", "verify-enterprise"}:
        if results["overall_classification"] in {"CRITICAL_FINDING", "EVIDENCE_INSUFFICIENT"}:
            print("[-] Gate Check: FAILED (Release blocked due to critical findings or insufficient evidence)")
            sys.exit(1)
        else:
            print("[+] Gate Check: PASSED (Enterprise Due Diligence Verified)")
            sys.exit(0)


if __name__ == "__main__":
    main()
