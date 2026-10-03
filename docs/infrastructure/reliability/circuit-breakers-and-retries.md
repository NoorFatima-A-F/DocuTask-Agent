# Circuit Breakers, Bulkheads & Retry Policies

## 1. Circuit Breaker Semantics
- **CLOSED**: All traffic permitted. Consecutive failures or error rates beyond threshold trip to `OPEN`.
- **OPEN**: All calls fast-failed immediately or directed to `fallback_fn`. Cooldown timer governs transition to `HALF_OPEN`.
- **HALF_OPEN**: Controlled canary trial requests. If trial requests succeed without failure, breaker resets to `CLOSED`; if any trial fails, breaker trips back to `OPEN`.

## 2. Retry Strategies
| Strategy | Formula | Typical Use Case |
|---|---|---|
| `IMMEDIATE` | $delay = 0$ | Fast in-memory operations, local lock contention |
| `LINEAR` | $delay = t_0 \times (attempt + 1)$ | Internal service calls with predictable recovery |
| `EXPONENTIAL` | $delay = t_0 \times 2^{attempt}$ | Cloud API dependencies, external webhooks |
| `RANDOMIZED_JITTER` | $delay = t_{base} \pm U(-\delta, \delta)$ | Preventing thundering herd on shared resource recovery |
| `ADAPTIVE` | $delay = t_{base} \times (1 + 0.2 \times errors) + jitter$ | Self-healing under persistent high congestion |

## 3. Bulkhead Concurrency Isolation
Bulkheads isolate thread pools and concurrency limits per downstream dependency, ensuring slow or hung external dependencies cannot starve CPU/memory resources of unaffected workloads.
