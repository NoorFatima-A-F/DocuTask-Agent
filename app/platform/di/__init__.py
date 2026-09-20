"""Dependency Injection Package (Phase 9 AAPEROS)."""

from app.platform.di.container import (
    DIContainer,
    ServiceProvider,
    global_di_container,
)

__all__ = ["DIContainer", "ServiceProvider", "global_di_container"]
