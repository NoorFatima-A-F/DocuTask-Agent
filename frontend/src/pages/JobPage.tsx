import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { api } from '../api/api';
import { errorMessage } from '../api/client';
import { FINISHED_JOB_STATUSES, type Extraction, type Job } from '../api/types';
import { ConfidenceSummary, FieldTable } from '../components/FieldTable';
import { StatusBadge } from '../components/StatusBadge';
import { Button, Card, ErrorBox, Link } from '../components/ui';

const POLL_MS = 2000;

const STATUS_TEXT: Record<string, string> = {
  QUEUED: 'Waiting for a worker.',
  RUNNING: 'Running OCR and extraction.',
  RETRYING: 'A temporary error occurred; the job will retry automatically.',
  COMPLETED: 'Extraction finished and passed all checks.',
  NEEDS_REVIEW: 'Extraction finished but needs a human review before it is final.',
  FAILED: 'The job failed. No data was extracted.',
};

export function JobPage({ jobId }: { jobId: string }) {
  const queryClient = useQueryClient();
  const job = useQuery({
    queryKey: ['job', jobId],
    queryFn: () => api.job(jobId),
    refetchInterval: (q) => (q.state.data && FINISHED_JOB_STATUSES.includes(q.state.data.status) ? false : POLL_MS),
  });
  const finished = !!job.data && job.data.status !== 'FAILED' && FINISHED_JOB_STATUSES.includes(job.data.status);
  const extraction = useQuery({
    queryKey: ['extraction', job.data?.document_id, job.data?.updated_at],
    queryFn: () => api.extraction(job.data!.document_id),
    enabled: finished,
  });
  const retry = useMutation({
    mutationFn: () => api.retryJob(jobId),
    onSuccess: (updated) => queryClient.setQueryData(['job', jobId], updated),
  });

  if (job.error) return <ErrorBox message={errorMessage(job.error)} />;
  if (!job.data) return <p className="text-sm text-slate-400">Loading…</p>;

  return (
    <div className="space-y-6">
      <Link to="/">← All jobs</Link>
      <JobSummary job={job.data} onRetry={() => retry.mutate()} retrying={retry.isPending} />
      <ErrorBox message={retry.error ? errorMessage(retry.error) : null} />
      {extraction.error && <ErrorBox message={errorMessage(extraction.error)} />}
      {extraction.data && <ExtractionView extraction={extraction.data} />}
    </div>
  );
}

function JobSummary({ job, onRetry, retrying }: { job: Job; onRetry: () => void; retrying: boolean }) {
  return (
    <Card
      title={`Job ${job.id.slice(0, 8)}`}
      actions={
        job.status === 'FAILED' ? (
          <Button variant="secondary" onClick={onRetry} disabled={retrying}>
            Retry
          </Button>
        ) : undefined
      }
    >
      <div className="flex items-center gap-3">
        <StatusBadge status={job.status} />
        <span className="text-sm text-slate-300">{STATUS_TEXT[job.status]}</span>
      </div>
      <dl className="mt-3 grid grid-cols-2 gap-x-6 gap-y-1 text-sm sm:grid-cols-4">
        <dt className="text-slate-400">Type</dt>
        <dd>{job.document_type}</dd>
        <dt className="text-slate-400">Attempts</dt>
        <dd>
          {job.attempts}/{job.max_attempts}
        </dd>
      </dl>
      {job.error_code && (
        <p className="mt-3 text-sm text-red-300" data-testid="job-error">
          <span className="font-mono">{job.error_code}</span>
          {job.last_error && <>: {job.last_error}</>}
        </p>
      )}
    </Card>
  );
}

export function ExtractionView({ extraction }: { extraction: Extraction }) {
  const { result } = extraction;
  const data = result.final_json ?? result.structured_json;
  return (
    <Card title="Extracted data" actions={<StatusBadge status={result.status} />}>
      {result.status === 'NEEDS_REVIEW' && (
        <p className="mb-3 rounded border border-orange-700 bg-orange-950 px-3 py-2 text-sm text-orange-200">
          Not final: a reviewer must approve or correct these values.
        </p>
      )}
      <ConfidenceSummary confidence={result.confidence} details={result.confidence_details} />
      <div className="mt-4">
        {data ? (
          <FieldTable data={data} details={result.confidence_details} />
        ) : (
          <p className="text-sm text-slate-400">No data.</p>
        )}
      </div>
      <p className="mt-3 text-xs text-slate-500">
        Model {extraction.metadata.model} · {extraction.statistics.processing_time_ms} ms
        {extraction.statistics.estimated_cost != null && ` · $${extraction.statistics.estimated_cost.toFixed(5)}`}
      </p>
    </Card>
  );
}
