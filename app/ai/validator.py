from app.core.security import sanitize_log_input
"""
AI Output Validator Module.
Validates raw LLM generated JSON against target Pydantic schemas.
"""

from typing import Any, Dict, Tuple
from pydantic import ValidationError

from app.ai.exceptions import AIValidationException
from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger


class AIValidator:
    """Validator validating LLM output against Pydantic models."""

    @classmethod
    def validate(cls, raw_json_dict: Dict[str, Any], document_type: str) -> Tuple[Dict[str, Any], float]:
        """
        Validates parsed JSON dictionary against Pydantic schema for document_type.
        
        :param raw_json_dict: Dictionary parsed from LLM JSON response
        :param document_type: Target document type name
        :return: Tuple of (validated_dict, confidence_score)
        :raises AIValidationException: If validation fails
        """
        model_cls = PromptBuilder.get_target_model(document_type)

        try:
            validated_instance = model_cls.model_validate(raw_json_dict)
            validated_dict = validated_instance.model_dump()

            # Calculate confidence score based on non-null fields
            total_fields = len(validated_dict)
            non_null_fields = sum(
                1 for v in validated_dict.values()
                if v is not None and v != [] and v != {}
            )
            confidence = round(non_null_fields / total_fields, 4) if total_fields > 0 else 1.0

            return validated_dict, max(0.5, confidence)

        except ValidationError as exc:
            error_details = exc.errors()
            formatted_errors = [
                f"Field '{'->'.join(str(l) for l in err['loc'])}': {err['msg']}"
                for err in error_details
            ]
            error_msg = "; ".join(formatted_errors)
            logger.warning("AI JSON validation failure for document type '%s': %s", sanitize_log_input(document_type), sanitize_log_input(error_msg))
            raise AIValidationException(
                message=f"LLM generated JSON failed schema validation: {error_msg}",
                errors=error_details
            )
