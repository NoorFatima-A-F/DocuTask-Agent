# Enterprise Naming Standards & Conventions

## 1. Directory & Package Naming
- **Rule**: Lowercase alphanumeric words separated by single underscores (`snake_case`).
- **Standard**: Meaningful capability nouns (e.g., `verification_engine`, `dataset_management`, `quality_gates`).
- **Forbidden**: `misc`, `helpers`, `common2`, `temp`, `stuff`, `new_code`.

## 2. Domain Events
- **Rule**: PascalCase in past-tense (e.g., `VerificationCreated`, `ExecutionStarted`, `EvidenceCollected`, `CertificationIssued`).

## 3. REST API Endpoints
- **Rule**: Pluralized, versioned lowercase nouns (e.g., `/api/v1/verifications`, `/api/v1/executions`).
