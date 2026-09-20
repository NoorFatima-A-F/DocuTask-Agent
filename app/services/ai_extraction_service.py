"""
AI Structured Extraction Service Business Logic Layer.
Orchestrates LLM providers, prompt generation, JSON schema validation, automatic retries,
cost tracking, and database persistence.
"""

import json
import time
from typing import Any, Dict, List, Optional
from uuid import UUID

from app.ai.exceptions import AIRetryLimitExceededException
from app.ai.factory import LLMFactory
from app.ai.prompt_builder import PromptBuilder
from app.ai.schemas import (
    ExtractionMetadata,
    ExtractionRequest,
    ExtractionResponse,
    ExtractionResult,
    ExtractionStatistics,
)
from app.ai.validator import AIValidator
from app.core.exceptions import ResourceNotFoundException
from app.core.logging import logger
from app.models.ai_extraction import AIExtraction
from app.models.user import User
from app.repositories.ai_extraction_repository import AIExtractionRepository
from app.repositories.document_repository import DocumentRepository
from app.services.ocr_service import OCRService


class AIExtractionService:
    """Service handling AI structured document extraction workflow."""

    MAX_RETRIES = 3

    def __init__(
        self,
        document_repo: DocumentRepository,
        ai_extraction_repo: AIExtractionRepository,
        ocr_service: OCRService
    ):
        self.doc_repo = document_repo
        self.ai_repo = ai_extraction_repo
        self.ocr_service = ocr_service

    def _to_response_schema(self, record: AIExtraction) -> ExtractionResponse:
        """Converts database ORM entity to ExtractionResponse Pydantic schema."""
        parsed_json = json.loads(record.structured_json) if isinstance(record.structured_json, str) else record.structured_json

        return ExtractionResponse(
            id=record.id,
            metadata=ExtractionMetadata(
                document_id=record.document_id,
                document_type=record.document_type,
                provider=record.provider,
                model=record.model,
                prompt_version=record.prompt_version,
                created_at=record.created_at
            ),
            statistics=ExtractionStatistics(
                processing_time_ms=record.processing_time_ms,
                input_tokens=record.input_tokens,
                output_tokens=record.output_tokens,
                estimated_cost=record.estimated_cost,
                retry_count=0
            ),
            result=ExtractionResult(
                raw_response=record.raw_response,
                structured_json=parsed_json,
                confidence=record.confidence
            )
        )

    async def extract_structured_data(
        self,
        document_id: UUID,
        owner: User,
        request: ExtractionRequest
    ) -> ExtractionResponse:
        """
        Extracts structured JSON data for document using specified LLM provider and document schema.
        Handles auto-OCR execution, caching, validation, and retry logic.
        """
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc:
            raise ResourceNotFoundException("Document not found")

        # Ownership authorization check
        if doc.owner_id != owner.id and not owner.is_superuser:
            logger.warning(f"Unauthorized AI extraction attempt: User '{owner.id}' on Document '{document_id}'")
            raise ResourceNotFoundException("Document not found")

        doc_type = request.document_type.lower().strip()

        # Caching check
        if not request.force_reextract:
            latest = await self.ai_repo.get_latest(document_id, document_type=doc_type)
            if latest:
                logger.info(f"Returning cached AI extraction for document '{document_id}' type '{doc_type}'")
                return self._to_response_schema(latest)

        # Update status to EXTRACTION_RUNNING
        await self.doc_repo.update_status(doc, "EXTRACTION_RUNNING")

        try:
            # Obtain extracted text from OCR service (runs OCR pipeline automatically if missing)
            try:
                doc_content = await self.ocr_service.get_extracted_text(document_id, owner)
            except ResourceNotFoundException:
                logger.info(f"No text found for doc '{document_id}'. Executing OCR extraction first...")
                doc_content = await self.ocr_service.extract_text_for_document(document_id, owner)

            if not doc_content.text or not doc_content.text.strip():
                logger.warning(f"Document '{document_id}' contains no text content for AI extraction")
                doc_text = "No readable text content was found in this document."
            else:
                doc_text = doc_content.text

            # Select LLM Provider via Factory
            provider = LLMFactory.get_provider(request.provider)
            target_model = request.model or provider.default_model

            # Build Prompts and Schema
            system_instruction = PromptBuilder.build_system_instruction(doc_type)
            user_prompt = PromptBuilder.build_prompt(doc_text, doc_type)
            json_schema = PromptBuilder.get_json_schema(doc_type)

            start_time = time.perf_counter()
            retry_count = 0
            validated_dict = None
            final_raw_response = ""
            total_input_tokens = 0
            total_output_tokens = 0
            confidence = 1.0

            current_prompt = user_prompt

            # Validation & Retry Loop
            while retry_count < self.MAX_RETRIES:
                try:
                    parsed_json, raw_resp, in_tok, out_tok = await provider.generate_json(
                        prompt=current_prompt,
                        json_schema=json_schema,
                        system_instruction=system_instruction,
                        model=target_model
                    )

                    total_input_tokens += in_tok
                    total_output_tokens += out_tok
                    final_raw_response = raw_resp

                    # Validate parsed JSON against Pydantic schema
                    validated_dict, confidence = AIValidator.validate(parsed_json, doc_type)
                    break  # Successful validation

                except Exception as exc:
                    retry_count += 1
                    logger.warning(
                        f"AI extraction validation failure on attempt {retry_count}/{self.MAX_RETRIES} for doc '{document_id}': {str(exc)}"
                    )
                    if retry_count >= self.MAX_RETRIES:
                        logger.error(f"Max retries reached for doc '{document_id}'.")
                        raise AIRetryLimitExceededException(
                            f"Failed to obtain valid JSON schema output after {self.MAX_RETRIES} attempts: {str(exc)}"
                        )
                    # Modify prompt for corrective retry
                    current_prompt = (
                        f"{user_prompt}\n\n"
                        f"CORRECTION REQUIRED: Your previous attempt failed validation with error: {str(exc)}.\n"
                        f"Please correct the JSON structure to strictly conform to the required schema."
                    )

            end_time = time.perf_counter()
            processing_time_ms = int((end_time - start_time) * 1000)
            estimated_cost = provider.calculate_cost(total_input_tokens, total_output_tokens, target_model)

            # Persist AIExtraction record in database
            extraction_record = await self.ai_repo.create({
                "document_id": document_id,
                "document_type": doc_type,
                "provider": provider.provider_name,
                "model": target_model,
                "raw_response": final_raw_response,
                "structured_json": json.dumps(validated_dict),
                "prompt_version": "v1.0",
                "processing_time_ms": processing_time_ms,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
                "estimated_cost": estimated_cost,
                "confidence": confidence
            })

            # Update document status to EXTRACTION_COMPLETED
            await self.doc_repo.update_status(doc, "EXTRACTION_COMPLETED")

            logger.info(
                f"AI extraction completed for doc '{document_id}': Type='{doc_type}', Time={processing_time_ms}ms, Cost=${estimated_cost}"
            )

            return ExtractionResponse(
                id=extraction_record.id,
                metadata=ExtractionMetadata(
                    document_id=document_id,
                    document_type=doc_type,
                    provider=provider.provider_name,
                    model=target_model,
                    prompt_version="v1.0",
                    created_at=extraction_record.created_at
                ),
                statistics=ExtractionStatistics(
                    processing_time_ms=processing_time_ms,
                    input_tokens=total_input_tokens,
                    output_tokens=total_output_tokens,
                    estimated_cost=estimated_cost,
                    retry_count=retry_count
                ),
                result=ExtractionResult(
                    raw_response=final_raw_response,
                    structured_json=validated_dict,
                    confidence=confidence
                )
            )

        except Exception as exc:
            logger.error(f"AI extraction failed for document '{document_id}': {str(exc)}")
            await self.doc_repo.update_status(doc, "EXTRACTION_FAILED")
            raise exc

    async def get_latest_result(self, document_id: UUID, owner: User) -> ExtractionResponse:
        """Retrieves most recent AI extraction result for a document."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        latest = await self.ai_repo.get_latest(document_id)
        if not latest:
            raise ResourceNotFoundException("No AI extraction results found for this document. Run extraction first.")

        return self._to_response_schema(latest)

    async def get_extraction_status(self, document_id: UUID, owner: User) -> Dict[str, Any]:
        """Retrieves AI extraction operational status for a document."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        latest = await self.ai_repo.get_latest(document_id)
        return {
            "document_id": document_id,
            "status": doc.upload_status,
            "has_extraction": latest is not None,
            "document_type": latest.document_type if latest else None,
            "confidence": latest.confidence if latest else None
        }

    async def get_extraction_history(self, document_id: UUID, owner: User) -> List[ExtractionResponse]:
        """Retrieves complete history of past AI extractions for a document."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        records = await self.ai_repo.get_history(document_id)
        return [self._to_response_schema(r) for r in records]

    async def delete_result(self, document_id: UUID, owner: User) -> None:
        """Deletes AI extraction results for a document."""
        doc = await self.doc_repo.get_by_id(document_id)
        if not doc or (doc.owner_id != owner.id and not owner.is_superuser):
            raise ResourceNotFoundException("Document not found")

        latest = await self.ai_repo.get_latest(document_id)
        if latest:
            await self.ai_repo.delete(latest.id)
            logger.info(f"Deleted AI extraction result for document '{document_id}'")
