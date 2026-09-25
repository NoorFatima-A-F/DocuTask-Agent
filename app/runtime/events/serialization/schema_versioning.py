"""
DocuTask Agent - Event Schema Versioning & Migrations
Phase 13.1: Autonomous Runtime Observability & Domain Event Platform (ARODP)
"""

from typing import Dict, Any


class EventSchemaVersioning:
    """
    Handles backwards-compatible event schema versioning and payload transformations.
    """

    CURRENT_VERSION = "13.1.0"

    @staticmethod
    def migrate_if_needed(event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Upgrades older event schema versions to the latest canonical format."""
        event_dict.get("version", "1.0.0")
        
        # If older schema without correlation_id
        if "correlation_id" not in event_dict:
            event_dict["correlation_id"] = f"corr-{event_dict.get('mission_id', 'global')}"
            
        if "causation_id" not in event_dict:
            event_dict["causation_id"] = f"cause-{event_dict.get('event_id', 'init')}"

        if "actor" not in event_dict or isinstance(event_dict["actor"], str):
            event_dict["actor"] = {
                "actor_id": str(event_dict.get("actor", "system")),
                "actor_type": "SYSTEM",
            }

        event_dict["version"] = EventSchemaVersioning.CURRENT_VERSION
        return event_dict
