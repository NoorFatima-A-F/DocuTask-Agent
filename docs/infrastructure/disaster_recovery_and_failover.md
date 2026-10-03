# Disaster Recovery and Regional Failover Guide

## Regional Failover Design
Each region can designate a paired `failover_region_id`. When a primary region becomes `DEGRADED` or `OFFLINE`, traffic is automatically routed to the designated standby failover region.

## Verification & Quorum
Consensus checks verify that a minimum quorum of healthy active regions exists before allowing configuration changes or epoch advancements.
