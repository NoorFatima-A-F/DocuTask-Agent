"""
Dataset Security & Poisoning Scanner.
Scans samples for malicious payload injections, malware signatures, and poisoned prompts.
"""
from typing import List, Tuple
from app.platform_verification.dataset_governance.domain.models import DatasetSample


class DatasetSecurityScanner:
    def scan_samples(self, samples: List[DatasetSample]) -> Tuple[bool, List[str]]:
        threats: List[str] = []
        poison_signatures = ["<script>", "javascript:", "eval(", "rm -rf", "__import__('os')"]

        for s in samples:
            for sig in poison_signatures:
                if sig in s.content:
                    threats.append(f"Security threat detected in sample '{s.sample_id}': contains '{sig}'")

        is_clean = len(threats) == 0
        return is_clean, threats


dataset_security_scanner = DatasetSecurityScanner()
