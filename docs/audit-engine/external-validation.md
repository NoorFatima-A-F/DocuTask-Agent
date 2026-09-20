# External Reality Validation & Dynamic Probe Architecture

## Overview

The **External Reality Validation** framework (`enterprise_audit_engine/external_validation`) acts as an independent out-of-band verification layer. It confirms that the system's runtime behavior, network endpoints, transaction persistence, and active defenses match the claims made in internal code and static audit evidence.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        REALITY VALIDATION ENGINE                       │
├──────────────────┬──────────────────────┬──────────────────────────────┤
│  API VALIDATOR   │  DATABASE VALIDATOR  │  SECURITY REALITY VALIDATOR  │
│ - Live Endpoint  │ - Isolation Levels   │ - Mass Assignment Injection  │
│ - Auth Guarding  │ - Rollback Atomicity │ - JWT 'none' Alg Probe       │
│ - Schema Conform │ - Connection Pool    │ - Path Traversal Probe       │
│ - Timeout & Rate │ - Persistence State  │ - CORS Permissiveness        │
└────────┬─────────┴──────────┬───────────┴──────────────┬───────────────┘
         │                    │                          │
         ▼                    ▼                          ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      VALIDATION ASSERTION REGISTRY                     │
│  - Captures Reality Assertions with Evidence Fingerprints              │
│  - Cryptographic Verification of Observed vs Expected State           │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        CONTRADICTION DETECTOR                          │
│  Rule: If Internal == PASS and Reality == FAIL:                        │
│        ==> FINAL VERDICT: CERTIFICATION_REJECTED                       │
│        ==> Non-Overridable Reality Supremacy                           │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 1. Core Reality Validation Components

### 1.1 API Reality Validator (`ApiRealityValidator`)
Inspects live and simulated HTTP/REST endpoints against contract definitions and security boundaries:
- **Authentication Enforcement**: Probes protected endpoints without credentials and asserts `401 Unauthorized` or `403 Forbidden` responses.
- **Contract Schema Validation**: Validates JSON response structures, content-types, and headers against OpenAPI/JSONSchema definitions.
- **Rate-Limiting and Timeout Probes**: Emits burst traffic and delayed calls to verify reverse-proxy and gateway throttles.

### 1.2 Database Reality Validator (`DatabaseRealityValidator`)
Directly verifies ACID guarantees, transactional boundaries, and state persistence:
- **Transaction Rollback Atomicity**: Injects intentional execution failures mid-transaction and queries the database engine to prove zero residual writes exist.
- **Session Isolation & Concurrency**: Validates dirty reads, non-repeatable reads, and phantom reads under read-committed or serializable isolation settings.
- **Connection Pool Exhaustion**: Verifies that connection acquisition adheres to bounded pools without resource starvation.

### 1.3 Security Reality Validator (`SecurityRealityValidator`)
Executes real-world dynamic adversarial attack probes against running or emulated services:
- **Mass Assignment Vulnerabilities**: Injects privileged fields (e.g., `{"is_admin": true, "role": "superuser"}`) during standard entity updates.
- **JWT Cryptographic Downgrade**: Submits authentication tokens with `{"alg": "none"}` or altered HMAC keys.
- **Path Traversal & Injection**: Transmits canonicalized traversal sequences (`../../etc/passwd`, `..\..\windows\win.ini`) to file upload and retrieval handlers.
- **Permissive CORS & Header Inspection**: Inspects `Access-Control-Allow-Origin: *` with credentials enabled.

---

## 2. Contradiction Detection & Non-Overridable Rule

The `ContradictionDetector` evaluates internal evidence collection vs. external reality validation results:

$$\text{Verdict} = \begin{cases} \text{CERTIFICATION\_REJECTED}, & \text{if } \exists c \in \text{Checks}: \text{Internal}(c) = \text{PASS} \land \text{Reality}(c) = \text{FAIL} \\ \text{CERTIFIED}, & \text{otherwise} \end{cases}$$

> [!CAUTION]
> **Reality Supremacy Rule**: No internal collector score, unit test pass rate, or static code analysis claim can override an observed external failure. Any contradiction results in an immediate and non-overridable `CERTIFICATION_REJECTED` verdict.
