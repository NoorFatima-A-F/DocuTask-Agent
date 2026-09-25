"""
Confidence Dimensions Specification for Phase 13.3 (ASCE-CGP).
Defines the 13 independent confidence dimensions calculated across the platform.
"""

from enum import Enum


class ConfidenceDimension(str, Enum):
    OCR = "OCR"
    EXTRACTION = "EXTRACTION"
    VALIDATION = "VALIDATION"
    PLANNER = "PLANNER"
    EXECUTION = "EXECUTION"
    WORKER = "WORKER"
    MEMORY = "MEMORY"
    EVIDENCE = "EVIDENCE"
    RECOVERY = "RECOVERY"
    REFLECTION = "REFLECTION"
    GOVERNANCE = "GOVERNANCE"
    MISSION = "MISSION"
    OVERALL = "OVERALL"


class ConfidenceStatus(str, Enum):
    VERIFIED = "VERIFIED"
    CALIBRATED = "CALIBRATED"
    UNVERIFIED = "UNVERIFIED"
    DEGRADED = "DEGRADED"
    REJECTED = "REJECTED"
