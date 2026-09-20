/**
 * REST API Client for Autonomous Planner Visualization, Dynamic DAG Execution & Live Replanning (APDLE).
 */

import {
  CPMAnalysisPayload,
  GraphMutationRecordPayload,
  ScheduleStatusPayload,
  SimulationResultPayload,
  VisualDAGSnapshotPayload,
} from '../types/apdlePlanner';

const API_BASE = '/api/v1/planner';

export class ApdlePlannerApiClient {
  /** Fetches current visual DAG snapshot */
  static async getGraph(missionId: string = 'default_mission'): Promise<VisualDAGSnapshotPayload> {
    try {
      const res = await fetch(`${API_BASE}/graph/${missionId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Using fallback DAG snapshot:', e);
      return this.getFallbackGraph(missionId);
    }
  }

  /** Fetches Critical Path Method analysis */
  static async getCriticalPath(missionId: string = 'default_mission'): Promise<CPMAnalysisPayload> {
    try {
      const res = await fetch(`${API_BASE}/critical-path/${missionId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Using fallback CPM analysis:', e);
      return {
        total_critical_path_duration_ms: 780.0,
        critical_nodes_count: 3,
        critical_node_ids: ['node_ocr_01', 'node_extract_items', 'node_smt_verify'],
        nodes_cpm: {
          node_ocr_01: {
            name: 'Adaptive Holdout OCR Scan',
            task_type: 'OCR',
            estimated_runtime_ms: 350.0,
            earliest_start_ms: 0.0,
            latest_start_ms: 0.0,
            earliest_finish_ms: 350.0,
            latest_finish_ms: 350.0,
            total_slack_ms: 0.0,
            is_critical: true,
          },
          node_extract_items: {
            name: 'Table Line-Item Parsing',
            task_type: 'EXTRACTION',
            estimated_runtime_ms: 280.0,
            earliest_start_ms: 350.0,
            latest_start_ms: 350.0,
            earliest_finish_ms: 630.0,
            latest_finish_ms: 630.0,
            total_slack_ms: 0.0,
            is_critical: true,
          },
          node_extract_meta: {
            name: 'Vendor & Tax Header Extraction',
            task_type: 'EXTRACTION',
            estimated_runtime_ms: 180.0,
            earliest_start_ms: 350.0,
            latest_start_ms: 450.0,
            earliest_finish_ms: 530.0,
            latest_finish_ms: 630.0,
            total_slack_ms: 100.0,
            is_critical: false,
          },
          node_smt_verify: {
            name: 'SMT Arithmetic Invariant Proof',
            task_type: 'VALIDATION',
            estimated_runtime_ms: 60.0,
            earliest_start_ms: 630.0,
            latest_start_ms: 630.0,
            earliest_finish_ms: 690.0,
            latest_finish_ms: 690.0,
            total_slack_ms: 0.0,
            is_critical: true,
          },
          node_reflection: {
            name: 'Meta-Cognitive Self-Critique',
            task_type: 'REFLECTION',
            estimated_runtime_ms: 90.0,
            earliest_start_ms: 690.0,
            latest_start_ms: 690.0,
            earliest_finish_ms: 780.0,
            latest_finish_ms: 780.0,
            total_slack_ms: 0.0,
            is_critical: true,
          },
        },
      };
    }
  }

  /** Fetches scheduling state */
  static async getSchedule(missionId: string = 'default_mission'): Promise<ScheduleStatusPayload> {
    try {
      const res = await fetch(`${API_BASE}/schedule/${missionId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Using fallback schedule status:', e);
      return {
        mission_id: missionId,
        dag_id: 'dag-fallback',
        completed_nodes: ['node_ocr_01'],
        failed_nodes: [],
        total_nodes: 5,
        ready_nodes: ['node_extract_items', 'node_extract_meta'],
        wavefronts: [
          ['node_ocr_01'],
          ['node_extract_items', 'node_extract_meta'],
          ['node_smt_verify'],
          ['node_reflection'],
        ],
        workers: [
          {
            worker_id: 'worker_ocr_01',
            name: 'OCR GPU Worker 1',
            capabilities: ['OCR', 'VISION', 'GENERAL'],
            status: 'IDLE',
            active_tasks: 0,
            max_concurrency: 4,
            historical_success_rate: 0.99,
            average_latency_ms: 320.0,
          },
          {
            worker_id: 'worker_nlp_01',
            name: 'NLP Extraction Worker 1',
            capabilities: ['EXTRACTION', 'NLP', 'GENERAL'],
            status: 'BUSY',
            active_tasks: 2,
            max_concurrency: 4,
            historical_success_rate: 0.97,
            average_latency_ms: 240.0,
          },
          {
            worker_id: 'worker_smt_01',
            name: 'Formal SMT Governance Worker',
            capabilities: ['VALIDATION', 'GOVERNANCE', 'SMT', 'GENERAL'],
            status: 'IDLE',
            active_tasks: 0,
            max_concurrency: 2,
            historical_success_rate: 1.0,
            average_latency_ms: 55.0,
          },
        ],
      };
    }
  }

  /** Fetches Monte Carlo pre-execution simulation */
  static async getSimulation(
    missionId: string = 'default_mission',
    numTrials: number = 100
  ): Promise<SimulationResultPayload> {
    try {
      const res = await fetch(`${API_BASE}/simulation/${missionId}?num_trials=${numTrials}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Using fallback simulation:', e);
      return {
        mission_id: missionId,
        trials_count: numTrials,
        mean_completion_ms: 785.4,
        p50_completion_ms: 760.0,
        p90_completion_ms: 880.0,
        p99_completion_ms: 995.0,
        expected_total_cost_usd: 0.0032,
        expected_total_tokens: 1950,
        expected_retry_probability: 0.04,
        bottleneck_node_ids: ['node_ocr_01', 'node_extract_items'],
      };
    }
  }

  /** Triggers adaptive in-flight replanning */
  static async triggerReplan(
    missionId: string = 'default_mission',
    failedNodeId?: string,
    errorReason: string = 'Validation invariant breached',
    confidenceDrop?: number
  ): Promise<{
    status: string;
    mutation: GraphMutationRecordPayload;
    updated_dag: VisualDAGSnapshotPayload;
  }> {
    try {
      const res = await fetch(`${API_BASE}/replan/${missionId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          failed_node_id: failedNodeId,
          error_reason: errorReason,
          confidence_drop: confidenceDrop,
        }),
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      console.warn('Using fallback replan execution:', e);
      const graph = this.getFallbackGraph(missionId);
      graph.generation += 1;
      return {
        status: 'REPLANNED',
        mutation: {
          mutation_id: 'mut-demo-01',
          mission_id: missionId,
          mutation_type: 'INJECT_RECOVERY',
          trigger_reason: errorReason,
          affected_node_ids: [failedNodeId || 'node_ocr_01', 'rec_deskew_01', 'rec_ocr_retry_01'],
          nodes_added_count: 2,
          nodes_removed_count: 0,
          edges_added_count: 3,
          edges_removed_count: 1,
          timestamp: Date.now() / 1000,
          diff_summary: {
            injected: ['rec_deskew_01', 'rec_ocr_retry_01'],
            resumed_at: 'node_extract_items',
          },
        },
        updated_dag: graph,
      };
    }
  }

  /** Fetches mutation history */
  static async getMutations(missionId: string = 'default_mission'): Promise<GraphMutationRecordPayload[]> {
    try {
      const res = await fetch(`${API_BASE}/mutations/${missionId}`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (e) {
      return [];
    }
  }

  private static getFallbackGraph(missionId: string): VisualDAGSnapshotPayload {
    return {
      dag_id: 'dag-init',
      mission_id: missionId,
      generation: 1,
      critical_path_duration_ms: 780.0,
      critical_nodes_count: 4,
      structural_depth: 4,
      nodes: [
        {
          id: 'node_ocr_01',
          label: 'Adaptive Holdout OCR Scan',
          task_type: 'OCR',
          status: 'COMPLETED',
          priority: 10,
          estimated_cost_usd: 0.0008,
          estimated_runtime_ms: 350.0,
          actual_runtime_ms: 342.0,
          assigned_worker: 'worker_ocr_01',
          is_critical_path: true,
          total_slack_ms: 0.0,
          position: { x: 100, y: 150 },
        },
        {
          id: 'node_extract_items',
          label: 'Table Line-Item Parsing',
          task_type: 'EXTRACTION',
          status: 'RUNNING',
          priority: 20,
          estimated_cost_usd: 0.0012,
          estimated_runtime_ms: 280.0,
          actual_runtime_ms: 0.0,
          assigned_worker: 'worker_nlp_01',
          is_critical_path: true,
          total_slack_ms: 0.0,
          position: { x: 320, y: 100 },
        },
        {
          id: 'node_extract_meta',
          label: 'Vendor & Tax Header Extraction',
          task_type: 'EXTRACTION',
          status: 'RUNNING',
          priority: 20,
          estimated_cost_usd: 0.0006,
          estimated_runtime_ms: 180.0,
          actual_runtime_ms: 0.0,
          assigned_worker: 'worker_nlp_02',
          is_critical_path: false,
          total_slack_ms: 100.0,
          position: { x: 320, y: 220 },
        },
        {
          id: 'node_smt_verify',
          label: 'SMT Arithmetic Invariant Proof',
          task_type: 'VALIDATION',
          status: 'WAITING',
          priority: 15,
          estimated_cost_usd: 0.0002,
          estimated_runtime_ms: 60.0,
          actual_runtime_ms: 0.0,
          is_critical_path: true,
          total_slack_ms: 0.0,
          position: { x: 540, y: 150 },
        },
        {
          id: 'node_reflection',
          label: 'Meta-Cognitive Self-Critique',
          task_type: 'REFLECTION',
          status: 'WAITING',
          priority: 30,
          estimated_cost_usd: 0.0004,
          estimated_runtime_ms: 90.0,
          actual_runtime_ms: 0.0,
          is_critical_path: true,
          total_slack_ms: 0.0,
          position: { x: 760, y: 150 },
        },
      ],
      edges: [
        { id: 'e1', source: 'node_ocr_01', target: 'node_extract_items', edge_type: 'DATA_FLOW', is_critical_path: true },
        { id: 'e2', source: 'node_ocr_01', target: 'node_extract_meta', edge_type: 'DATA_FLOW', is_critical_path: false },
        { id: 'e3', source: 'node_extract_items', target: 'node_smt_verify', edge_type: 'DATA_FLOW', is_critical_path: true },
        { id: 'e4', source: 'node_extract_meta', target: 'node_smt_verify', edge_type: 'DATA_FLOW', is_critical_path: false },
        { id: 'e5', source: 'node_smt_verify', target: 'node_reflection', edge_type: 'DATA_FLOW', is_critical_path: true },
      ],
    };
  }
}
