/**
 * DocuTask Agent - Phase 3 (ESMR)
 * Event-Sourced Mission Replay, Decision Provenance & Enterprise Audit Platform Types
 */

export type ReplaySpeed = '0.25x' | '0.5x' | '1x' | '2x' | '4x' | '8x' | '16x' | 'INSTANT';

export type PlayerStatus = 'STOPPED' | 'PLAYING' | 'PAUSED' | 'SEEKING' | 'REVERSING' | 'COMPLETED' | 'ERROR';

export type BookmarkType = 'USER' | 'CHECKPOINT' | 'DECISION' | 'MUTATION' | 'FAILURE' | 'REPLAN' | 'APPROVAL' | 'REVERSAL';

export interface ReplayCursorState {
  current_index: number;
  total_events: number;
  current_event_id: string | null;
  current_timestamp: string | null;
  is_at_start: boolean;
  is_at_end: boolean;
  progress_percentage: number;
  last_seek_time: string;
}

export interface ReconstructedTaskState {
  task_id: string;
  task_type: string;
  status: string;
  worker_id: string | null;
  start_time: string | null;
  end_time: string | null;
  duration_ms: number;
  input_data: Record<string, any>;
  output_data: Record<string, any>;
  error: string | null;
  retry_count: number;
}

export interface ReconstructedMissionState {
  mission_id: string;
  status: string;
  current_stage: string;
  total_events_applied: number;
  tasks: Record<string, ReconstructedTaskState>;
  planner_strategy: string | null;
  planner_generation: number;
  confidence_score: number;
  dag_version: number;
  total_cost_usd: number;
  total_duration_ms: number;
  created_at: string | null;
  completed_at: string | null;
  metadata: Record<string, any>;
}

export interface StateDiffSummary {
  mission_id: string;
  from_index: number;
  to_index: number;
  status_changed: boolean;
  tasks_added: string[];
  tasks_modified: string[];
  tasks_completed: string[];
  confidence_delta: number;
  cost_delta_usd: number;
  dag_version_delta: number;
}

export interface ReplaySessionState {
  mission_id: string;
  status: PlayerStatus;
  speed: ReplaySpeed;
  cursor: ReplayCursorState;
  state: ReconstructedMissionState;
  diff_from_previous?: StateDiffSummary;
}

export interface TimelineEntry {
  event_id: string;
  sequence_number: number;
  timestamp: string;
  category: string;
  event_type: string;
  severity: string;
  stage: string;
  worker_id: string | null;
  task_id: string | null;
  summary: string;
  duration_ms: number | null;
  hash: string;
  previous_hash: string;
  is_checkpoint: boolean;
  payload: Record<string, any>;
}

export interface TimelineSummary {
  mission_id: string;
  total_events: number;
  start_time: string | null;
  end_time: string | null;
  total_duration_ms: number;
  stages: string[];
  categories: Record<string, number>;
  entries: TimelineEntry[];
}

export interface PlanUtilityScore {
  accuracy: number;
  latency_score: number;
  cost_score: number;
  safety_score: number;
  total_utility: number;
  weights: Record<string, number>;
}

export interface DecisionAlternative {
  strategy_name: string;
  utility_score: number;
  rejection_reason: string;
  metrics: Record<string, number>;
}

export interface DecisionRecord {
  decision_id: string;
  mission_id: string;
  event_id: string;
  event_sequence: number;
  timestamp: string;
  why: string;
  what: string;
  based_on: Record<string, any>;
  why_not_others: Record<string, string>;
  selected_strategy: string;
  confidence: number;
  planner_generation: number;
  utility_breakdown: PlanUtilityScore;
  alternatives_evaluated: DecisionAlternative[];
  sha256_provenance_hash: string;
  parent_decision_id: string | null;
}

export interface DecisionGraphNode {
  id: string;
  label: string;
  generation: number;
  confidence: number;
  utility: number;
  strategy: string;
  timestamp: string;
  why: string;
  what: string;
  is_selected: boolean;
  event_id: string;
}

export interface DecisionGraphEdge {
  from_id: string;
  to_id: string;
  relationship: string;
  utility_delta: number;
}

export interface DecisionGraph {
  mission_id: string;
  nodes: DecisionGraphNode[];
  edges: DecisionGraphEdge[];
  root_decision_id: string | null;
  coverage_percentage: number;
}

export interface AuditRecord {
  audit_id: string;
  mission_id: string;
  event_id: string;
  sequence_number: number;
  timestamp: string;
  category: string;
  action_type: string;
  actor: string;
  details: Record<string, any>;
  previous_audit_hash: string;
  audit_hash: string;
  hmac_signature: string;
  verified: boolean;
}

export interface AuditVerificationReport {
  mission_id: string;
  total_audit_records: number;
  is_valid: boolean;
  chain_broken_at_index: number | null;
  invalid_record_id: string | null;
  verified_at: string;
  signature_algorithm: string;
}

export interface SnapshotMetadata {
  snapshot_id: string;
  mission_id: string;
  event_index: number;
  event_id: string;
  timestamp: string;
  checksum: string;
  uncompressed_size_bytes: number;
  compressed_size_bytes: number;
  compression_ratio: number;
}

export interface ReplayBookmark {
  bookmark_id: string;
  mission_id: string;
  event_index: number;
  event_id: string;
  label: string;
  bookmark_type: BookmarkType;
  created_at: string;
  description: string;
}
