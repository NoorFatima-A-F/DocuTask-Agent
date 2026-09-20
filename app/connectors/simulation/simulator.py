"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Simulator.
Enables workflow and multi-agent execution testing without live external APIs, API keys, or networks.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, Optional
from app.connectors.core.models import ExecutionResult

logger = logging.getLogger(__name__)


class ConnectorSimulator:
    """
    Dry-run simulation engine producing deterministic mock outcomes for connector actions.
    """

    def __init__(self):
        # (connector_id, action_name) -> mock_response_dict or callable
        self._mocks: Dict[str, Any] = {}
        self._error_simulations: Dict[str, Exception] = {}

    def _key(self, connector_id: str, action_name: str) -> str:
        return f"{connector_id}:{action_name}"

    def register_mock(
        self,
        connector_id: str,
        action_name: str,
        mock_output: Dict[str, Any] | Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> None:
        """Registers a mock output or response generator for a connector action."""
        key = self._key(connector_id, action_name)
        self._mocks[key] = mock_output
        self._error_simulations.pop(key, None)

    def register_simulated_error(
        self,
        connector_id: str,
        action_name: str,
        exception: Exception,
    ) -> None:
        """Configures an action to deterministically throw an exception for test coverage."""
        key = self._key(connector_id, action_name)
        self._error_simulations[key] = exception

    def simulate(
        self,
        connector_id: str,
        action_name: str,
        inputs: Dict[str, Any],
    ) -> ExecutionResult:
        """
        Executes a simulated action invocation.
        """
        key = self._key(connector_id, action_name)

        if key in self._error_simulations:
            err = self._error_simulations[key]
            logger.info(f"Simulator raising configured error for {key}: {err}")
            return ExecutionResult(
                connector_id=connector_id,
                action_name=action_name,
                status="FAILED",
                error=str(err),
                latency_ms=5.0,
                cost_usd=0.0,
            )

        mock = self._mocks.get(key)
        if mock is not None:
            if callable(mock):
                output = mock(inputs)
            else:
                output = dict(mock)
        else:
            # Default synthetic response
            output = {
                "simulated": True,
                "connector_id": connector_id,
                "action_name": action_name,
                "inputs_echo": inputs,
            }

        return ExecutionResult(
            connector_id=connector_id,
            action_name=action_name,
            status="SUCCESS",
            output=output,
            latency_ms=10.0,
            cost_usd=0.0,
            cached=True,
        )
