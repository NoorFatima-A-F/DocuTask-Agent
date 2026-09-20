"""Versioned Configuration Management (Req 48, 49)."""
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional
import hashlib
import uuid


@dataclass
class VersionedConfiguration:
    """Immutable, versioned configuration release artifact (Req 48)."""
    config_id: str
    version: str
    environment: str
    checksum: str
    owner: str
    settings: Dict[str, Any]
    approved: bool = False
    effective_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def create(
        cls,
        version: str,
        environment: str,
        settings: Dict[str, Any],
        owner: str = "platform-team",
    ) -> "VersionedConfiguration":
        cfg_str = str(sorted(settings.items())).encode("utf-8")
        chk = f"sha256:{hashlib.sha256(cfg_str).hexdigest()}"
        return cls(
            config_id=f"cfg-{uuid.uuid4().hex[:8]}",
            version=version,
            environment=environment,
            checksum=chk,
            owner=owner,
            settings=settings,
        )
