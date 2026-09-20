"""
Provenance & Runtime Environment Manifest Generator
"""
import sys
import os
import platform
import hashlib
from app.platform_verification.domain.models import RuntimeEnvironmentProfile

class ProvenanceTracker:
    @staticmethod
    def capture_environment_profile(
        model_name: str = "gemini-2.5-flash",
        prompt_content: str = "DocuTask Standard Extraction System Prompt v1.0",
        config_dict: dict = None
    ) -> RuntimeEnvironmentProfile:
        config_bytes = str(sorted((config_dict or {}).items())).encode("utf-8")
        config_hash = hashlib.sha256(config_bytes).hexdigest()[:16]
        prompt_hash = hashlib.sha256(prompt_content.encode("utf-8")).hexdigest()[:16]

        return RuntimeEnvironmentProfile(
            host_os=f"{platform.system()} {platform.release()} ({platform.machine()})",
            python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
            git_commit=os.getenv("GIT_COMMIT_SHA", "e7f8c92a-main-verified"),
            app_version="1.0.0-phase13.23",
            hardware_summary={
                "cpu_count": os.cpu_count() or 4,
                "architecture": platform.architecture()[0]
            },
            active_model_name=model_name,
            prompt_hash=prompt_hash,
            config_hash=config_hash
        )

provenance_tracker = ProvenanceTracker()
