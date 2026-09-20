# Enterprise Event-Driven Architecture & CloudEvents Mesh Specification

## 1. CloudEvents 1.0 Envelope Schema

Every state change and asynchronous invocation in DocuTask Agent is emitted as a strictly typed, immutable event adhering to the **CloudEvents 1.0** specification.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "type": "object",
  "required": [
    "specversion",
    "event_id",
    "event_type",
    "source",
    "timestamp",
    "organization_id",
    "workspace_id",
    "correlation_id",
    "actor",
    "data"
  ],
  "properties": {
    "specversion": { "type": "string", "const": "1.0" },
    "event_id": { "type": "string", "format": "uuid" },
    "event_type": { "type": "string", "pattern": "^[a-z0-9]+\\.[a-z0-9_]+\\.[a-z0-9_]+$" },
    "source": { "type": "string", "format": "uri" },
    "timestamp": { "type": "string", "format": "date-time" },
    "organization_id": { "type": "string" },
    "workspace_id": { "type": "string" },
    "environment_id": { "type": "string", "default": "production" },
    "correlation_id": { "type": "string", "format": "uuid" },
    "causation_id": { "type": "string", "format": "uuid" },
    "actor": {
      "type": "object",
      "required": ["type", "id"],
      "properties": {
        "type": { "type": "string", "enum": ["USER", "AGENT", "SYSTEM", "CONNECTOR"] },
        "id": { "type": "string" },
        "name": { "type": "string" }
      }
    },
    "data": { "type": "object" },
    "version": { "type": "string", "default": "1.0.0" }
  }
}
```

---

## 2. Distributed Event Mesh Topology

```mermaid
graph TD
    subgraph "Producers"
        P1[API Gateway]
        P2[Workflow Engine]
        P3[Agent Mesh]
        P4[Connector Webhooks]
    end

    subgraph "Event Mesh (Apache Kafka / RabbitMQ)"
        BUS[Event Ingestion Router]
        TOPIC_WF[Topic: docutask.workflows]
        TOPIC_AGT[Topic: docutask.agents]
        TOPIC_DOC[Topic: docutask.documents]
        TOPIC_SEC[Topic: docutask.security]
        TOPIC_AUD[Topic: docutask.audit]
        DLQ[Dead-Letter Queue (DLQ)]
    end

    subgraph "Consumers"
        C1[Workflow Orchestrator]
        C2[Agent Worker Nodes]
        C3[Real-time Analytics Engine]
        C4[Audit Logging Vault]
        C5[Notification Dispatcher]
    end

    P1 & P2 & P3 & P4 --> BUS
    BUS --> TOPIC_WF & TOPIC_AGT & TOPIC_DOC & TOPIC_SEC & TOPIC_AUD
    BUS -.->|Failed Deserialization| DLQ
    TOPIC_WF --> C1 & C3 & C4
    TOPIC_AGT --> C2 & C3
    TOPIC_DOC --> C1 & C2
    TOPIC_SEC --> C4 & C5
    TOPIC_AUD --> C4
```

---

## 3. The 9 Enterprise Event Categories & Complete Event Catalog

### 1. Workflow Events (`docutask.workflow.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `workflow.definition.published` | A new workflow definition version is published | `workflow_id`, `version`, `author_id` |
| `workflow.execution.started` | A workflow instance begins execution | `execution_id`, `workflow_id`, `trigger_event_id` |
| `workflow.stage.entered` | A workflow stage begins | `execution_id`, `stage_id`, `stage_name` |
| `workflow.step.completed` | A workflow step completes successfully | `execution_id`, `step_id`, `output_summary` |
| `workflow.execution.paused` | Workflow pauses waiting for external input | `execution_id`, `step_id`, `pause_reason` |
| `workflow.execution.resumed` | Workflow resumes after input received | `execution_id`, `resumed_by_event_id` |
| `workflow.execution.failed` | Workflow terminates due to unhandled error | `execution_id`, `error_code`, `stack_trace` |
| `workflow.execution.completed` | Workflow finishes all stages successfully | `execution_id`, `duration_ms`, `final_outputs` |

### 2. Agent Events (`docutask.agent.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `agent.turn.dispatched` | Coordinator assigns a task turn to an agent | `agent_id`, `mission_id`, `step_id` |
| `agent.planning.completed` | Planning Agent finishes causal execution DAG | `agent_id`, `plan_id`, `node_count` |
| `agent.tool.invoked` | Execution Agent invokes a discrete tool | `agent_id`, `tool_name`, `parameters_hash` |
| `agent.consensus.reached` | Multi-agent voting completes with majority | `mission_id`, `vote_ratio`, `winning_verdict` |
| `agent.reflection.logged` | Reflection Agent captures learned strategy | `agent_id`, `trajectory_id`, `reward_score` |

### 3. Document Events (`docutask.document.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `document.ingestion.uploaded` | New document binary uploaded to object storage | `document_id`, `filename`, `byte_size`, `mime_type` |
| `document.ocr.completed` | Layout-aware OCR finishes page text extraction| `document_id`, `page_count`, `ocr_engine` |
| `document.extraction.succeeded`| LLM extracts validated structured schema | `document_id`, `schema_type`, `field_count` |
| `document.validation.failed` | Extracted values fail business invariant check| `document_id`, `failed_fields`, `confidence` |

### 4. Security Events (`docutask.security.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `security.threat.detected` | Input sanitization detects prompt injection | `source_ip`, `attack_category`, `raw_prompt_hash` |
| `security.auth.failed` | Invalid JWT, expired token, or signature error | `client_id`, `ip_address`, `failure_reason` |
| `security.access.denied` | RBAC/ABAC policy engine denies access | `actor_id`, `resource_arn`, `policy_id` |
| `security.key.rotated` | Enterprise KMS envelope encryption key rotated| `key_id`, `version`, `rotated_at` |

### 5. Integration Events (`docutask.integration.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `connector.action.executed` | External ERP/CRM action finishes | `connector_id`, `destination_app`, `response_code` |
| `connector.rate_limited` | Third-party endpoint returns HTTP 429 | `connector_id`, `retry_after_seconds` |
| `connector.webhook.received` | Inbound webhook received from external service| `connector_id`, `webhook_id`, `payload_size` |

### 6. AI Events (`docutask.ai.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `ai.inference.requested` | Request sent to AI model provider | `model_name`, `provider`, `prompt_tokens` |
| `ai.inference.completed` | Response received from model provider | `model_name`, `completion_tokens`, `latency_ms` |
| `ai.cache.hit` | Request fulfilled from semantic prompt cache | `cache_key`, `similarity_score`, `saved_tokens` |
| `ai.budget.exceeded` | Monthly workspace token budget threshold met | `workspace_id`, `current_spend_usd`, `spend_cap` |

### 7. Human Events (`docutask.human.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `human.approval.requested` | Step creates task in operator review queue | `task_id`, `assigned_user_id`, `sla_deadline` |
| `human.approval.granted` | Operator approves task with optional edits | `task_id`, `approver_id`, `review_duration_sec` |
| `human.approval.rejected` | Operator rejects task with justification | `task_id`, `rejection_reason` |

### 8. Audit Events (`docutask.audit.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `audit.record.sealed` | WORM audit log block cryptographically sealed | `block_id`, `sha256_root`, `entry_count` |
| `audit.export.generated` | Compliance report package compiled | `export_id`, `compliance_standard`, `download_url` |

### 9. System Events (`docutask.system.*`)
| Event Type | Trigger Description | Core Payload Attributes |
| :--- | :--- | :--- |
| `system.node.healthy` | Heartbeat pulse emitted by worker node | `node_id`, `cpu_usage_pct`, `memory_usage_pct` |
| `system.disaster_recovery.initiated`| Automated failover to secondary cloud region | `primary_region`, `target_region`, `rto_target_sec` |
