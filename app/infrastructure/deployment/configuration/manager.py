"""Versioned Configuration Management, Inheritance, and Rollbacks."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import threading



@dataclass
class ConfigurationBundle:
    """A versioned set of configuration key-values."""
    config_id: str
    service_name: str
    environment: str
    version: int
    values: Dict[str, Any]
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True


class ConfigurationManager:
    """Manages versioned configuration sets with inheritance and rollback capabilities."""

    def __init__(self) -> None:
        self._bundles: Dict[str, List[ConfigurationBundle]] = {}  # f"{service}:{env}" -> [ConfigurationBundle]
        self._lock = threading.RLock()

    def set_config(self, service_name: str, environment: str, values: Dict[str, Any]) -> ConfigurationBundle:
        """Create a new configuration version."""
        key = f"{service_name}:{environment}"
        with self._lock:
            existing = self._bundles.get(key, [])
            new_version = len(existing) + 1
            for b in existing:
                b.is_active = False

            bundle = ConfigurationBundle(
                config_id=f"cfg-{key}-{new_version}",
                service_name=service_name,
                environment=environment,
                version=new_version,
                values=values,
                is_active=True,
            )
            self._bundles.setdefault(key, []).append(bundle)
            return bundle

    def get_active_config(self, service_name: str, environment: str) -> Optional[Dict[str, Any]]:
        """Retrieve active configuration values."""
        key = f"{service_name}:{environment}"
        with self._lock:
            existing = self._bundles.get(key, [])
            for b in reversed(existing):
                if b.is_active:
                    return b.values
            return None

    def rollback_config(self, service_name: str, environment: str) -> Optional[ConfigurationBundle]:
        """Rollback configuration to previous version."""
        key = f"{service_name}:{environment}"
        with self._lock:
            existing = self._bundles.get(key, [])
            if len(existing) < 2:
                return None

            active = existing[-1]
            previous = existing[-2]

            active.is_active = False
            previous.is_active = True
            return previous
