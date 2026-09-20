/**
 * Enterprise Verification Platform Domain Types.
 * Covers all 15 Core Components and 12-Stage Deterministic Lifecycle.
 */

export type VerificationStage =
  | 'PRE_FLIGHT_DISCOVERY'
  | 'DATASET_ACQUISITION'
  | 'ENVIRONMENT_PROVISIONING'
  | 'INVARIANT_REGISTRATION'
  | 'PROBABILISTIC_EXECUTION'
  | 'METRIC_COMPUTATION'
  | 'STATISTICAL_ANALYSIS'
  | 'EVIDENCE_SEALING'
  | 'QUALITY_GATE_EVALUATION'
  | 'COMPLIANCE_CERTIFICATION'
  | 'TELEMETRY_EXPORT'
  | 'POST_FLIGHT_TEARDOWN';

export type VerificationStatus = 'PENDING' | 'RUNNING' | 'PASSED' | 'FAILED' | 'CANCELLED' | 'ERROR';

export type DatasetClass =
  | 'HAPPY_PATH'
  | 'BOUNDARY'
  | 'NEGATIVE'
  | 'ADVERSARIAL'
  | 'REGRESSION'
  | 'STRESS'
  | 'SYNTHETIC'
  | 'PRODUCTION_SNAPSHOT'
  | 'MULTILINGUAL'
  | 'BENCHMARK'
  | 'SMOKE';

export type EnvironmentType =
  | 'DEVELOPMENT'
  | 'INTEGRATION'
  | 'STAGING'
  | 'PRODUCTION_SHADOW'
  | 'CHAOS'
  | 'SECURITY_LAB'
  | 'BENCHMARK';

export interface ComponentHealth {
  component_name: string;
  status: string;
  throughput_ops_sec: number;
  latency_ms: number;
  error_rate_pct: number;
  uptime_seconds: number;
  active_connections: number;
}

export interface VerificationDefinition {
  definition_id: string;
  name: string;
  description: string;
  target_domain: string;
  version: string;
  is_immutable: boolean;
  owner: string;
  tags: string[];
  dataset_ids: string[];
  required_invariants: string[];
  config_template: Record<string, any>;
  created_at: string;
}

export interface VerificationRun {
  run_id: string;
  definition_id: string;
  plan_id: string;
  status: VerificationStatus;
  current_stage: VerificationStage;
  stage_progress_pct: number;
  overall_score: number;
  passed_invariants_count: number;
  failed_invariants_count: number;
  start_time: string;
  end_time?: string;
  correlation_id: string;
}

export interface DatasetRecord {
  dataset_id: string;
  name: string;
  dataset_class: DatasetClass;
  version: string;
  sample_count: number;
  sha256_checksum: string;
  tags: string[];
  is_archived: boolean;
  created_at: string;
}

export interface EnvironmentReadiness {
  environment_id: string;
  name: string;
  env_type: EnvironmentType;
  is_ready: boolean;
  cpu_utilization_pct: number;
  memory_available_mb: number;
  network_latency_ms: number;
  active_sandboxes: number;
  last_health_check: string;
}

export interface EvidenceItem {
  evidence_id: string;
  run_id: string;
  evidence_type: string;
  payload_hash: string;
  content_preview: string;
  metadata: Record<string, any>;
  timestamp: string;
}

export interface AuditEntry {
  audit_id: string;
  event_type: string;
  entity_id: string;
  actor: string;
  details: Record<string, any>;
  sha256_prev_hash: string;
  sha256_entry_hash: string;
  timestamp: string;
}

export interface TraceabilityNode {
  node_id: string;
  node_type: string;
  label: string;
  metadata: Record<string, any>;
  connections: string[];
}

export interface PluginDescriptor {
  plugin_id: string;
  name: string;
  domain: string;
  version: string;
  capabilities: string[];
  is_enabled: boolean;
  priority: number;
  health_status: string;
}

export interface VerificationOverview {
  platform_name: string;
  version: string;
  total_core_components: number;
  components_healthy: number;
  active_definitions: number;
  registered_plugins: number;
  datasets_count: number;
  environments_count: number;
  completed_runs: number;
  audit_ledger_size: number;
  chain_tamper_verified: boolean;
}
