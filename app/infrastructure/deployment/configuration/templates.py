"""Configuration Templates and Environment Variable Interpolation."""

from dataclasses import dataclass
import re
from typing import Any, Dict


@dataclass
class ConfigTemplate:
    """A parameterized configuration template."""
    template_id: str
    name: str
    template_string: str  # e.g. "MAX_WORKERS=${MAX_WORKERS:-4}\nDATABASE_URL=${DB_URL}"
    environment: str = "default"

    def render(self, variables: Dict[str, Any]) -> str:
        """Substitute variables into the template string with fallback defaults."""
        pattern = r"\$\{([A-Za-z0-9_]+)(?::-([^}]+))?\}"

        def replace(match: re.Match) -> str:
            var_name = match.group(1)
            default_val = match.group(2) or ""
            return str(variables.get(var_name, default_val))

        return re.sub(pattern, replace, self.template_string)
