"""Readiness Evidence Repository Manager (3H.3.12.3).

Organizes readiness evidence into versioned and structured directories:
- readiness_evidence/
- readiness_evidence/runs/YYYY-MM-DD-runXXX/
"""

import os
from datetime import datetime, timezone


class EvidenceRepositoryManager:
    """Manages creation and paths of structured run-based evidence storage."""

    def __init__(self, base_dir: str = "readiness_evidence"):
        self.base_dir = base_dir

    def create_run_directory(self) -> str:
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        run_id = "run001"
        run_path = os.path.join(self.base_dir, "runs", f"{date_str}-{run_id}")
        os.makedirs(run_path, exist_ok=True)
        os.makedirs(self.base_dir, exist_ok=True)
        return run_path

    def get_base_directory(self) -> str:
        os.makedirs(self.base_dir, exist_ok=True)
        return self.base_dir
