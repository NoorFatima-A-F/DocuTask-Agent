# ADR-702: Tenant Hierarchy Design

## Status
Accepted

## Context
Enterprise organizations require internal organizational structures and boundaries (departments, staging/production environments, and autonomous project teams) within a single billing tenant.

## Decision
Establish a strict 4-level tenant containment hierarchy:
$$\text{Organization} \longrightarrow \text{Workspace} \longrightarrow \text{Project} \longrightarrow \text{Environment}$$

- **Organization**: Primary legal entity, billing account, subscription tier, and white-label branding root.
- **Workspace**: Departmental boundary owning agents, workflows, knowledge spaces, and connectors.
- **Project**: Deployment boundary grouping specific agent swarms and workflow DAGs.
- **Environment**: Runtime execution partition (`Development`, `QA`, `Staging`, `Production`, `Sandbox`) with isolated variables and secrets.

## Consequences
- **Positive**: Clean organizational governance and environment separation (e.g. Prod Gmail connector $\neq$ Dev Gmail connector).
- **Trade-off**: Requires hierarchical permission resolution across multiple boundary levels.
