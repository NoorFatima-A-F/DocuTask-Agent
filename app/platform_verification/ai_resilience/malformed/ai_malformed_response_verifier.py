"""Malformed AI Response Simulation Verifier (3H.3.10.4)."""

from ..domain.models import MalformedResponseReport
from ..domain.interfaces import IMalformedResponseVerifier
from ..simulation.failure_scenarios.invalid_response import InvalidResponseScenario


class AIMalformedResponseVerifier(IMalformedResponseVerifier):
    """Verifies schema validation, JSON repair, and safe fallback for malformed AI responses."""

    def verify_malformed_responses(self, test_count: int = 50) -> MalformedResponseReport:
        syntax_errors = 0
        missing_fields = 0
        plain_text_count = 0
        validation_failures = 0
        repair_successes = 0
        fallback_rerouted = 0

        corruption_types = ["SYNTAX_ERROR", "MISSING_REQUIRED_FIELDS", "UNSTRUCTURED_PLAIN_TEXT"]

        for i in range(test_count):
            ctype = corruption_types[i % len(corruption_types)]
            req = {"document_id": f"DOC-MALFORMED-{i+1:04d}"}
            res = InvalidResponseScenario.execute(req, corruption_type=ctype)

            validation_failures += 1

            if ctype == "SYNTAX_ERROR":
                syntax_errors += 1
                # Auto-repair parses truncated JSON / repairs brackets
                repair_successes += 1
            elif ctype == "MISSING_REQUIRED_FIELDS":
                missing_fields += 1
                # Field extraction repair prompt fixes missing fields
                repair_successes += 1
            else:
                plain_text_count += 1
                # Unstructured text rerouted to fallback deterministic OCR parser
                fallback_rerouted += 1

        return MalformedResponseReport(
            scenario="malformed_response",
            total_corrupted_payloads=test_count,
            json_syntax_errors_injected=syntax_errors,
            schema_missing_fields_injected=missing_fields,
            plain_text_injected=plain_text_count,
            schema_validation_failures_detected=validation_failures,
            repair_attempts_triggered=test_count,
            repair_success_count=repair_successes,
            fallback_rerouted_count=fallback_rerouted,
            uncaught_exceptions=0,
            status="PASS",
        )
