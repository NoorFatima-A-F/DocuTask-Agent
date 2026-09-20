"""Standalone External Verifier CLI Entrypoint."""

import argparse
import json
import sys
from pathlib import Path
from enterprise_audit_engine.external_verifier.standalone_verifier import StandaloneExternalVerifier


def main():
    parser = argparse.ArgumentParser(description="Standalone Independent Certificate Verifier (Minimal Computing Base)")
    parser.add_argument("--certificate", type=str, required=True, help="Path to certificate.json")
    parser.add_argument("--public-key", type=str, default=None, help="Optional path to public_key.pem")
    parser.add_argument("--merkle-manifest", type=str, default=None, help="Optional path to merkle_root.json")

    args = parser.parse_args()

    cert_p = Path(args.certificate).resolve()
    pub_p = Path(args.public_key).resolve() if args.public_key else None
    merkle_p = Path(args.merkle_manifest).resolve() if args.merkle_manifest else None

    res = StandaloneExternalVerifier.verify_standalone(cert_p, pub_p, merkle_p)

    print("\n=======================================================")
    print("      INDEPENDENT EXTERNAL AUDITOR VERIFICATION       ")
    print("=======================================================")
    print(f" Status:        {res['status']}")
    print(f" System:        {res.get('system_name', 'N/A')}")
    print(f" Release:       {res.get('release_version', 'N/A')}")
    print(f" EQI Score:     {res.get('eqi_score', 'N/A')} / 100")
    print(f" Signature:     {'VALID (Ed25519)' if res.get('signature_valid') else 'INVALID'}")
    print(f" Merkle Tree:   {'VALID' if res.get('merkle_valid') else 'INVALID'}")
    print(f" Expiration:    {'EXPIRED' if res.get('is_expired') else 'VALID (Active)'}")
    print("=======================================================")

    if not res["is_trusted"]:
        print(f"[-] Verification REJECTED ({res['issues_count']} issues):")
        for i in res.get("issues", []):
            print(f"    - {i}")
        sys.exit(1)
    else:
        print("[+] FINAL: TRUSTED (Independent Verification Succeeded).")
        sys.exit(0)


if __name__ == "__main__":
    main()
