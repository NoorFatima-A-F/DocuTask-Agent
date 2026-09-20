"""
Evidence Provenance & Scientific Lineage Framework
Module: provenance_serialization.py

Serializes W3C PROV Documents into:
- JSON-LD
- PROV-N (Provenance Notation)
- PROV-XML
- OpenLineage JSON
"""

from __future__ import annotations

import json
from typing import Any, Dict, List
import xml.etree.ElementTree as ET

from research_validation.provenance.provenance_schema import (
    OpenLineageRunEvent, ProvDocument, ProvRelation
)


class ProvenanceSerializer:
    """
    Multi-format serializer for scientific provenance graphs.
    """

    @classmethod
    def to_json_ld(cls, doc: ProvDocument) -> str:
        """Serialize W3C PROV Document to standard JSON-LD."""
        context = {
            "prov": doc.namespaces.get("prov", "http://www.w3.org/ns/prov#"),
            "xsd": doc.namespaces.get("xsd", "http://www.w3.org/2001/XMLSchema#"),
            "rvisf": doc.namespaces.get("rvisf", "https://deepmind.google/rvisf/provenance#"),
            "entity": "prov:Entity",
            "activity": "prov:Activity",
            "agent": "prov:Agent",
            "used": "prov:used",
            "wasGeneratedBy": "prov:wasGeneratedBy",
            "wasDerivedFrom": "prov:wasDerivedFrom",
            "wasAttributedTo": "prov:wasAttributedTo",
            "wasAssociatedWith": "prov:wasAssociatedWith",
        }

        graph: List[Dict[str, Any]] = []

        # Entities
        for e in doc.entities.values():
            node = {
                "@id": f"rvisf:{e.entity_id}",
                "@type": "prov:Entity",
                "prov:label": e.label,
                "prov:generatedAtTime": e.generated_at_time,
                "attributes": e.attributes
            }
            if e.was_derived_from_ids:
                node["prov:wasDerivedFrom"] = [f"rvisf:{pid}" for pid in e.was_derived_from_ids]
            if e.was_generated_by_id:
                node["prov:wasGeneratedBy"] = f"rvisf:{e.was_generated_by_id}"
            if e.was_attributed_to_id:
                node["prov:wasAttributedTo"] = f"rvisf:{e.was_attributed_to_id}"
            graph.append(node)

        # Activities
        for a in doc.activities.values():
            node = {
                "@id": f"rvisf:{a.activity_id}",
                "@type": "prov:Activity",
                "prov:label": a.label,
                "prov:startedAtTime": a.start_time,
                "prov:endedAtTime": a.end_time,
                "attributes": a.attributes
            }
            if a.used_entity_ids:
                node["prov:used"] = [f"rvisf:{uid}" for uid in a.used_entity_ids]
            if a.was_associated_with_id:
                node["prov:wasAssociatedWith"] = f"rvisf:{a.was_associated_with_id}"
            graph.append(node)

        # Agents
        for ag in doc.agents.values():
            node = {
                "@id": f"rvisf:{ag.agent_id}",
                "@type": f"prov:{ag.agent_type}",
                "prov:label": ag.name,
                "attributes": ag.attributes
            }
            if ag.acted_on_behalf_of_id:
                node["prov:actedOnBehalfOf"] = f"rvisf:{ag.acted_on_behalf_of_id}"
            graph.append(node)

        payload = {
            "@context": context,
            "@id": f"rvisf:{doc.document_id}",
            "@graph": graph
        }

        return json.dumps(payload, indent=2, sort_keys=True)

    @classmethod
    def to_prov_n(cls, doc: ProvDocument) -> str:
        """Serialize W3C PROV Document to PROV-N (Provenance Notation)."""
        lines: List[str] = [f"document {doc.document_id}"]

        # Prefixes
        for prefix, uri in doc.namespaces.items():
            lines.append(f"  prefix {prefix} <{uri}>")
        lines.append("")

        # Entities
        for e in doc.entities.values():
            lines.append(f"  entity(rvisf:{e.entity_id}, [prov:label=\"{e.label}\"])")

        # Activities
        for a in doc.activities.values():
            lines.append(f"  activity(rvisf:{a.activity_id}, {a.start_time}, {a.end_time}, [prov:label=\"{a.label}\"])")

        # Agents
        for ag in doc.agents.values():
            lines.append(f"  agent(rvisf:{ag.agent_id}, [prov:label=\"{ag.name}\", prov:type=\"{ag.agent_type}\"])")

        # Relations
        for r in doc.relations:
            lines.append(f"  {r.relation_type.value}(rvisf:{r.source_id}, rvisf:{r.target_id})")

        lines.append("endDocument")
        return "\n".join(lines)

    @classmethod
    def to_prov_xml(cls, doc: ProvDocument) -> str:
        """Serialize W3C PROV Document to PROV-XML."""
        ET.register_namespace("prov", "http://www.w3.org/ns/prov#")
        ET.register_namespace("rvisf", "https://deepmind.google/rvisf/provenance#")
        root = ET.Element("{http://www.w3.org/ns/prov#}document")

        # Entities
        for e in doc.entities.values():
            e_elem = ET.SubElement(root, "{http://www.w3.org/ns/prov#}entity")
            e_elem.set("{http://www.w3.org/ns/prov#}id", f"rvisf:{e.entity_id}")
            lbl = ET.SubElement(e_elem, "{http://www.w3.org/ns/prov#}label")
            lbl.text = e.label

        # Activities
        for a in doc.activities.values():
            a_elem = ET.SubElement(root, "{http://www.w3.org/ns/prov#}activity")
            a_elem.set("{http://www.w3.org/ns/prov#}id", f"rvisf:{a.activity_id}")
            lbl = ET.SubElement(a_elem, "{http://www.w3.org/ns/prov#}label")
            lbl.text = a.label

        # Agents
        for ag in doc.agents.values():
            ag_elem = ET.SubElement(root, "{http://www.w3.org/ns/prov#}agent")
            ag_elem.set("{http://www.w3.org/ns/prov#}id", f"rvisf:{ag.agent_id}")
            lbl = ET.SubElement(ag_elem, "{http://www.w3.org/ns/prov#}label")
            lbl.text = ag.name

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @classmethod
    def to_openlineage_json(cls, run_event: OpenLineageRunEvent) -> str:
        """Serialize OpenLineage RunEvent to JSON."""
        return json.dumps(run_event.to_dict(), indent=2, sort_keys=True)
