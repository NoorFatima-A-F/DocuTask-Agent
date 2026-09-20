# Cross-Region Replication & Conflict Resolution

## 1. Replication Modes
- **SYNCHRONOUS**: Zero RPO ($RPO = 0s$). Writes acknowledge only after quorum of regions acknowledge. Suitable for metadata catalogs and tenant security credentials.
- **ASYNCHRONOUS**: Ultra-low latency ($RPO < 10s$). Changes streamed via delta batches. Suitable for document embeddings and intermediate processing stages.
- **SEMI_SYNCHRONOUS**: Primary waits for at least 1 secondary region confirmation before client acknowledgement.

## 2. Deterministic Conflict Resolution Strategies
```
Replication Conflict Detected
          │
          ├──> [LAST_WRITE_WINS] : Highest timestamp / highest version tie-breaker
          ├──> [VECTOR_CLOCK]    : Causal dominance resolution
          ├──> [QUORUM_BASED]    : Majority consensus across distributed nodes
          └──> [MANUAL_REVIEW]   : Divergent states flagged for human operator resolution
```
