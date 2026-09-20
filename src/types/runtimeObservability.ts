/**
 * TypeScript Contracts for Autonomous Runtime Observability Layer (AROL).
 * Strictly mirrors backend schemas for 19 event categories, trace contexts,
 * live metrics, flame graphs, and mathematical health scoring.
 */

export type EventSeverity = 'DEBUG' | 'INFO' | 'WARNING' | 'ERROR' | 'CRITICAL';
export type EventPriority = 'CRITICAL' | 'HIGH' | 'NORMAL' | 'LOW';

export type EventCategory =
  | 'MISSION'
  | 'PLANNER'
  | 'EXECUTION'
  | 'WORKER'
  | 'RESOURCE'
  | 'MEMORY'
  | 'REFLECTION'
  | 'GOVERNANCE'
  | 'VALIDATION'
  | 'TOOL'
  | 'STORAGE'
  | 'COST'
  | 'SCHEDULER'
  | 'FAILURE'
  | 'RECOVERY'
  | 'HUMAN_REVIEW'
  | 'TELEMETRY'
  | 'BENCHMARK'
  | 'SYSTEM';

export interface TraceContextPayload {
  trace_id: string;
  span_id: string;
  parent_span_id?: string | null;
  execution_depth: number;
  component: string;
  operation: string;
  worker_id?: string | null;
  node_id?: string | null;
  timestamp_ns: number;
  baggage?: Record<string, string>;
}

export interface RuntimeEventPayload {
  event_id: string;
  category: EventCategory;
  event_type: string;
  mission_id: string;
  correlation_id: string;
  parent_event_id?: string | null;
  trace_context: TraceContextPayload;
  timestamp: number;
  duration_ms: number;
  agent_id?: string | null;
  worker_id?: string | null;
  node_id?: string | null;
  task_id?: string | null;
  stage: string;
  status: string;
  severity: EventSeverity;
  priority: EventPriority;
  payload: Record<string, any>;
  evidence: Record<string, any>;
  metadata: Record<string, any>;
  version: string;
  prev_event_hash?: string | null;
  event_hash?: string | null;
}

export interface AnomalyReportPayload {
  anomaly_id: string;
  metric_name: string;
  anomaly_type: string;
  severity: EventSeverity;
  observed_value: number;
  expected_mean: number;
  z_score: number;
  timestamp: number;
  details: string;
  root_cause_hint?: string | null;
}

export interface RuntimeHealthScorePayload {
  overall_score: number;
  is_healthy: boolean;
  component_scores: {
    failure_resilience: number;
    retry_stability: number;
    cpu_headroom: number;
    memory_headroom: number;
    queue_capacity: number;
  };
  active_anomalies: AnomalyReportPayload[];
  active_workers_count: number;
  queue_backlog: number;
  evaluated_at: number;
  provenance: Record<string, any>;
}

export interface FlameGraphNodePayload {
  name: string;
  value_ms: number;
  children: FlameGraphNodePayload[];
  component: string;
  span_id?: string | null;
  is_critical_path: boolean;
}

export interface MissionTimelineItemPayload {
  event_id: string;
  timestamp: number;
  stage: string;
  category: string;
  event_type: string;
  status: string;
  duration_ms: number;
  summary: string;
  evidence: Record<string, any>;
  event_hash?: string | null;
}

export interface RuntimeDashboardStatePayload {
  timestamp: number;
  health: RuntimeHealthScorePayload;
  resources: {
    cpu_pct: number;
    memory_rss_mb: number;
    memory_vms_mb: number;
    thread_count: number;
    active_async_tasks: number;
    timestamp: number;
  };
  metrics: Record<string, number>;
  derived: {
    node_success_rate: number;
    mission_success_rate: number;
    memory_hit_ratio: number;
    total_cost_usd: number;
    total_tokens: number;
  };
  active_workers: Array<{
    worker_id: string;
    status: string;
    last_stage: string;
    last_seen: number;
  }>;
  recent_events: RuntimeEventPayload[];
  anomalies: AnomalyReportPayload[];
  total_events_stored: number;
}
