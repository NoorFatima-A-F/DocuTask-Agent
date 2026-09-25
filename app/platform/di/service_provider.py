"""Service Provider Interface."""

from __future__ import annotations

from app.platform.di.container import (
    DIContainer,
    ServiceProvider,
    global_di_container,
)

__all__ = ["DIContainer", "ServiceProvider", "global_di_container"]
