"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Schema Mapper.
Provides declarative schema translation, nested path extraction, conditional logic,
computed fields, default fallbacks, and enum lookup tables.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field

from app.connectors.core.exceptions import SchemaMappingError

logger = logging.getLogger(__name__)


class FieldMappingRule(BaseModel):
    """Specification for mapping a source path to a target field."""
    target_field: str
    source_path: Optional[str] = None  # Dot-separated path, e.g. "customer.contact.email"
    default_value: Optional[Any] = None
    transform_fn_name: Optional[str] = None  # e.g. "uppercase", "lowercase", "int", "float"
    lookup_table: Optional[Dict[str, Any]] = None  # Value substitution dictionary
    computed_template: Optional[str] = None  # e.g. "{first_name} {last_name}"


class SchemaMappingPlan(BaseModel):
    """Declarative collection of mapping rules for transforming one schema to another."""
    id: str = "default_mapping"
    version: str = "1.0.0"
    source_schema_name: str = "external"
    target_schema_name: str = "internal"
    rules: List[FieldMappingRule] = Field(default_factory=list)


class SchemaMapper:
    """
    Executes declarative schema translations between heterogeneous system representations.
    """

    def __init__(self):
        self._plans: Dict[str, SchemaMappingPlan] = {}
        self._custom_transforms: Dict[str, Callable[[Any], Any]] = {
            "uppercase": lambda v: str(v).upper() if v is not None else "",
            "lowercase": lambda v: str(v).lower() if v is not None else "",
            "int": lambda v: int(v) if v is not None and str(v).isdigit() else 0,
            "float": lambda v: float(v) if v is not None else 0.0,
            "strip": lambda v: str(v).strip() if v is not None else "",
        }

    def register_plan(self, plan: SchemaMappingPlan) -> None:
        """Registers a reusable schema mapping plan."""
        self._plans[plan.id] = plan

    def register_transform(self, name: str, fn: Callable[[Any], Any]) -> None:
        """Registers a custom transformation function for field mapping."""
        self._custom_transforms[name] = fn

    def _get_nested_value(self, data: Dict[str, Any], path: str) -> Any:
        """Navigates dot-separated dictionary keys safely."""
        keys = path.split(".")
        curr: Any = data
        for k in keys:
            if isinstance(curr, dict) and k in curr:
                curr = curr[k]
            else:
                return None
        return curr

    def _set_nested_value(self, target_dict: Dict[str, Any], target_field: str, value: Any) -> None:
        """Sets value at dot-separated nested path in target dictionary."""
        keys = target_field.split(".")
        curr = target_dict
        for k in keys[:-1]:
            if k not in curr or not isinstance(curr[k], dict):
                curr[k] = {}
            curr = curr[k]
        curr[keys[-1]] = value

    def map_schema(
        self,
        source_data: Dict[str, Any],
        mapping_plan: SchemaMappingPlan | str,
    ) -> Dict[str, Any]:
        """
        Applies a mapping plan against source data to produce the target structured dictionary.
        """
        if isinstance(mapping_plan, str):
            plan = self._plans.get(mapping_plan)
            if not plan:
                raise SchemaMappingError(f"Mapping plan '{mapping_plan}' not found")
        else:
            plan = mapping_plan

        target: Dict[str, Any] = {}

        for rule in plan.rules:
            val = None

            # 1. Computed Template
            if rule.computed_template:
                try:
                    val = rule.computed_template.format(**source_data)
                except Exception as e:
                    logger.debug(f"Computed template failed for field '{rule.target_field}': {e}")
                    val = rule.default_value

            # 2. Path extraction
            elif rule.source_path:
                extracted = self._get_nested_value(source_data, rule.source_path)
                val = extracted if extracted is not None else rule.default_value

            # 3. Direct default
            else:
                val = rule.default_value

            # 4. Lookup table substitution
            if rule.lookup_table and val is not None:
                str_key = str(val)
                val = rule.lookup_table.get(str_key, val)

            # 5. Transform function
            if rule.transform_fn_name and val is not None:
                fn = self._custom_transforms.get(rule.transform_fn_name)
                if fn:
                    try:
                        val = fn(val)
                    except Exception as e:
                        logger.warning(f"Transform '{rule.transform_fn_name}' failed: {e}")

            # Assign to target
            self._set_nested_value(target, rule.target_field, val)

        return target
