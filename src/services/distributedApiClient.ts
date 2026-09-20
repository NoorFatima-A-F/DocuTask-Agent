/**
 * Phase 13.18: Distributed Platform API Client
 * Connects to /api/v1/distributed with robust resilient mock fallback.
 */

import {
  ClusterOverview,
  WorkerNode,
  ScheduledJob,
  DurableWorkflow,
  WorkflowCheckpoint,
  QueueChannelMetrics,
  RegionTopologyInfo,
  DisasterRecoverySnapshot,
} from '../types/distributedPlatform';

const BASE_URL = '/api/v1/distributed';

export class DistributedApiClient {
  private static async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const res = await fetch(`${BASE_URL}${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
      },
      ...options,
    });
    if (!res.ok) {
      throw new Error(`API error ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  static async getClusterOverview(): Promise<ClusterOverview> {
    try {
      return await this.request<ClusterOverview>('/cluster/overview');
    } catch {
      return {
        cluster_id: 'acr_fabric_cluster_01',
        status: 'HEALTHY',
        total_workers: 5,
        active_workers: 5,
        draining_workers: 0,
        crashed_workers: 0,
        total_queued_jobs: 14,
        total_running_jobs: 6,
        total_completed_jobs: 1845,
        mean_cluster_cpu_pct: 23.6,
        mean_cluster_memory_pct: 29.8,
        throughput_jobs_per_sec: 52.4,
        active_regions: ['us-east-1', 'eu-central-1', 'asia-east-1', 'pk-south-1'],
        timestamp: new Date().toISOString(),
      };
    }
  }

  static async getWorkers(region?: string, activeOnly = false): Promise<WorkerNode[]> {
    try {
      const q = new URLSearchParams();
      if (region) q.append('region', region);
      if (activeOnly) q.append('active_only', 'true');
      return await this.request<WorkerNode[]>(`/workers?${q.toString()}`);
    } catch {
      return [
        {
          worker_id: 'node_us_east_01',
          hostname: 'worker-cloudrun-us-01.internal',
          region: 'us-east-1',
          status: 'ONLINE',
          capabilities: ['reasoning', 'ocr', 'planning', 'tool_execution'],
          capacity: {
            max_concurrent_jobs: 8,
            allocated_jobs: 2,
            cpu_cores: 4,
            memory_mb: 8192,
            cpu_utilization_pct: 18.5,
            memory_utilization_pct: 24.0,
          },
          last_heartbeat: new Date().toISOString(),
          registered_at: new Date(Date.now() - 86400000).toISOString(),
          version: 'v1.18.0',
          total_jobs_completed: 420,
          historical_avg_latency_ms: 110.5,
        },
        {
          worker_id: 'node_eu_central_01',
          hostname: 'worker-gke-eu-01.internal',
          region: 'eu-central-1',
          status: 'ONLINE',
          capabilities: ['reasoning', 'planning'],
          capacity: {
            max_concurrent_jobs: 8,
            allocated_jobs: 1,
            cpu_cores: 4,
            memory_mb: 8192,
            cpu_utilization_pct: 25.0,
            memory_utilization_pct: 32.0,
          },
          last_heartbeat: new Date().toISOString(),
          registered_at: new Date(Date.now() - 86400000).toISOString(),
          version: 'v1.18.0',
          total_jobs_completed: 310,
          historical_avg_latency_ms: 95.0,
        },
        {
          worker_id: 'node_asia_east_01',
          hostname: 'worker-gke-asia-01.internal',
          region: 'asia-east-1',
          status: 'ONLINE',
          capabilities: ['reasoning', 'ocr'],
          capacity: {
            max_concurrent_jobs: 8,
            allocated_jobs: 3,
            cpu_cores: 4,
            memory_mb: 8192,
            cpu_utilization_pct: 42.0,
            memory_utilization_pct: 48.0,
          },
          last_heartbeat: new Date().toISOString(),
          registered_at: new Date(Date.now() - 86400000).toISOString(),
          version: 'v1.18.0',
          total_jobs_completed: 280,
          historical_avg_latency_ms: 125.0,
        },
      ];
    }
  }

  static async drainWorker(workerId: string): Promise<any> {
    return await this.request<any>(`/workers/${workerId}/drain`, { method: 'POST' });
  }

  static async getQueueMetrics(): Promise<QueueChannelMetrics[]> {
    try {
      return await this.request<QueueChannelMetrics[]>('/queues');
    } catch {
      return [
        {
          channel_name: 'agent_tasks',
          critical_depth: 1,
          high_depth: 3,
          normal_depth: 8,
          batch_depth: 2,
          total_depth: 14,
          dlq_depth: 0,
        },
        {
          channel_name: 'system_jobs',
          critical_depth: 0,
          high_depth: 1,
          normal_depth: 2,
          batch_depth: 0,
          total_depth: 3,
          dlq_depth: 0,
        },
      ];
    }
  }

  static async submitJob(params: {
    workflow_id: string;
    agent_id: string;
    task_name: string;
    priority?: string;
  }): Promise<ScheduledJob> {
    return await this.request<ScheduledJob>('/scheduler/jobs', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  static async listJobs(limit = 50, state?: string): Promise<ScheduledJob[]> {
    try {
      const q = new URLSearchParams({ limit: String(limit) });
      if (state) q.append('state', state);
      return await this.request<ScheduledJob[]>(`/scheduler/jobs?${q.toString()}`);
    } catch {
      return [
        {
          job_id: 'job_sample_001',
          workflow_id: 'wf_doc_101',
          agent_id: 'agent_doc_extractor',
          task_name: 'Extract Multimodal Invoices',
          priority: 'HIGH',
          state: 'RUNNING',
          assigned_worker_id: 'node_us_east_01',
          retry_count: 0,
          max_retries: 3,
          sla_deadline_ms: 4500.0,
          enqueued_at: new Date(Date.now() - 15000).toISOString(),
          started_at: new Date(Date.now() - 12000).toISOString(),
          execution_duration_ms: 180.0,
        },
        {
          job_id: 'job_sample_002',
          workflow_id: 'wf_arch_102',
          agent_id: 'agent_chief_architect',
          task_name: 'Optimize Graph Architecture',
          priority: 'NORMAL',
          state: 'QUEUED',
          retry_count: 0,
          max_retries: 3,
          sla_deadline_ms: 5000.0,
          enqueued_at: new Date(Date.now() - 8000).toISOString(),
          execution_duration_ms: 0.0,
        },
      ];
    }
  }

  static async getDurableWorkflows(): Promise<DurableWorkflow[]> {
    try {
      return await this.request<DurableWorkflow[]>('/workflows/durable');
    } catch {
      return [
        {
          workflow_id: 'wf_invoice_proc_01',
          title: 'Enterprise Document Extraction Saga',
          tenant_id: 'tenant_enterprise_01',
          agent_id: 'agent_doc_extractor',
          state: 'RUNNING',
          current_step_index: 2,
          total_steps: 4,
          assigned_worker_id: 'node_us_east_01',
          created_at: new Date(Date.now() - 3600000).toISOString(),
          updated_at: new Date().toISOString(),
          checkpoints: [
            {
              checkpoint_id: 'chk_001',
              workflow_id: 'wf_invoice_proc_01',
              step_index: 0,
              completed_steps: [
                {
                  step_index: 0,
                  step_name: 'Multimodal OCR Extraction',
                  status: 'COMPLETED',
                  inputs: { file: 'invoice_9941.pdf' },
                  outputs: { pages: 3, status: 'EXTRACTED' },
                  duration_ms: 120.0,
                },
              ],
              variables: { doc_type: 'INVOICE' },
              memory_context: { tenant: 'acme_corp' },
              timestamp: new Date(Date.now() - 1800000).toISOString(),
              fencing_token: 1,
              state_hash: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
            },
          ],
        },
      ];
    }
  }

  static async pauseWorkflow(workflowId: string): Promise<DurableWorkflow> {
    return await this.request<DurableWorkflow>(`/workflows/${workflowId}/pause`, { method: 'POST' });
  }

  static async resumeWorkflow(workflowId: string): Promise<DurableWorkflow> {
    return await this.request<DurableWorkflow>(`/workflows/${workflowId}/resume`, { method: 'POST' });
  }

  static async getCheckpoints(workflowId: string): Promise<WorkflowCheckpoint[]> {
    try {
      return await this.request<WorkflowCheckpoint[]>(`/checkpoints/${workflowId}`);
    } catch {
      return [];
    }
  }

  static async getAutoscalingStatus(): Promise<any> {
    try {
      return await this.request<any>('/autoscaling/status');
    } catch {
      return {
        policy: {
          min_workers: 3,
          max_workers: 50,
          target_cpu_utilization_pct: 70.0,
          current_desired_workers: 5,
          last_scaling_action: 'STABLE',
          last_scaled_at: new Date().toISOString(),
        },
        recent_decisions: [
          {
            action: 'STABLE',
            current_workers: 5,
            desired_workers: 5,
            queue_depth: 14,
            mean_cpu_pct: 24.5,
            mean_ram_pct: 31.2,
            timestamp: new Date().toISOString(),
          },
        ],
      };
    }
  }

  static async evaluateAutoscaling(): Promise<any> {
    return await this.request<any>('/autoscaling/evaluate', { method: 'POST' });
  }

  static async getRegions(): Promise<RegionTopologyInfo[]> {
    try {
      return await this.request<RegionTopologyInfo[]>('/regions');
    } catch {
      return [
        { region: 'us-east-1', location: 'N. Virginia (GCP us-east4)', status: 'ONLINE', avg_latency_ms: 8.5 },
        { region: 'us-west-2', location: 'Oregon (GCP us-west1)', status: 'ONLINE', avg_latency_ms: 65.0 },
        { region: 'eu-central-1', location: 'Frankfurt (GCP europe-west3)', status: 'ONLINE', avg_latency_ms: 10.2 },
        { region: 'asia-east-1', location: 'Tokyo (GCP asia-northeast1)', status: 'ONLINE', avg_latency_ms: 12.0 },
        { region: 'pk-south-1', location: 'Karachi Edge (Hybrid Node Cluster)', status: 'ONLINE', avg_latency_ms: 6.0 },
      ];
    }
  }

  static async injectChaosFailure(workerId: string): Promise<any> {
    return await this.request<any>('/chaos/inject-failure', {
      method: 'POST',
      body: JSON.stringify({ worker_id: workerId }),
    });
  }

  static async getDisasterRecoveryStatus(): Promise<DisasterRecoverySnapshot[]> {
    try {
      return await this.request<DisasterRecoverySnapshot[]>('/disaster-recovery/status');
    } catch {
      return [
        {
          snapshot_id: 'dr_snap_us_east_daily',
          timestamp: new Date().toISOString(),
          source_region: 'us-east-1',
          target_replicas: ['eu-central-1', 'asia-east-1'],
          workflow_count: 42,
          checkpoint_count: 180,
          snapshot_size_bytes: 2458900,
          status: 'REPLICATED',
          rpo_seconds: 1.8,
          rto_seconds: 8.5,
        },
      ];
    }
  }

  static async runDisasterRecoveryDrill(): Promise<any> {
    return await this.request<any>('/disaster-recovery/drill', {
      method: 'POST',
      body: JSON.stringify({ failed_region: 'us-east-1', target_failover_region: 'eu-central-1' }),
    });
  }

  static async runDistributedCycle(): Promise<any> {
    return await this.request<any>('/runtime/cycle', { method: 'POST' });
  }
}
