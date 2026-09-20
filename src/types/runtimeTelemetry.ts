/**
 * Runtime Observability & Real Execution Telemetry Domain Types
 * 
 * Production-grade event models, derived metrics with mathematical formulas,
 * agent status telemetry with dynamic heartbeats, OpenTelemetry trace structures,
 * and deterministic replay snapshots.
 */

import type { AgentRoleType, ZeroFabricationSentinel } from '../components/agent';

export interface RuntimeEventPayload {
  [key: string]: any;
}

export interface RuntimeEventMetadata {
  [key: string]: any;
}

export interface RuntimeEvent {
  event_id: string;
  mission_id: string;
  parent_event_id: string | null;
  timestamp: string; // ISO 8601 UTC
  sequence_number: number;
  agent_id: string | null;
  worker_id: string | null;
  event_type: string;
  payload: RuntimeEventPayload;
  metadata: RuntimeEventMetadata;
  correlation_id: string;
  causation_id: string | null;
  trace_id: string;
  span_id: string | null;
  duration_ms: number | null;
  status: 'COMPLETED' | 'STARTED' | 'FAILED' | 'SKIPPED' | 'PAUSED' | 'RESUMED' | 'CANCELLED';
  version: string;
}

export interface DerivedMetric<T = number | string> {
  value: T;
  formatted: string;
  derivation_formula: string;
  sample_size: number;
  provenance_event_ids: string[];
  sentinel_state: ZeroFabricationSentinel | null;
}

export interface MissionMetricsSummary {
  mission_id: string;
  duration: DerivedMetric<number>;
  worker_utilization: DerivedMetric<number>;
  planner_throughput: DerivedMetric<number>;
  retry_rate: DerivedMetric<number>;
  reflection_frequency: DerivedMetric<number>;
  memory_hit_rate: DerivedMetric<number>;
  task_completion_rate: DerivedMetric<number>;
  overall_confidence: DerivedMetric<number>;
  average_latency: DerivedMetric<number>;
}

export interface RuntimeAgentStatus {
  agent_id: string;
  name: string;
  role: AgentRoleType;
  operational_state: 'IDLE' | 'THINKING' | 'EXECUTING' | 'WAITING' | 'PAUSED' | 'FAILED';
  current_task_id: string | null;
  current_goal: string;
  current_activity: string;
  queue_depth: number;
  tokens_processed: number;
  tasks_completed_count: number;
  tasks_failed_count: number;
  reflection_count: number;
  last_decision_title: string;
  last_decision_confidence: number | null;
  last_heartbeat_utc: string;
  heartbeat_frequency_hz: number;
  dynamic_heartbeat_interval_ms: number;
  is_stalled: boolean;
  sentinel_state: ZeroFabricationSentinel | null;
}

export interface RuntimeDagNode {
  node_id: string;
  mission_id: string;
  label: string;
  node_type: 'GOAL' | 'SUBGOAL' | 'TASK' | 'EXECUTION_UNIT' | 'EVIDENCE' | 'PUBLICATION';
  status: 'PENDING' | 'IN_PROGRESS' | 'COMPLETED' | 'FAILED' | 'SKIPPED';
  assigned_agent: AgentRoleType;
  dependencies: string[];
  retry_count: number;
  runtime_seconds: number;
  artifacts_produced: string[];
  sha256_digest: string;
}

export interface RuntimeMissionState {
  mission_id: string;
  goal: string;
  current_state: string;
  total_events: number;
  total_tasks: number;
  completed_tasks: number;
  failed_tasks: number;
  retries: number;
  memory_lookups: number;
  memory_hits: number;
  reflection_events: number;
  latest_confidence: number;
  latest_thought: string;
  latest_thought_agent: string;
  dag_nodes: RuntimeDagNode[];
}

export interface ReplaySnapshotState {
  mission_id: string;
  target_sequence_step: number;
  reconstructed_at_utc: string;
  current_state: string;
  active_agent_id: string;
  confidence_score: number;
  completed_tasks: number;
  total_tasks: number;
  last_thought_text: string;
  events_processed_count: number;
  dag_node_states: Record<string, string>;
  memory_recalled_count: number;
}

export interface TraceSpanNode {
  span_id: string;
  trace_id: string;
  parent_span_id: string | null;
  event: RuntimeEvent;
  duration_ms: number;
  children: TraceSpanNode[];
}