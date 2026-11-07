"""Live smoke test: extract the Contoso test invoice with the real Gemini API.

Requires GEMINI_API_KEY (or GOOGLE_API_KEY) in the environment or .env. Not run in CI.
Exits non-zero if the call fails or any expected field is wrong.

    python tooling/smoke_gemini.py [--model gemini-3.8-flash]
"""

from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.ai.prompt_builder import PromptBuilder  # noqa: E402
from app.ai.providers.gemini import GeminiProvider  # noqa: E402
from app.ai.validator import AIValidator  # noqa: E402
from app.core.errors.extraction import LLMError  # noqa: E402
from tests.fakes.data import CONTOSO_INVOICE_TEXT  # noqa: E402

EXPECTED = {
    "vendor_name": "Contoso Ltd",
    "invoice_number": "A-7731",
    "total_amount": 42.10,
    "currency": "EUR",
    "tax_amount": 7.00,
}


async def main(model: str | None) -> int:
    provider = GeminiProvider(default_model_name=model)
    print(f"model: {provider.default_model}")
    try:
        result = await provider.generate_json(
            PromptBuilder.build_prompt(CONTOSO_INVOICE_TEXT, "invoice"),
            PromptBuilder.get_json_schema("invoice"),
            PromptBuilder.build_system_instruction("invoice"),
        )
    except LLMError as exc:
        print(f"FAILED: {exc.error_code}: {exc.message}")
        return 2
    data, _ = AIValidator.validate(result.data, "invoice")
    print(f"tokens: in={result.input_tokens} out={result.output_tokens}")
    print(f"cost:   {provider.calculate_cost(result.input_tokens, result.output_tokens)}")
    failures = 0
    for field, want in EXPECTED.items():
        got = data.get(field)
        ok = abs(got - want) < 0.005 if isinstance(want, float) and isinstance(got, (int, float)) else got == want
        failures += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {field}: {got!r} (expected {want!r})")
    return 1 if failures else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=None)
    sys.exit(asyncio.run(main(parser.parse_args().model)))
