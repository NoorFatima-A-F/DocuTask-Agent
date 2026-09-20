"""
Enterprise Configuration Loader.
Loads configuration from files (YAML/JSON), environment, or cloud dictionaries.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from .schema import ConfigSource
from .provider import ConfigurationProvider


class ConfigurationLoader:
    """Loads and populates configuration layers into the ConfigurationProvider."""

    def __init__(self, provider: ConfigurationProvider):
        self.provider = provider

    def load_from_dict(self, source: ConfigSource, data: Dict[str, Any]) -> None:
        """Flatten nested dict and load into the specified layer."""
        flattened = self._flatten_dict(data)
        self.provider.set_layer_values(source, flattened)

    def load_from_json_file(self, file_path: str, source: ConfigSource = ConfigSource.YAML_FILE) -> None:
        """Load configuration from a JSON file."""
        path = Path(file_path)
        if not path.exists():
            return
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.load_from_dict(source, data)

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = "", sep: str = ".") -> Dict[str, Any]:
        """Recursively flatten nested dictionary keys."""
        items: Dict[str, Any] = {}
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.update(self._flatten_dict(v, new_key, sep=sep))
            else:
                items[new_key] = v
        return items
