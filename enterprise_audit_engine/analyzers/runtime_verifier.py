"""Runtime Execution & Container Infrastructure Verifier."""

import os
from pathlib import Path
from typing import Dict, Any, List


class RuntimeVerifier:
    """Verifies runtime execution readiness, containerization, orchestration, and health probes."""

    @staticmethod
    def verify_runtime_environment(repo_root: Path) -> Dict[str, Any]:
        has_dockerfile = (repo_root / "Dockerfile").exists() or (repo_root / "docker" / "Dockerfile").exists()
        has_docker_compose = (repo_root / "docker-compose.yml").exists() or (repo_root / "docker-compose.yaml").exists()
        has_k8s = (repo_root / "k8s").exists() or (repo_root / "kubernetes").exists() or (repo_root / "deploy" / "k8s").exists()
        
        # Check healthcheck probe existence in app
        has_health_endpoint = False
        app_dir = repo_root / "app"
        if app_dir.exists():
            for root, _, files in os.walk(app_dir):
                for f in files:
                    if f.endswith(".py"):
                        try:
                            with open(Path(root) / f, "r", encoding="utf-8", errors="ignore") as fp:
                                content = fp.read().lower()
                                if "/health" in content or "def health" in content or "healthcheck" in content:
                                    has_health_endpoint = True
                                    break
                        except Exception:
                            pass
                if has_health_endpoint:
                    break

        # Check production readiness indicators
        has_gunicorn_uvicorn = False
        if has_dockerfile:
            try:
                df_path = repo_root / "Dockerfile" if (repo_root / "Dockerfile").exists() else repo_root / "docker" / "Dockerfile"
                with open(df_path, "r", encoding="utf-8", errors="ignore") as fp:
                    df_content = fp.read().lower()
                    if "uvicorn" in df_content or "gunicorn" in df_content:
                        has_gunicorn_uvicorn = True
            except Exception:
                pass

        runtime_score = 0.0
        if has_dockerfile:
            runtime_score += 25.0
        if has_docker_compose:
            runtime_score += 25.0
        if has_k8s:
            runtime_score += 25.0
        if has_health_endpoint:
            runtime_score += 25.0

        return {
            "has_dockerfile": has_dockerfile,
            "has_docker_compose": has_docker_compose,
            "has_k8s_manifests": has_k8s,
            "has_health_endpoint": has_health_endpoint,
            "has_production_server_configured": has_gunicorn_uvicorn,
            "runtime_readiness_score": runtime_score,
            "readiness_classification": "CONFIGURATION_PRESENT" if runtime_score >= 50.0 else "INSUFFICIENT",
        }
