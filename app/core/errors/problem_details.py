"""
RFC 9457 Problem Details Specification.
Standardized API error response format.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
import uuid


@dataclass
class ProblemDetails:
    """RFC 9457 Compliant Problem Details Structure."""
    type: str = "about:blank"
    title: str = "An error occurred"
    status: int = 500
    detail: Optional[str] = None
    instance: Optional[str] = None
    error_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    invalid_params: List[Dict[str, Any]] = field(default_factory=list)
    extensions: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to RFC 9457 JSON response dictionary."""
        d = {
            "type": self.type,
            "title": self.title,
            "status": self.status,
            "error_id": self.error_id,
            "timestamp": self.timestamp.isoformat(),
        }
        if self.detail:
            d["detail"] = self.detail
        if self.instance:
            d["instance"] = self.instance
        if self.invalid_params:
            d["invalid_params"] = self.invalid_params
        if self.extensions:
            d.update(self.extensions)
        return d
