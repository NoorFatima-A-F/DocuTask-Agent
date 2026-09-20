# Evidence Classification & Confidence Policy

## Controlled Classification Ontology

| Classification | Meaning | Required Evidence |
| :--- | :--- | :--- |
| **`VERIFIED`** | Fully proven by source code and automated test execution. | `STATIC_SOURCE_CODE` + `AUTOMATED_TEST_EXECUTION` (pass) |
| **`VERIFIED_BY_EXECUTION`** | Proven by live runtime execution in a container/environment. | `RUNTIME_EXECUTION` (exit 0) |
| **`VERIFIED_BY_STATIC_ANALYSIS`** | Proven by AST code inspection and type checks. | `STATIC_SOURCE_CODE` |
| **`VERIFIED_BY_CONFIGURATION`** | Proven by verified declarative configuration files. | `CONFIGURATION_FILE` |
| **`CONFIGURATION_PRESENT_RUNTIME_NOT_VERIFIED`** | Manifests exist, but live runtime execution was not performed. | `CONFIGURATION_FILE` |
| **`PARTIALLY_VERIFIED`** | Implementation exists with warnings or partial test coverage. | Incomplete tests or non-zero exit code |
| **`DOCUMENTATION_ONLY`** | Specified in markdown/ADR, but no active source code exists. | Documentation file only |
| **`CRITICAL_FINDING`** | Security vulnerability or secret exposure identified. | Scan detection |

## Deterministic Confidence Levels
- **`VERY_HIGH`**: Subsystem verified via live runtime execution or benchmarks.
- **`HIGH`**: Subsystem verified via static source code + automated passing test suites.
- **`MEDIUM`**: Subsystem verified via static source code inspection only.
- **`LOW`**: Subsystem verified via configuration manifests or documentation only.
- **`NONE`**: Subsystem has zero verifiable evidence.
