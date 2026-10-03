"""Golden Baseline System Manager."""

import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from enterprise_audit_engine.baseline.baseline_manifest import (
    GoldenBaselineManifest,
    PolicyBaseline,
    RuleBaseline,
)
from enterprise_audit_engine.certification_authority.policy.policy_engine import CertificationPolicyEngine


class GoldenBaselineManager:
    """Manages baseline snapshots and compares current engine state against approved baselines."""

    def __init__(self, baseline_root: Path):
        self.baseline_root = baseline_root
        self.baseline_root.mkdir(parents=True, exist_ok=True)

    def create_baseline(self, version: str, engine_root: Path) -> GoldenBaselineManifest:
        """Captures and persists an immutable Golden Baseline for a version."""
        version_dir = self.baseline_root / version
        version_dir.mkdir(parents=True, exist_ok=True)

        # 1. Compute file hashes
        file_hashes: Dict[str, str] = {}
        for root, dirs, files in os.walk(engine_root):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache", "tests"}]
            for f in files:
                if f.endswith((".py", ".json", ".yaml", ".yml")) and not f.startswith("."):
                    fp = Path(root) / f
                    rel_p = fp.relative_to(engine_root).as_posix()
                    try:
                        file_hashes[rel_p] = hashlib.sha256(fp.read_bytes()).hexdigest()
                    except Exception:
                        pass

        engine_source_hash = hashlib.sha256(
            ":".join(f"{k}:{v}" for k, v in sorted(file_hashes.items())).encode("utf-8")
        ).hexdigest()

        # 2. Extract policy baselines
        policy_baselines = {}
        for p_name, rules in CertificationPolicyEngine.DEFAULT_POLICIES.items():
            policy_baselines[p_name] = PolicyBaseline(
                policy_name=p_name,
                minimum_confidence=rules.get("minimum_confidence", "HIGH"),
                required_domains=rules.get("required_domains", []),
                forbidden_critical_findings=rules.get("forbidden_critical_findings", True),
                minimum_eqi=rules.get("minimum_eqi", 85.0),
            )

        # 3. Extract rule baselines
        rule_baselines = [
            RuleBaseline(rule_name="config_only", expected_classification="CONFIGURATION_PRESENT", required_evidence_type="CONFIGURATION_FILE"),
            RuleBaseline(rule_name="static_only", expected_classification="VERIFIED_BY_STATIC_ANALYSIS", required_evidence_type="STATIC_SOURCE_CODE"),
            RuleBaseline(rule_name="runtime_verified", expected_classification="VERIFIED_BY_EXECUTION", required_evidence_type="RUNTIME_EXECUTION"),
        ]

        manifest = GoldenBaselineManifest(
            baseline_version=version,
            engine_version="2.1.0",
            engine_source_hash=engine_source_hash,
            policies=policy_baselines,
            rules=rule_baselines,
            file_hashes=file_hashes,
        )

        manifest_path = version_dir / "baseline_manifest.json"
        with open(manifest_path, "w", encoding="utf-8") as fp:
            json.dump(manifest.model_dump(), fp, indent=2, sort_keys=True)

        return manifest

    def load_baseline(self, version: str) -> Optional[GoldenBaselineManifest]:
        manifest_path = self.baseline_root / version / "baseline_manifest.json"
        if not manifest_path.exists():
            return None
        with open(manifest_path, "r", encoding="utf-8") as fp:
            return GoldenBaselineManifest.model_validate(json.load(fp))

    def compare_against_baseline(self, version: str, engine_root: Path) -> Dict[str, Any]:
        """Compares current engine files and rules against the Golden Baseline."""
        baseline = self.load_baseline(version)
        if not baseline:
            return {
                "matched": False,
                "error": f"Golden baseline for version '{version}' not found.",
            }

        added_files = []
        modified_files = []
        removed_files = []
        weakened_rules = []

        # Current file hashes
        current_hashes: Dict[str, str] = {}
        for root, dirs, files in os.walk(engine_root):
            dirs[:] = [d for d in dirs if d not in {"__pycache__", ".pytest_cache", "tests"}]
            for f in files:
                if f.endswith((".py", ".json", ".yaml", ".yml")) and not f.startswith("."):
                    fp = Path(root) / f
                    rel_p = fp.relative_to(engine_root).as_posix()
                    try:
                        current_hashes[rel_p] = hashlib.sha256(fp.read_bytes()).hexdigest()
                    except Exception:
                        pass

        for p, b_hash in baseline.file_hashes.items():
            if p not in current_hashes:
                removed_files.append(p)
            elif current_hashes[p] != b_hash:
                modified_files.append(p)

        for p in current_hashes:
            if p not in baseline.file_hashes:
                added_files.append(p)

        # Policy checks
        for p_name, b_pol in baseline.policies.items():
            curr_pol = CertificationPolicyEngine.DEFAULT_POLICIES.get(p_name)
            if not curr_pol:
                weakened_rules.append(f"Policy '{p_name}' was removed entirely.")
            else:
                if curr_pol.get("minimum_eqi", 0.0) < b_pol.minimum_eqi:
                    weakened_rules.append(f"Policy '{p_name}' minimum EQI lowered from {b_pol.minimum_eqi} to {curr_pol.get('minimum_eqi')}.")
                if b_pol.forbidden_critical_findings and not curr_pol.get("forbidden_critical_findings", True):
                    weakened_rules.append(f"Policy '{p_name}' allowed critical findings (previously forbidden).")

        matched = (len(modified_files) == 0 and len(removed_files) == 0 and len(weakened_rules) == 0)

        return {
            "matched": matched,
            "baseline_version": version,
            "added_files_count": len(added_files),
            "added_files": added_files,
            "modified_files_count": len(modified_files),
            "modified_files": modified_files,
            "removed_files_count": len(removed_files),
            "removed_files": removed_files,
            "weakened_rules_count": len(weakened_rules),
            "weakened_rules": weakened_rules,
            "status": "BASELINE_VERIFIED" if matched else "BASELINE_DISCREPANCIES_FOUND",
        }
