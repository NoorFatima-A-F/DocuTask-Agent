"""
Benchmark & Reproducibility Profiling Engine.
Executes repeated extraction runs on identical input datasets to evaluate determinism and output consistency.
"""

from typing import Any, Dict, List
from app.ai.base import LLMProvider
from app.ai.prompt_builder import PromptBuilder
from app.ai.validator import AIValidator
from app.core.logging import logger


class ReproducibilityEngine:
    """Engine executing determinism and reproducibility experiments."""

    @classmethod
    async def evaluate_reproducibility(
        cls,
        provider: LLMProvider,
        ocr_text: str,
        document_type: str,
        iterations: int = 3
    ) -> Dict[str, Any]:
        """
        Executes iterations identical runs and measures output consistency.
        """
        system_instruction = PromptBuilder.build_system_instruction(document_type)
        prompt = PromptBuilder.build_prompt(ocr_text, document_type)
        json_schema = PromptBuilder.get_json_schema(document_type)

        results: List[Dict[str, Any]] = []

        for idx in range(iterations):
            parsed_dict, raw_text, in_tok, out_tok = await provider.generate_json(
                prompt=prompt,
                json_schema=json_schema,
                system_instruction=system_instruction
            )
            validated_dict, _ = AIValidator.validate(parsed_dict, document_type)
            results.append(validated_dict)

        # Check field consistency across iterations
        first_keys = set(results[0].keys())
        key_matches = all(set(r.keys()) == first_keys for r in results)

        # Calculate value similarity
        identical_runs = sum(1 for r in results if r == results[0])
        consistency_rate = round(identical_runs / iterations, 4)

        logger.info(f"Reproducibility profiling completed: Iterations={iterations}, ConsistencyRate={consistency_rate * 100}%")

        return {
            "iterations": iterations,
            "document_type": document_type,
            "consistency_rate": consistency_rate,
            "key_structure_match": key_matches,
            "is_fully_reproducible": consistency_rate == 1.0,
            "sample_output": results[0]
        }
