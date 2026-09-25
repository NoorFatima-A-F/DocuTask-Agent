"""
Formula Versioning Manager for Phase 13.3 (ASCE-CGP).
Maintains version histories of mathematical confidence formulas.
"""

from typing import Dict, List, Any


class FormulaVersioningManager:
    """
    Tracks historical revisions of confidence formulas and deprecation states.
    """

    VERSION_HISTORY: List[Dict[str, Any]] = [
        {"version": "v1.0.0", "released": "2026-01-15", "status": "DEPRECATED", "notes": "Simple unweighted mean."},
        {"version": "v1.1.0", "released": "2026-03-20", "status": "DEPRECATED", "notes": "Added linear feature weighting."},
        {"version": "v1.2.0", "released": "2026-06-10", "status": "SUPPORTED", "notes": "Added temperature scaling calibration."},
        {"version": "v1.3.0", "released": "2026-09-01", "status": "ACTIVE_DEFAULT", "notes": "Multi-dimensional ensemble with Bayesian prior updates."},
    ]

    @classmethod
    def get_active_version(cls) -> str:
        return "v1.3.0"

    @classmethod
    def list_versions(cls) -> List[Dict[str, Any]]:
        return cls.VERSION_HISTORY
