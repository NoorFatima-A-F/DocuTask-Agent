# Reliability Lifecycle State Machine

## 1. State Model
The platform tracks reliability lifecycles across 7 strictly governed states:

```mermaid
stateDiagram-v2
    [*] --> OPTIMAL
    OPTIMAL --> DEGRADED : Latency/Error Spikes
    OPTIMAL --> FAILING : RTO Breach Warning
    OPTIMAL --> OUTAGE : Complete Disconnection
    DEGRADED --> OPTIMAL : Telemetry Normalized
    DEGRADED --> FAILING : Escalating Errors
    DEGRADED --> PARTIALLY_FAILED : Subsystem Failure
    DEGRADED --> OUTAGE : Cascading Outage
    DEGRADED --> RECOVERING : Auto-Remediation Initiated
    FAILING --> OUTAGE : Threshold Breached
    FAILING --> PARTIALLY_FAILED : Partial Loss
    FAILING --> RECOVERING : Recovery Triggered
    PARTIALLY_FAILED --> RECOVERING : Recovery Triggered
    OUTAGE --> RECOVERING : Recovery Triggered
    RECOVERING --> RECOVERED : Verification Passed
    RECOVERING --> FAILING : Recovery Aborted
    RECOVERED --> OPTIMAL : Soak Period Cleared
    RECOVERED --> DEGRADED : Residual Latency
```

## 2. Invariants & Transition Rules
1. **No-Skip Invariant**: Cannot transition directly from `OUTAGE` or `PARTIALLY_FAILED` to `OPTIMAL` without passing through `RECOVERING` and `RECOVERED`.
2. **Audit Requirement**: Every transition generates an immutable `ReliabilityTransitionRecord` including trigger source, reason, and telemetry snapshot.
