"""
Hermetic Verification Context Factory and Workspace Sandbox Manager.
"""
from __future__ import annotations
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from app.platform_verification.test_harness.domain.models import VerificationContext


class VerificationContextManager:
    """Creates isolated workspace directories for every verification execution."""

    @staticmethod
    def create_context(
        test_id: str,
        environment: str = "staging",
        dataset_version: str = "v1.0.0",
        model_version: str = "gemini-1.5-pro",
        base_dir: Optional[Path] = None,
    ) -> VerificationContext:
        exec_id = f"exec_{uuid.uuid4().hex[:10]}"
        root = (base_dir or Path(tempfile.gettempdir())) / "docutask_verification" / exec_id

        input_d = root / "input"
        output_d = root / "output"
        logs_d = root / "logs"
        traces_d = root / "traces"
        metrics_d = root / "metrics"
        evidence_d = root / "evidence"

        for d in [input_d, output_d, logs_d, traces_d, metrics_d, evidence_d]:
            d.mkdir(parents=True, exist_ok=True)

        return VerificationContext(
            execution_id=exec_id,
            test_id=test_id,
            environment=environment,
            dataset_version=dataset_version,
            model_version=model_version,
            config_hash=uuid.uuid5(uuid.NAMESPACE_DNS, f"{test_id}_{dataset_version}").hex[:16],
            start_time=datetime.now(timezone.utc).isoformat(),
            workspace_root=root,
            input_dir=input_d,
            output_dir=output_d,
            logs_dir=logs_d,
            traces_dir=traces_d,
            metrics_dir=metrics_d,
            evidence_dir=evidence_d,
        )

    @staticmethod
    def cleanup_context(context: VerificationContext) -> None:
        """Cleans up temporary files if workspace exists."""
        if context.workspace_root.exists() and not context.is_cleaned_up:
            shutil.rmtree(context.workspace_root, ignore_errors=True)
            context.is_cleaned_up = True
