"""
Enterprise Integration Fabric & Universal Connector Platform (EIF-UCP) - Transformation Engine.
Provides format conversions across JSON, XML, CSV, YAML, Binary, and structured enterprise schemas.
"""

from __future__ import annotations

import base64
import csv
import io
import json
import logging
from typing import Any, Dict, List, Optional, Union
import xml.etree.ElementTree as ET

from app.connectors.core.exceptions import TransformationError

logger = logging.getLogger(__name__)


class TransformationEngine:
    """
    Universal data conversion engine supporting multi-format bidirectional transformations.
    """

    # --- JSON ---
    def json_to_dict(self, json_str: str) -> Dict[str, Any]:
        try:
            return json.loads(json_str)
        except Exception as e:
            raise TransformationError(f"Failed to parse JSON: {e}")

    def dict_to_json(self, data: Dict[str, Any], indent: Optional[int] = None) -> str:
        try:
            return json.dumps(data, indent=indent, default=str)
        except Exception as e:
            raise TransformationError(f"Failed to serialize to JSON: {e}")

    # --- XML ---
    def xml_to_dict(self, xml_str: str) -> Dict[str, Any]:
        """Parses basic XML hierarchy into a nested Python dictionary."""
        try:
            root = ET.fromstring(xml_str)
            return {root.tag: self._elem_to_dict(root)}
        except Exception as e:
            raise TransformationError(f"Failed to parse XML: {e}")

    def _elem_to_dict(self, elem: ET.Element) -> Union[Dict[str, Any], str]:
        children = list(elem)
        if not children:
            return elem.text or ""
        result: Dict[str, Any] = {}
        for child in children:
            child_data = self._elem_to_dict(child)
            if child.tag in result:
                if isinstance(result[child.tag], list):
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = [result[child.tag], child_data]
            else:
                result[child.tag] = child_data
        return result

    def dict_to_xml(self, data: Dict[str, Any], root_tag: str = "root") -> str:
        """Serializes dictionary to an XML string."""
        try:
            root = ET.Element(root_tag)
            self._dict_to_elem(data, root)
            return ET.tostring(root, encoding="utf-8").decode("utf-8")
        except Exception as e:
            raise TransformationError(f"Failed to convert dict to XML: {e}")

    def _dict_to_elem(self, data: Any, parent: ET.Element) -> None:
        if isinstance(data, dict):
            for k, v in data.items():
                child = ET.SubElement(parent, str(k))
                self._dict_to_elem(v, child)
        elif isinstance(data, list):
            for item in data:
                child = ET.SubElement(parent, "item")
                self._dict_to_elem(item, child)
        else:
            parent.text = str(data) if data is not None else ""

    # --- CSV ---
    def csv_to_records(self, csv_str: str, delimiter: str = ",") -> List[Dict[str, Any]]:
        """Parses CSV text into a list of row dictionaries."""
        try:
            reader = csv.DictReader(io.StringIO(csv_str), delimiter=delimiter)
            return [dict(row) for row in reader]
        except Exception as e:
            raise TransformationError(f"Failed to parse CSV: {e}")

    def records_to_csv(self, records: List[Dict[str, Any]], delimiter: str = ",") -> str:
        """Serializes a list of dictionaries to a CSV string."""
        if not records:
            return ""
        try:
            output = io.StringIO()
            writer = csv.DictWriter(output, fieldnames=list(records[0].keys()), delimiter=delimiter)
            writer.writeheader()
            writer.writerows(records)
            return output.getvalue()
        except Exception as e:
            raise TransformationError(f"Failed to serialize records to CSV: {e}")

    # --- Binary & Base64 ---
    def bytes_to_base64(self, data: bytes) -> str:
        return base64.b64encode(data).decode("utf-8")

    def base64_to_bytes(self, b64_str: str) -> bytes:
        try:
            return base64.b64decode(b64_str)
        except Exception as e:
            raise TransformationError(f"Failed to decode Base64 data: {e}")

    # --- Generic Convert ---
    def convert(self, source_data: Any, from_format: str, to_format: str) -> Any:
        """Converts data between formats ('json', 'xml', 'csv', 'dict')."""
        f_from = from_format.lower()
        f_to = to_format.lower()

        # Step 1: Parse to intermediate python structure (dict / list)
        if f_from == "dict" or isinstance(source_data, (dict, list)):
            intermediate = source_data
        elif f_from == "json":
            intermediate = self.json_to_dict(source_data)
        elif f_from == "xml":
            intermediate = self.xml_to_dict(source_data)
        elif f_from == "csv":
            intermediate = self.csv_to_records(source_data)
        else:
            intermediate = source_data

        # Step 2: Render to target format
        if f_to == "dict":
            return intermediate
        elif f_to == "json":
            return self.dict_to_json(intermediate)
        elif f_to == "xml":
            if isinstance(intermediate, dict):
                return self.dict_to_xml(intermediate)
            return self.dict_to_xml({"data": intermediate})
        elif f_to == "csv":
            if isinstance(intermediate, list):
                return self.records_to_csv(intermediate)
            return self.records_to_csv([intermediate])
        return intermediate
