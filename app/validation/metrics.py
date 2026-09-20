"""
Automatic Evaluation & Quality Metrics Engine.
Computes objective, mathematical AI extraction quality metrics: Accuracy, Precision, Recall,
F1 Score, Hallucination Rate, Schema Compliance, and Confidence Correctness.
"""

from typing import Any, Dict
from app.validation.schemas import MetricEvaluationResult


class EvaluationMetricsEngine:
    """Engine computing mathematical AI quality metrics against gold ground truth."""

    @classmethod
    def evaluate(
        self,
        actual_json: Dict[str, Any],
        ground_truth_json: Dict[str, Any],
        schema_valid: bool = True,
        confidence: float = 1.0
    ) -> MetricEvaluationResult:
        """
        Calculates field-level and document-level metrics comparing actual AI output against ground truth.
        """
        all_keys = set(ground_truth_json.keys()).union(set(actual_json.keys()))
        total_fields = len(all_keys) if all_keys else 1

        correct_fields = 0
        missing_fields = 0
        hallucinated_fields = 0

        for key in all_keys:
            expected_val = ground_truth_json.get(key)
            actual_val = actual_json.get(key)

            if key in ground_truth_json and key in actual_json:
                # Value comparison
                if self._compare_values(actual_val, expected_val):
                    correct_fields += 1
                elif actual_val is None or actual_val == "" or actual_val == []:
                    missing_fields += 1
                else:
                    hallucinated_fields += 1
            elif key in ground_truth_json and key not in actual_json:
                missing_fields += 1
            elif key not in ground_truth_json and key in actual_json:
                if actual_val is not None and actual_val != "" and actual_val != []:
                    hallucinated_fields += 1

        # Accuracy Calculations
        field_accuracy = round(correct_fields / total_fields, 4) if total_fields > 0 else 1.0
        exact_match = 1.0 if actual_json == ground_truth_json else 0.0
        schema_compliance = 1.0 if schema_valid else 0.0

        missing_rate = round(missing_fields / total_fields, 4) if total_fields > 0 else 0.0
        hallucination_rate = round(hallucinated_fields / total_fields, 4) if total_fields > 0 else 0.0

        # Precision, Recall, F1 Score
        tp = correct_fields
        fp = hallucinated_fields
        fn = missing_fields

        precision = round(tp / (tp + fp), 4) if (tp + fp) > 0 else 1.0
        recall = round(tp / (tp + fn), 4) if (tp + fn) > 0 else 1.0

        if (precision + recall) > 0:
            f1_score = round(2 * (precision * recall) / (precision + recall), 4)
        else:
            f1_score = 0.0

        # Confidence Correctness
        confidence_correctness = round(1.0 - abs(confidence - field_accuracy), 4)

        return MetricEvaluationResult(
            total_fields=total_fields,
            correct_fields=correct_fields,
            missing_fields=missing_fields,
            hallucinated_fields=hallucinated_fields,
            field_accuracy=field_accuracy,
            exact_match_accuracy=exact_match,
            schema_compliance_rate=schema_compliance,
            missing_field_rate=missing_rate,
            hallucination_rate=hallucination_rate,
            precision=precision,
            recall=recall,
            f1_score=f1_score,
            average_confidence=confidence,
            confidence_correctness=confidence_correctness
        )

    @staticmethod
    def _compare_values(val1: Any, val2: Any) -> bool:
        """Helper comparing values with string, number, and type tolerance."""
        if val1 == val2:
            return True
        if val1 is None and val2 is None:
            return True
        if str(val1).strip().lower() == str(val2).strip().lower():
            return True
        # Numeric tolerance check
        try:
            f1, f2 = float(val1), float(val2)
            return abs(f1 - f2) < 0.01
        except (ValueError, TypeError):
            pass
        return False
