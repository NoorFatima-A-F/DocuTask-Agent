"""CLI Client Configuration and Runner."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from ..sdk.python.client import GovernanceClient


class CLIConfig:
    """Manages CLI configuration and profiles."""

    def __init__(self, config_path: Optional[str] = None) -> None:
        default_path = Path.home() / ".doctask" / "governance_config.json"
        self.config_file = Path(config_path) if config_path else default_path
        self._data: Dict[str, Any] = self._load()

    def _load(self) -> Dict[str, Any]:
        if self.config_file.exists():
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save(self) -> None:
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2)

    @property
    def api_key(self) -> Optional[str]:
        return os.environ.get("DOCTASK_GOVERNANCE_API_KEY") or self._data.get("api_key", "default_cli_key")

    @api_key.setter
    def api_key(self, value: str) -> None:
        self._data["api_key"] = value

    @property
    def base_url(self) -> str:
        return os.environ.get("DOCTASK_GOVERNANCE_URL") or self._data.get("base_url", "https://api.governance.doctask.io")

    def get_client(self) -> GovernanceClient:
        return GovernanceClient(api_key=self.api_key or "default_cli_key", base_url=self.base_url)
