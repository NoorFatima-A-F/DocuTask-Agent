# Enterprise Verification Naming & Architecture Standards

1. **Modules**: Snake_case directory (`modules/ocr_verification/`).
2. **Entities & Value Objects**: PascalCase noun phrases (`VerificationDefinition`, `QualityGateResult`).
3. **Use Cases**: PascalCase verb phrases (`ManageVerificationRunUseCase`).
4. **Repositories**: `InMemory{Entity}Repository`, `Postgres{Entity}Repository`.
5. **Events**: Past tense PascalCase (`VerificationCompletedDomainEvent`).
6. **Interfaces**: Suffix `Interface` (`VerificationRepositoryInterface`).
