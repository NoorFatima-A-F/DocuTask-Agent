# Placement Pipeline Guide

## Pipeline Stages
1. **Submission & Validation**: Validates schema and requirements.
2. **Global Region Selection**: Evaluates data residency and tenant affinity to filter and rank regions.
3. **Cluster Filtering**: Validates cluster health, supported workloads, and tenant cluster affinity.
4. **Worker Candidate Filtering**: Eliminates workers failing hard constraints (capabilities, CPU/RAM/GPU, concurrency limits, lease validity).
5. **Candidate Scoring**: Evaluates resource headroom, optional capability match bonus, affinity tags, and load.
6. **Capacity Reservation**: Atomically reserves CPU, RAM, GPU, and slots on the selected worker.
7. **Execution Lease**: Issues a single-owner lease for the execution attempt.
8. **Assignment Dispatch**: Dispatches the task to the worker and transitions workload state to `ASSIGNED`.
