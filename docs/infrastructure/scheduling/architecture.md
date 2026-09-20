# Global Execution Scheduling Architecture

## Overview
The DocuTask Agent Execution Scheduling Platform coordinates workload placement across multi-cloud and Kubernetes clusters using a two-tier scheduling topology:

```
Workload Submission
        ↓
Global Scheduler (Data Residency & Regional Policy)
        ↓
Regional Scheduler (Cluster Selection & Worker Placement)
        ↓
Constraint Filtering & Placement Scoring
        ↓
Two-Phase Capacity Reservation
        ↓
Single-Owner Execution Lease Issuance
        ↓
Worker Assignment & Dispatch
```

## Tier Responsibilities
- **Global Scheduler**: Determines eligible regions based on data residency, tenant regional pinning, compliance profiles, and coarse regional capacity.
- **Regional Scheduler**: Discovers active clusters and candidate workers in the region, evaluates hard constraints, computes multi-factor scores, reserves resources atomically, issues execution leases, and tracks assignments.
