# ADR-947: Dynamic Operational Dashboard Architecture

## Status
Accepted

## Context
Operators and engineers require composable, role-specific visualizations (Executive SLO overview, SRE Infrastructure, AI LLM Inference runtime, Document Workflow orchestration) that render dynamically from backend telemetry queries without hardcoded frontends.

## Decision
We implement a declarative dashboard engine comprising:
1. Flexible data models (`Dashboard`, `DashboardPanel`, `DashboardWidget`, `WidgetType`).
2. Widget query evaluator (`WidgetQueryEvaluator`) supporting time-series graphs, single-value gauges, data tables, heatmaps, status grids, flamegraphs, and topology maps.
3. Pre-configured domain builders (`DashboardBuilder`) generating standardized SRE, AI Inference, and Workflow dashboards.
4. Exportable and importable JSON definitions allowing version control and automated provisioning.

## Consequences
- Declarative, API-accessible operational dashboards.
- Dynamic data binding directly against in-memory or exported metrics, logs, traces, and profiling data.
- Standardized layout across operational, engineering, and business user personas.
