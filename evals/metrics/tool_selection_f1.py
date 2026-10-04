"""
evals/metrics/tool_selection_f1.py
Calculates Precision, Recall, and F1 Score for Agent Tool Invocations and Classifications.
"""

from __future__ import annotations
from typing import List, Set


def compute_tool_f1(expected_tools: List[str], selected_tools: List[str]) -> float:
    """Computes harmonic mean F1 score for tool/router selections."""
    exp_set: Set[str] = set(expected_tools)
    sel_set: Set[str] = set(selected_tools)

    if not exp_set and not sel_set:
        return 1.0
    if not exp_set or not sel_set:
        return 0.0

    true_positives = len(exp_set.intersection(sel_set))
    precision = true_positives / len(sel_set) if sel_set else 0.0
    recall = true_positives / len(exp_set) if exp_set else 0.0

    if precision + recall == 0:
        return 0.0

    return round(2 * (precision * recall) / (precision + recall), 4)
