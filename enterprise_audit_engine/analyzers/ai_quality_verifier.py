"""AI / LLM Pipeline Quality & Robustness Verifier."""

import os
from pathlib import Path
from typing import Dict, Any, List


class AIQualityVerifier:
    """Verifies AI/LLM pipeline components, fallback handlers, token tracking, and eval harnesses."""

    @staticmethod
    def analyze_ai_subsystem(repo_root: Path) -> Dict[str, Any]:
        ai_dirs = [
            repo_root / "app" / "services" / "ai",
            repo_root / "app" / "ai",
            repo_root / "app" / "agents",
            repo_root / "app" / "services" / "llm",
            repo_root / "app" / "services" / "ocr",
            repo_root / "app" / "services",
        ]

        total_ai_files = 0
        has_prompt_templates = False
        has_fallback_handling = False
        has_token_tracking = False
        has_structured_output = False
        has_retry_logic = False
        has_ground_truth_evals = False
        detected_models: List[str] = []

        eval_dir = repo_root / "tests" / "evals"
        if eval_dir.exists() and any(eval_dir.iterdir()):
            has_ground_truth_evals = True

        for target_dir in ai_dirs:
            if not target_dir.exists():
                continue
            for root, _, files in os.walk(target_dir):
                for f in files:
                    if f.endswith(".py"):
                        total_ai_files += 1
                        file_path = Path(root) / f
                        try:
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as fp:
                                content = fp.read()
                                lower_content = content.lower()

                                if "prompt" in lower_content or "system_message" in lower_content:
                                    has_prompt_templates = True
                                if "fallback" in lower_content or "except" in lower_content and ("openai" in lower_content or "gemini" in lower_content or "llm" in lower_content):
                                    has_fallback_handling = True
                                if "token" in lower_content or "usage" in lower_content:
                                    has_token_tracking = True
                                if "response_format" in lower_content or "pydantic" in lower_content or "schema" in lower_content:
                                    has_structured_output = True
                                if "retry" in lower_content or "tenacity" in lower_content or "backoff" in lower_content:
                                    has_retry_logic = True

                                for model_name in ["gpt-4", "gpt-3.5", "gemini-1.5", "gemini-2.0", "claude-3", "tesseract", "easyocr"]:
                                    if model_name in lower_content and model_name not in detected_models:
                                        detected_models.append(model_name)
                        except Exception:
                            pass

        maturity = "LOW"
        if has_structured_output and has_fallback_handling and has_retry_logic:
            maturity = "HIGH" if has_ground_truth_evals else "MEDIUM"

        return {
            "total_ai_files": total_ai_files,
            "detected_models": detected_models,
            "has_prompt_templates": has_prompt_templates,
            "has_fallback_handling": has_fallback_handling,
            "has_token_tracking": has_token_tracking,
            "has_structured_output": has_structured_output,
            "has_retry_logic": has_retry_logic,
            "has_ground_truth_evals": has_ground_truth_evals,
            "ai_pipeline_maturity": maturity,
        }
