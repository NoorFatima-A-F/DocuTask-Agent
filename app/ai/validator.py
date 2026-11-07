"""Schema validation of LLM output against the per-document-type Pydantic models.

Validation answers only "is this shaped correctly?". How much to trust the values is
decided by :mod:`app.ai.confidence` against the source text.
"""

from typing import Any, Dict

from pydantic import ValidationError

from app.ai.exceptions import AIValidationException
from app.ai.prompt_builder import PromptBuilder
from app.core.logging import logger
from app.core.security import sanitize_log_input


class AIValidator:
    """Validates LLM output against Pydantic models."""

    @classmethod
    def validate(cls, raw_json_dict: Dict[str, Any], document_type: str) -> Dict[str, Any]:
        """Return the validated, normalised dict or raise :class:`AIValidationException`."""
        model_cls = PromptBuilder.get_target_model(document_type)
        try:
            return model_cls.model_validate(raw_json_dict).model_dump()
        except ValidationError as exc:
            error_details = exc.errors(include_url=False, include_input=False)
            error_msg = "; ".join(
                f"Field '{'->'.join(str(part) for part in err['loc'])}': {err['msg']}" for err in error_details
            )
            logger.warning(
                "AI JSON validation failure for document type '%s': %s",
                sanitize_log_input(document_type),
                sanitize_log_input(error_msg),
            )
            raise AIValidationException(
                message=f"LLM generated JSON failed schema validation: {error_msg}", errors=error_details
            ) from exc
