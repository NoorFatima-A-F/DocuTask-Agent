/**
 * Phase 13.18: Distributed Platform Types & Interfaces
 * Autonomous Cloud Runtime & Distributed Agent Fabric (ACR-DAF).
 */

export type WorkerStatus = 'ONLINE' | 'BUSY' | 'DRAINING' | 'OFFLINE' | 'CRASHED';

export type JobPriority = 'CRITICAL' | 'HIGH' | 'NORMAL' | 'BATCH';

export type JobState =
  | 'QUEUED'
  | 'SCHEDULED'
  | 'RUNNING'
  | 'CHECKPOINTED'
  | 'PAUSED'
  | 'COMPLETED'
  | 'FAILED'
  | 'MIGRATED';

export type RegionName =
  | 'us-east-1'
  | 'us-west-2'
  | 'eu-central-1'
  | 'asia-east-1'
  | 'pk-south-1';

export type ScalingAction = 'SCALE_UP' | 'SCALE_DOWN' | 'STABLE';

export interface WorkerCapacity {
  max_concurrent_jobs: number;
  allocated_jobs: number;
  cpu_cores: number;
  memory_mb: number;
  cpu_utilization_pct: number;
  memory_utilization_pct: number;
  gpu_available?: boolean;
}

export interface WorkerNode {
  worker_id: string;
  hostname: string;
  region: RegionName;
  status: WorkerStatus;
  capabilities: string[];
  capacity: WorkerCapacity;
  last_heartbeat: string;
  registered_at: string;
  version: string;
  total_jobs_completed: number;
  historical_avg_latency_ms: number;
}

export interface ScheduledJob {
  job_id: string;
  workflow_id: string;
  agent_id: string;
  task_name: string;
  priority: JobPriority;
  state: JobState;
  assigned_worker_id?: string | null;
  target_region?: RegionName | null;
  payload?: Record<string, any>;
  retry_count: number;
  max_retries: number;
  sla_deadline_ms: number;
  enqueued_at: string;
  started_at?: string | null;
  completed_at?: string | null;
  execution_duration_ms: number;
  error_message?: string | null;
}

export interface WorkflowStepState {
  step_index: number;
  step_name: string;
  status: string;
  inputs?: Record<string, any>;
  outputs?: Record<string, any>;
  duration_ms: number;
}

export interface WorkflowCheckpoint {
  checkpoint_id: string;
  workflow_id: string;
  step_index: number;
  completed_steps: WorkflowStepState[];
  variables: Record<string, any>;
  memory_context: Record<string, any>;
  timestamp: string;
  fencing_token: number;
  state_hash: string;
}

export interface DurableWorkflow {
  workflow_id: string;
  title: string;
  tenant_id: string;
  agent_id: string;
  state: JobState;
  current_step_index: number;
  total_steps: number;
  assigned_worker_id?: string | null;
  checkpoints: WorkflowCheckpoint[];
  created_at: string;
  updated_at: string;
}

export interface LockLease {
  lock_key: string;
  holder_id: string;
  fencing_token: number;
  acquired_at: string;
  expires_at: string;
  lease_duration_sec: number;
}

export interface AutoscalingPolicy {
  policy_id: string;
  min_workers: number;
  max_workers: number;
  target_cpu_utilization_pct: number;
  target_queue_latency_ms: number;
  scale_up_threshold_jobs: number;
  scale_down_idle_sec: number;
  current_desired_workers: number;
  last_scaling_action: ScalingAction;
  last_scaled_at: string;
}

export interface ClusterOverview {
  cluster_id: string;
  status: string;
  total_workers: number;
  active_workers: number;
  draining_workers: number;
  crashed_workers: number;
  total_queued_jobs: number;
  total_running_jobs: number;
  total_completed_jobs: number;
  mean_cluster_cpu_pct: number;
  mean_cluster_memory_pct: number;
  throughput_jobs_per_sec: number;
  active_regions: string[];
  timestamp: string;
}

export interface DisasterRecoverySnapshot {
  snapshot_id: string;
  timestamp: string;
  source_region: RegionName;
  target_replicas: RegionName[];
  workflow_count: number;
  checkpoint_count: number;
  snapshot_size_bytes: number;
  status: string;
  rpo_seconds: number;
  rto_seconds: number;
}

export interface QueueChannelMetrics {
  channel_name: string;
  critical_depth: number;
  high_depth: number;
  normal_depth: number;
  batch_depth: number;
  total_depth: number;
  dlq_depth: number;
}

export interface RegionTopologyInfo {
  region: string;
  location: string;
  status: string;
  avg_latency_ms: number;
}
