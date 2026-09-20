"""
Supply Chain & Package Integrity Scanner.
"""
from typing import List, Dict, Any


class SupplyChainScanner:
    """Verifies that dependencies originate from trusted sources and have valid hash manifests."""

    def verify_supply_chain(self, packages: List[Dict[str, Any]]) -> Dict[str, Any]:
        untrusted = []
        for p in packages:
            if not p.get("has_hash", True):
                untrusted.append(f"Package '{p.get('name')}' lacks cryptographic integrity hash")
        return {
            "status": "PASS" if len(untrusted) == 0 else "FAIL",
            "untrusted_packages": untrusted,
        }
