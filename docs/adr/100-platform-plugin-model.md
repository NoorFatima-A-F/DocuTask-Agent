# 100. Platform Plugin Framework & Capability Sandboxing

Date: 2026-09-20

## Status
Accepted

## Context
Third-party extensions, custom deployment strategies, proprietary cloud adapters, and telemetry sinks must be supported without modifying the platform delivery kernel or bypassing governance.

## Decision
We implement `PlatformPlugin` with an explicit lifecycle (`DISCOVERED` -> `REGISTERED` -> `APPROVED` -> `ACTIVE` -> `DISABLED`) and strict `PluginSandbox` permission enforcement. Plugins must declare required permissions (`storage:read`, `telemetry:emit`, etc.) and cannot access unauthorized secrets or networks.

## Consequences
- Enables extensible ecosystem growth while enforcing strict multi-tenant and platform security invariants.
- Third-party extensions can be safely loaded and monitored in production.
