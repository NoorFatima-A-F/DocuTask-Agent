# LLM Provider Architecture Specification

**Subsystem**: Provider Interface & Decoupling Layer  
**Path**: `C:\Users\User\Desktop\ai_document_processing_platform\app\ai\base.py`  

---

## 1. Provider Interface Contract

All LLM providers must implement `LLMProvider`:

```python
class LLMProvider(ABC):
    @property
    def provider_name(self) -> str: ...
    @property
    def default_model(self) -> str: ...
    async def generate(self, prompt: str, system_instruction: str = "", model: str = "") -> str: ...
    async def generate_json(self, prompt: str, json_schema: Dict[str, Any], system_instruction: str = "", model: str = "") -> Tuple[Dict, str, int, int]: ...
    async def health_check(self) -> bool: ...
    def supports_model(self, model_name: str) -> bool: ...
    def supports_streaming(self) -> bool: ...
    def estimate_tokens(self, text: str) -> int: ...
    def calculate_cost(self, input_tokens: int, output_tokens: int, model: str = "") -> float: ...
```

---

## 2. Zero-Code-Change Cloud Expansion Roadmap

Adding a new provider (e.g. `ClaudeProvider` or `OpenAIProvider`) requires only:
1. Creating `app/ai/providers/claude.py` implementing `LLMProvider`.
2. Registering in `LLMRegistry.register_provider("claude", ClaudeProvider)`.
3. Business logic services and API routers remain 100% unchanged.
