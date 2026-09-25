"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Connector Builder SDK.
Provides a fluent builder pattern for authoring lightweight, compliant connector plugins.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional
from app.connectors.core.models import (
    ActionDescriptor,
    AuthType,
    CapabilityDescriptor,
    Connector,
    ConnectorCategory,
    ConnectorStatus,
    TriggerDescriptor,
)
from app.connectors.sdk.base import BaseConnector


class FunctionalConnector(BaseConnector):
    """Concrete connector implementation populated by the ConnectorBuilder."""

    def __init__(
        self,
        connector_model: Connector,
        auth_handler: Optional[Callable[[Dict[str, Any]], bool]] = None,
        validate_handler: Optional[Callable[[], bool]] = None,
        capabilities_list: Optional[List[CapabilityDescriptor]] = None,
        actions_list: Optional[List[ActionDescriptor]] = None,
        triggers_list: Optional[List[TriggerDescriptor]] = None,
        action_dispatch: Optional[Dict[str, Callable[[Dict[str, Any]], Any]]] = None,
    ):
        super().__init__(connector_model)
        self._auth_handler = auth_handler or (lambda creds: True)
        self._validate_handler = validate_handler or (lambda: True)
        self._capabilities_list = capabilities_list or []
        self._actions_list = actions_list or []
        self._triggers_list = triggers_list or []
        self._action_dispatch = action_dispatch or {}

    def authenticate(self, credentials: Dict[str, Any]) -> bool:
        self._authenticated = self._auth_handler(credentials)
        return self._authenticated

    def validate_connection(self) -> bool:
        return self._validate_handler()

    def capabilities(self) -> List[CapabilityDescriptor]:
        return list(self._capabilities_list)

    def actions(self) -> List[ActionDescriptor]:
        return list(self._actions_list)

    def triggers(self) -> List[TriggerDescriptor]:
        return list(self._triggers_list)

    def execute(
        self,
        action_name: str,
        inputs: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if action_name in self._action_dispatch:
            res = self._action_dispatch[action_name](inputs)
            if isinstance(res, dict):
                return res
            return {"result": res}
        return {"status": "SUCCESS", "action": action_name, "inputs": inputs}


class ConnectorBuilder:
    """
    Fluent builder API for creating enterprise connector plugins.
    """

    def __init__(self, connector_id: str, name: str):
        self._id = connector_id
        self._name = name
        self._vendor = "DocuTask"
        self._version = "1.0.0"
        self._category = ConnectorCategory.CUSTOM
        self._auth_types: List[AuthType] = [AuthType.API_KEY]
        self._capabilities: List[CapabilityDescriptor] = []
        self._actions: List[ActionDescriptor] = []
        self._triggers: List[TriggerDescriptor] = []
        self._action_handlers: Dict[str, Callable[[Dict[str, Any]], Any]] = {}
        self._auth_fn: Optional[Callable[[Dict[str, Any]], bool]] = None
        self._validate_fn: Optional[Callable[[], bool]] = None
        self._documentation = ""
        self._license = "Apache-2.0"
        self._config_schema: Dict[str, Any] = {}

    def with_vendor(self, vendor: str) -> ConnectorBuilder:
        self._vendor = vendor
        return self

    def with_version(self, version: str) -> ConnectorBuilder:
        self._version = version
        return self

    def with_category(self, category: ConnectorCategory | str) -> ConnectorBuilder:
        self._category = category if isinstance(category, ConnectorCategory) else ConnectorCategory(category)
        return self

    def with_auth_type(self, auth_type: AuthType | str) -> ConnectorBuilder:
        a_type = auth_type if isinstance(auth_type, AuthType) else AuthType(auth_type)
        if a_type not in self._auth_types:
            self._auth_types.append(a_type)
        return self

    def with_capability(
        self,
        name: str,
        category: ConnectorCategory = ConnectorCategory.CUSTOM,
        description: str = "",
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
    ) -> ConnectorBuilder:
        self._capabilities.append(
            CapabilityDescriptor(
                name=name,
                category=category,
                description=description,
                input_schema=input_schema or {},
                output_schema=output_schema or {},
            )
        )
        return self

    def with_action(
        self,
        name: str,
        capability: str,
        handler: Callable[[Dict[str, Any]], Any],
        description: str = "",
        input_schema: Optional[Dict[str, Any]] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        cost_usd: float = 0.001,
        timeout_seconds: float = 30.0,
    ) -> ConnectorBuilder:
        self._actions.append(
            ActionDescriptor(
                name=name,
                connector_id=self._id,
                capability=capability,
                description=description,
                input_schema=input_schema or {},
                output_schema=output_schema or {},
                cost_usd=cost_usd,
                timeout_seconds=timeout_seconds,
            )
        )
        self._action_handlers[name] = handler
        return self

    def with_trigger(
        self,
        name: str,
        trigger_type: Any,
        description: str = "",
        config_schema: Optional[Dict[str, Any]] = None,
    ) -> ConnectorBuilder:
        self._triggers.append(
            TriggerDescriptor(
                name=name,
                connector_id=self._id,
                trigger_type=trigger_type,
                description=description,
                config_schema=config_schema or {},
            )
        )
        return self

    def with_auth_validator(self, auth_fn: Callable[[Dict[str, Any]], bool]) -> ConnectorBuilder:
        self._auth_fn = auth_fn
        return self

    def with_connection_validator(self, validate_fn: Callable[[], bool]) -> ConnectorBuilder:
        self._validate_fn = validate_fn
        return self

    def with_documentation(self, doc: str) -> ConnectorBuilder:
        self._documentation = doc
        return self

    def build(self) -> BaseConnector:
        model = Connector(
            id=self._id,
            name=self._name,
            vendor=self._vendor,
            version=self._version,
            category=self._category,
            capabilities=[c.name for c in self._capabilities],
            authentication_types=self._auth_types,
            documentation=self._documentation,
            license=self._license,
            config_schema=self._config_schema,
            status=ConnectorStatus.READY,
        )
        return FunctionalConnector(
            connector_model=model,
            auth_handler=self._auth_fn,
            validate_handler=self._validate_fn,
            capabilities_list=self._capabilities,
            actions_list=self._actions,
            triggers_list=self._triggers,
            action_dispatch=self._action_handlers,
        )
