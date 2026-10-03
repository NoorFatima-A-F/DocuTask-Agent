# Architecture Decision Record: ADR-004

## Title
Extensible Plugin & Connector Architecture: Decoupled Manifests, WebAssembly Sandboxing, and Zero-Hardcoded Integrations

## Status
**ACCEPTED** (2026-03-24)

## Context
DocuTask Agent operates across complex enterprise application ecosystems requiring bidirectional connectivity with Enterprise Resource Planning (ERP like SAP S/4HANA, NetSuite), Customer Relationship Management (Salesforce, HubSpot), Electronic Health Records (Epic, Cerner), Document Management (SharePoint, Box), and custom line-of-business systems.

In legacy monolithic systems, enterprise connectors are built directly into core service codebases. This approach causes severe architectural degradation:
1. **Monolithic Coupling**: Changes to a third-party API specification (e.g., Salesforce OAuth token rotation) require deploying the entire core platform.
2. **Security Vulnerability**: Untrusted third-party code runs within the core process memory space, exposing sensitive platform tokens and memory state.
3. **Release Rigidity**: Customers and partners cannot develop custom internal connectors without upstream platform source access.
4. **Failure Cascades**: A memory leak or blocking network call in an integration driver can crash core agent execution threads.

DocuTask Agent requires a zero-hardcoding, isolated, and standardized plugin architecture that allows core platform services, third-party developers, and enterprise customers to author, test, and deploy integrations securely.

---

## Decision

We adopt a **Decoupled Plugin & Connector Architecture** based on standardized manifests, WebAssembly (WASM) / secure micro-VM sandboxing, and universal interface contracts:

### 1. Zero Hardcoding Mandate
Core domain and application layers (`app/core/`, `app/domain/`) shall contain ZERO vendor-specific SDKs, client libraries, or hardcoded integration endpoints. All external system communication is mediated through the Plugin & Connector SDK.

### 2. Standardized Plugin Manifest (`plugin.json`)
Every plugin is packaged as an immutable, cryptographically signed bundle with a declarative manifest specifying:
- Semantic identity (`id`, `version`, `name`, `author`)
- Required permissions & capabilities (`network_egress_domains`, `secret_access`, `filesystem_access`)
- Lifecycle hooks (`on_install`, `on_enable`, `on_disable`, `on_uninstall`)
- Extension points (Connectors, Trigger Handlers, Skill Actions, Extraction Extractors)
- Configuration JSONSchema with automated UI rendering metadata.

### 3. Unified Connector Interface (`IConnector`)
All external system connectors must implement the asynchronous `IConnector` protocol:
- `connect(config, auth_context) -> ConnectionHandle`
- `authenticate() -> AuthResult`
- `health_check() -> HealthStatus`
- `execute_action(action_name, parameters) -> ActionResult`
- `query_records(query_spec) -> RecordStream`
- `listen_events(event_filter) -> EventStream`
- `disconnect() -> None`

### 4. Sandbox Isolation (WASM / Ephemeral Containers)
- Lightweight plugins (data formatters, custom validation rules, transformation scripts) run inside a high-speed **WebAssembly (Wasmtime) sandbox** with sub-millisecond cold starts and strictly bounded memory (maximum 64MB).
- Heavyweight connectors (requiring proprietary native binary drivers or high-throughput network streaming) run inside isolated ephemeral container sandboxes with non-root privileges, read-only root filesystems, and strict network egress firewalls.

### 5. Plugin Registry & Dynamic Discovery
Plugins are published to an immutable OCI-compliant Plugin Registry with cryptographic signature verification (Sigstore/Cosign), automated vulnerability scanning (Trivy), and dynamic hot-reloading at runtime without platform downtime.

---

## Consequences

### Positive
- **Fault Isolation**: Faults, crashes, and memory leaks in connector code cannot corrupt or crash core DocuTask platform engines.
- **Enterprise Extensibility**: Enterprise IT teams can author internal proprietary plugins and deploy them to their private tenant registry without core codebase modifications.
- **Zero-Downtime Updates**: Connectors and plugins can be updated, patched, and rolled back dynamically per workspace.
- **Auditable Security**: Granular, declarative permission boundaries prevent data exfiltration and restrict network egress exclusively to approved vendor API endpoints.

### Negative / Trade-Offs
- **Serialization Overhead**: Inter-process communication between core agent workers and plugin sandboxes introduces minor serialization latency (typically <2ms via shared memory / gRPC).
- **SDK Maintenance**: The platform engineering team must maintain and document robust Plugin SDKs across supported runtime languages (Python, TypeScript, Rust/WASM).

---

## Alternatives Considered

1. **In-Process Python Modules / Dynamic `importlib`**: Rejected due to catastrophic security risks (unbounded memory access, access to `os.environ` secrets) and crash propagation to worker processes.
2. **External Microservices per Connector**: Rejected due to extreme infrastructure overhead and deployment complexity when supporting 100+ connectors across thousands of customer tenants.
3. **Hardcoded Monolithic Adapters**: Rejected due to high maintenance burden, release velocity bottlenecks, and violation of Clean Architecture principles.
