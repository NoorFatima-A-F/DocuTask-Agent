"""Capability Resolver interface."""

from __future__ import annotations

from app.platform.capability.capability_registry import (
    CapabilityRegistry,
    CapabilityResolver,
    global_capability_registry,
)

__all__ = ["CapabilityResolver", "CapabilityRegistry", "global_capability_registry"]
