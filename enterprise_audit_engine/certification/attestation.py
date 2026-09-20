"""Audit Engine Version Attestation & Engine Manifest Generator."""

import hashlib
import json
import os
import sys
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any


class EngineAttestation:
    """Provides immutable version attestation and build provenance for the audit engine."""

    ENGINE_VERSION = "2.1.0"

    @classmethod
    def get_git_commit(cls, repo_root: Path) -> str:
        try:
            res = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=str(repo_root),
                capture_output=True,
                text=True,
                timeout=5,
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except Exception:
            pass
        return "HEAD"

    @classmethod
    def compute_dependencies_hash(cls, repo_root: Path) -> str:
        req_file = repo_root / "requirements.txt"
        if req_file.exists():
            try:
                content = req_file.read_bytes()
                return hashlib.sha256(content).hexdigest()
            except Exception:
                pass
        return "sha256-unpinned"

    @classmethod
    def generate_build_info(cls, repo_root: Path) -> Dict[str, Any]:
        commit = cls.get_git_commit(repo_root)
        deps_hash = cls.compute_dependencies_hash(repo_root)
        
        info = {
            "engine_version": cls.ENGINE_VERSION,
            "git_commit": commit,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            "dependencies_hash": deps_hash,
            "build_timestamp": datetime.now(timezone.utc).isoformat(),
            "configuration_hash": hashlib.sha256(f"{cls.ENGINE_VERSION}-{commit}".encode("utf-8")).hexdigest(),
        }
        return info

    @classmethod
    def save_attestation_files(cls, engine_dir: Path, repo_root: Path) -> Dict[str, Path]:
        build_info = cls.generate_build_info(repo_root)
        
        build_info_path = engine_dir / "BUILD_INFO.json"
        manifest_path = engine_dir / "ENGINE_MANIFEST.json"
        version_path = engine_dir / "VERSION"

        with open(version_path, "w", encoding="utf-8") as fp:
            fp.write(cls.ENGINE_VERSION + "\n")

        with open(build_info_path, "w", encoding="utf-8") as fp:
            json.dump(build_info, fp, indent=2, sort_keys=True)

        engine_manifest = {
            "engine_name": "enterprise_audit_engine",
            "version": cls.ENGINE_VERSION,
            "attestation": build_info,
            "capabilities": [
                "deterministic_reproducibility",
                "merkle_evidence_sealing",
                "anti_hallucination_validation",
                "collector_contract_verification",
                "tampering_detection",
                "release_evidence_packaging",
            ],
            "manifest_hash": hashlib.sha256(json.dumps(build_info, sort_keys=True).encode("utf-8")).hexdigest(),
        }

        with open(manifest_path, "w", encoding="utf-8") as fp:
            json.dump(engine_manifest, fp, indent=2, sort_keys=True)

        return {
            "version": version_path,
            "build_info": build_info_path,
            "engine_manifest": manifest_path,
        }
