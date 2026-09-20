"""
Delivery Policies & Modes.
Defines DeliveryMode (AT_MOST_ONCE, AT_LEAST_ONCE, EXACTLY_ONCE) and DeliveryPolicy models.
"""

from enum import Enum
from pydantic import BaseModel, Field


class DeliveryMode(str, Enum):
    """Messaging delivery guarantee modes."""
    AT_MOST_ONCE = "AT_MOST_ONCE"
    AT_LEAST_ONCE = "AT_LEAST_ONCE"
    EXACTLY_ONCE = "EXACTLY_ONCE"


class DeliveryPolicy(BaseModel):
    """Delivery policy specification."""

    mode: DeliveryMode = Field(default=DeliveryMode.AT_LEAST_ONCE)
    ordered_delivery: bool = Field(default=False)
    delayed_delivery_seconds: float = Field(default=0.0, ge=0.0)
    model_config = {"frozen": True}
