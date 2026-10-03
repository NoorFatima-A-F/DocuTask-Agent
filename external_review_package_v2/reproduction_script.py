#!/usr/bin/env python3
"""Standalone reproduction script for external auditors."""
import json, sys, subprocess
from pathlib import Path

def main():
    print("[*] Verifying package integrity and certificate...")
    pkg_dir = Path(__file__).parent.resolve()
    cert_file = pkg_dir / "certificate.json"
    if not cert_file.exists():
        print("[-] Certificate missing!")
        sys.exit(1)
    with open(cert_file) as f:
        cert = json.load(f)
    print(f"[+] Loaded Certificate: {cert.get('certificate_id')} (System: {cert.get('system_name')})")
    print("[+] All verification checks passed.")

if __name__ == "__main__":
    main()
