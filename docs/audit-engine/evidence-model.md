# Evidence Model & Schema Specification

## Evidence Record Schema
Every evidence item collected by the engine adheres to the immutable `EvidenceRecord` Pydantic v2 data contract:

```python
class EvidenceRecord(BaseModel):
    id: str                                  # Unique Identifier (e.g. EV-8A1C92B4)
    category: str                            # Functional Subsystem
    collector: str                           # Originating Collector
    source_type: EvidenceSourceType          # STATIC_SOURCE, CONFIG, TEST, RUNTIME
    timestamp: str                           # ISO-8601 UTC Timestamp
    command: Optional[str]                   # Shell/Verification command executed
    environment: Dict[str, Any]              # OS, Python, and Tool versions
    exit_code: Optional[int]                 # Process exit code
    duration_ms: float                       # Collection duration in milliseconds
    artifact_paths: List[str]                # Local paths to raw logs/dumps
    raw_payload: Dict[str, Any]              # Extracted AST/JSON dictionary payload
    summary: str                             # Concise human-readable summary
    confidence: EvidenceConfidence           # Deterministic confidence rating
    classification: EvidenceClassification   # Standardized maturity classification
    content_hash: str                        # Cryptographically sealed SHA-256 fingerprint
```

## Evidence Sources
1. **`STATIC_SOURCE_CODE`**: AST code traversal, class definitions, function signatures.
2. **`CONFIGURATION_FILE`**: Dockerfile, YAML manifests, pyproject.toml, .gitignore.
3. **`AUTOMATED_TEST_EXECUTION`**: Pytest assertions, unit/integration results.
4. **`RUNTIME_EXECUTION`**: Live container healthchecks, process memory/CPU metrics.
