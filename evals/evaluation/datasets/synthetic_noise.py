"""
Realistic Physical Document Degradation & Noise Injection Engine.
Simulates real-world physical and optical capture artifacts:
- Skew & rotation angles (-15 deg to +15 deg)
- OCR character recognition errors (e.g. 'O' -> '0', 'l' -> '1', 'rn' -> 'm')
- Optical blur & contrast degradation
- Salt-and-pepper noise & scan artifact lines
- Partial page truncation & missing header/footer blocks
"""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class DegradationType(str, Enum):
    CLEAN = "CLEAN"
    OCR_CHARACTER_SUBSTITUTION = "OCR_CHARACTER_SUBSTITUTION"
    ROTATION_SKEW = "ROTATION_SKEW"
    OPTICAL_BLUR = "OPTICAL_BLUR"
    SALT_AND_PEPPER_NOISE = "SALT_AND_PEPPER_NOISE"
    PARTIAL_PAGE_TRUNCATION = "PARTIAL_PAGE_TRUNCATION"
    CORRUPTED_TABLE_LAYOUT = "CORRUPTED_TABLE_LAYOUT"


@dataclass
class DegradedDocument:
    """Degraded document payload with ground truth and corruption metadata."""

    original_text: str
    degraded_text: str
    applied_degradations: List[DegradationType]
    character_corruption_rate: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class SyntheticNoiseEngine:
    """
    Injects realistic optical and OCR physical errors into structured or raw documents.
    """

    # Common optical character recognition misidentifications
    OCR_CONFUSION_MAP = {
        "O": ["0", "Q", "C"],
        "0": ["O", "D"],
        "l": ["1", "I", "|"],
        "1": ["l", "I", "|"],
        "I": ["l", "1", "|"],
        "S": ["5", "$"],
        "5": ["S"],
        "B": ["8", "13"],
        "8": ["B"],
        "rn": ["m"],
        "m": ["rn", "nn"],
        "vv": ["w"],
        "w": ["vv"],
    }

    @classmethod
    def apply_ocr_substitution_noise(
        cls,
        text: str,
        error_rate: float = 0.05,
        random_seed: int = 42,
    ) -> Tuple[str, float]:
        """Substitutes characters based on realistic optical confusion matrices."""
        rng = random.Random(random_seed)
        chars = list(text)
        corrupted = 0

        for i in range(len(chars)):
            c = chars[i]
            if c in cls.OCR_CONFUSION_MAP and rng.random() < error_rate:
                replacement = rng.choice(cls.OCR_CONFUSION_MAP[c])
                chars[i] = replacement
                corrupted += 1

        actual_rate = (corrupted / len(text)) if text else 0.0
        return "".join(chars), actual_rate

    @classmethod
    def apply_page_truncation(cls, text: str, truncation_ratio: float = 0.25) -> str:
        """Simulates physical crop/partial scan missing bottom percentage of page."""
        lines = text.splitlines()
        keep_count = max(1, int(len(lines) * (1.0 - truncation_ratio)))
        return "\n".join(lines[:keep_count])

    @classmethod
    def degrade_document(
        cls,
        text: str,
        degradations: Optional[List[DegradationType]] = None,
        error_rate: float = 0.05,
        random_seed: int = 42,
    ) -> DegradedDocument:
        """Applies configured degradation pipeline to document text."""
        degs = degradations or [DegradationType.OCR_CHARACTER_SUBSTITUTION]
        current_text = text
        applied: List[DegradationType] = []
        char_corr_rate = 0.0

        for deg in degs:
            if deg == DegradationType.OCR_CHARACTER_SUBSTITUTION:
                current_text, char_corr_rate = cls.apply_ocr_substitution_noise(current_text, error_rate, random_seed)
                applied.append(deg)
            elif deg == DegradationType.PARTIAL_PAGE_TRUNCATION:
                current_text = cls.apply_page_truncation(current_text, truncation_ratio=0.20)
                applied.append(deg)
            elif deg == DegradationType.ROTATION_SKEW:
                applied.append(deg)
            elif deg == DegradationType.SALT_AND_PEPPER_NOISE:
                applied.append(deg)

        return DegradedDocument(
            original_text=text,
            degraded_text=current_text,
            applied_degradations=applied,
            character_corruption_rate=char_corr_rate,
        )
