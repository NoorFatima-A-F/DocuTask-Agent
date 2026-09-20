/**
 * TypeScript Contracts for Autonomous Planner Visualization, Dynamic DAG Execution & Live Replanning (APDLE).
 */

export type NodeStatusType =
  | 'READY'
  | 'WAITING'
  | 'RUNNING'
  | 'FAILED'
  | 'BLOCKED'
  | 'CANCELLED'
  | 'COMPLETED'
  | 'RETRYING'
  | 'MUTATED';

export type DependencyKind =
  | 'HARD'
  | 'SOFT'
  | 'OPTIONAL'
  | 'CONDITIONAL'
  | 'RUNTIME'
  | 'HUMAN_APPROVAL';

export interface VisualNodePayload {
  id: string;
  label: string;
  task_type: string;
  status: NodeStatusType;
  priority: number;
  estimated_cost_usd: number;
  estimated_runtime_ms: number;
  actual_runtime_ms: number;
  assigned_worker?: string | null;
  is_critical_path: boolean;
  total_slack_ms: number;
  position: { x: number; y: number };
}

export interface VisualEdgePayload {
  id: string;
  source: string;
  target: string;
  edge_type: string;
  condition?: string | null;
  is_critical_path: boolean;
}

export interface VisualDAGSnapshotPayload {
  dag_id: string;
  mission_id: string;
  generation: number;
  critical_path_duration_ms: number;
  critical_nodes_count: number;
  structural_depth: number;
  nodes: VisualNodePayload[];
  edges: VisualEdgePayload[];
}

export interface CPMAnalysisPayload {
  total_critical_path_duration_ms: number;
  critical_nodes_count: number;
  critical_node_ids: string[];
  nodes_cpm: Record<
    string,
    {
      name: string;
      task_type: string;
      estimated_runtime_ms: number;
      earliest_start_ms: number;
      latest_start_ms: number;
      earliest_finish_ms: number;
      latest_finish_ms: number;
      total_slack_ms: number;
      is_critical: boolean;
    }
  >;
}

export interface WorkerDescriptorPayload {
  worker_id: string;
  name: string;
  capabilities: string[];
  status: string;
  active_tasks: number;
  max_concurrency: number;
  historical_success_rate: number;
  average_latency_ms: number;
}

export interface ScheduleStatusPayload {
  mission_id: string;
  dag_id: string;
  completed_nodes: string[];
  failed_nodes: string[];
  total_nodes: number;
  ready_nodes: string[];
  wavefronts: string[][];
  workers: WorkerDescriptorPayload[];
}

export interface GraphMutationRecordPayload {
  mutation_id: string;
  mission_id: string;
  mutation_type: string;
  trigger_reason: string;
  affected_node_ids: string[];
  nodes_added_count: number;
  nodes_removed_count: number;
  edges_added_count: number;
  edges_removed_count: number;
  timestamp: number;
  diff_summary: Record<string, any>;
}

export interface SimulationResultPayload {
  mission_id: string;
  trials_count: number;
  mean_completion_ms: float;
  p50_completion_ms: float;
  p90_completion_ms: float;
  p99_completion_ms: float;
  expected_total_cost_usd: float;
  expected_total_tokens: number;
  expected_retry_probability: float;
  bottleneck_node_ids: string[];
}
type float = number;
