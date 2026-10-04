"""
evals/metrics/ocr_character_error_rate.py
Computes Character Error Rate (CER) and Word Error Rate (WER) via Levenshtein edit distance.
"""

from __future__ import annotations


def compute_levenshtein(s1: str, s2: str) -> int:
    """Computes standard dynamic programming Levenshtein edit distance."""
    if len(s1) < len(s2):
        return compute_levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]


def compute_cer(reference: str, hypothesis: str) -> float:
    """Computes Character Error Rate (CER = EditDistance / RefLength)."""
    if not reference:
        return 0.0 if not hypothesis else 1.0

    distance = compute_levenshtein(reference, hypothesis)
    return round(distance / max(len(reference), 1), 4)
