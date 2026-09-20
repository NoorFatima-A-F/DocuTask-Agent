"""
Formula Migration Utility for Phase 13.3 (ASCE-CGP).
Migrates historical scores across formula revisions without data loss.
"""

from typing import Dict, Any


class FormulaMigrator:
    """
    Translates legacy confidence calculations into modernized v1.3.0 schema representations.
    """

    @classmethod
    def migrate_score(cls, old_score: float, from_version: str, to_version: str = "v1.3.0") -> Dict[str, Any]:
        if from_version == to_version:
            return {"score": old_score, "version": to_version, "migrated": False}

        # Apply calibration adjustment factor
        adjustment = 1.0 if from_version == "v1.2.0" else 0.98
        new_score = round(max(0.0, min(1.0, old_score * adjustment)), 4)

        return {
            "original_score": old_score,
            "migrated_score": new_score,
            "from_version": from_version,
            "to_version": to_version,
            "migrated": True,
        }
