/**
 * Asynchronous Processing Job & Pipeline State Machine Types
 * Strictly typed against FastAPI backend /api/v1/jobs & /api/v1/runtime endpoints.
 */

export type JobState =
  | 'QUEUED'
  | 'PROCESSING'
  | 'COMPLETED'
  | 'FAILED'
  | 'RETRYING'
  | 'DLQ';

export type PipelineMilestone =
  | 'FILE_INGESTED'
  | 'OCR_DISPATCH'
  | 'SCHEMA_MAPPING'
  | 'LLM_EXTRACTION'
  | 'QUALITY_AUDIT';

export interface MilestoneProgress {
  step: PipelineMilestone;
  title: string;
  description: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  startedAt?: string;
  completedAt?: string;
  latencyMs?: number;
  engine: string;
}

export interface JobSubmitRequest {
  document_id: string;
  document_hash: string;
  document_type?: string;
  priority?: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
}

export interface JobSubmitResponse {
  job_id: string;
  document_id: string;
  status: string;
  idempotency_key: string;
  priority: string;
}

export interface JobStatusResponse {
  job_id: string;
  status: JobState;
  checkpoint_page: number;
  total_pages: number;
  progress_percentage: number;
  current_milestone?: PipelineMilestone;
  milestones?: MilestoneProgress[];
  error_message?: string;
  stack_trace?: string;
  created_at?: string;
  updated_at?: string;
}

export interface DLQItem {
  id: string;
  job_id: string;
  document_id: string;
  error_classification: string;
  error_message: string;
  stack_trace?: string;
  retry_count: number;
  max_retries: number;
  enqueued_at: string;
  payload: Record<string, unknown>;
}

export interface DLQListResponse {
  dlq_items: DLQItem[];
}

export interface RuntimeObservabilityKPIs {
  active_workers: number;
  total_ingested_documents: number;
  average_pipeline_latency_ms: number;
  mean_confidence_score: number;
  queue_depth: number;
  dlq_count: number;
  system_health_score: number;
}
