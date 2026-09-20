# Scheduler Diagnostics and Explainability Guide

## Transparent Placement Decisions
Every placement attempt generates an immutable `SchedulingDecision` containing:
- Selected Region, Cluster, and Worker
- Candidate counts and score breakdown
- Granular rejection reasons for all rejected worker candidates

## Inspecting Workload Diagnostics via SDK
```python
from app.infrastructure.sdk.scheduling import SchedulingSDK

sdk = SchedulingSDK()
report = sdk.diagnostics("wkl-ocr-100")
print("Is Scheduled:", report.is_scheduled)
print("Placement:", report.selected_placement)
print("Blocking Reasons:", report.blocking_reasons)
```
