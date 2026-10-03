# ADR-003: Queue Priority Strategy & Anti-Starvation Engine

**Status**: **ACCEPTED**  
**Date**: 2026-08-19  

## 1. Context & Problem Statement
Emergency documents and premium customer uploads must be processed ahead of standard batch uploads without starving low-priority background jobs.

## 2. Decision Outcome
Implement 3 priority queues (`HIGH`, `MEDIUM`, `LOW`) in `PriorityMessageBroker` ([app/jobs/broker.py](file:///C:/Users/User/Desktop/ai_document_processing_platform/app/jobs/broker.py)). Introduce an anti-starvation counter that forces dequeueing from the `LOW` queue after every 10 consecutive `HIGH`/`MEDIUM` job executions.

## 3. Consequences
- **Positive**: High-priority jobs achieve sub-30ms queue latency; low-priority jobs are guaranteed progress without starvation.
