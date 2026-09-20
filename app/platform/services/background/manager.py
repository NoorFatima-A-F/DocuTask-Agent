"""
Enterprise Background Service Manager.
Orchestrates scheduled workers, cleanup jobs, maintenance routines, and async platform tasks.
"""

import asyncio
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional
from .models import ServiceDefinition, ServicePriority


class BackgroundServiceManager:
    """Manages scheduled background task execution with priorities, retries, and concurrency control."""

    def __init__(self):
        self._services: Dict[str, ServiceDefinition] = {}
        self._running_tasks: Dict[str, asyncio.Task] = {}
        self._is_running: bool = False

    def register_service(self, service: ServiceDefinition) -> None:
        """Register a background service."""
        self._services[service.name] = service

    def unregister_service(self, name: str) -> None:
        """Unregister a service."""
        self._services.pop(name, None)

    async def execute_service(self, name: str, *args, **kwargs) -> Any:
        """Execute a service once on-demand."""
        service = self._services.get(name)
        if not service:
            raise ValueError(f"Background service '{name}' not found")

        for attempt in range(1, service.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(service.handler):
                    return await asyncio.wait_for(service.handler(*args, **kwargs), timeout=service.timeout_seconds)
                else:
                    return service.handler(*args, **kwargs)
            except Exception as e:
                if attempt == service.max_retries:
                    raise e
                await asyncio.sleep(0.1 * attempt)

    async def start(self) -> None:
        """Start background service runner."""
        self._is_running = True

    async def stop(self) -> None:
        """Stop all running background services."""
        self._is_running = False
        for task in self._running_tasks.values():
            if not task.done():
                task.cancel()
        self._running_tasks.clear()

    def list_services(self) -> List[ServiceDefinition]:
        """List registered background services sorted by priority."""
        return sorted(self._services.values(), key=lambda s: s.priority.value, reverse=True)
