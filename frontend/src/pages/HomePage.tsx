import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useRef, useState } from 'react';
import { api } from '../api/api';
import { errorMessage } from '../api/client';
import { DOCUMENT_TYPES, FINISHED_JOB_STATUSES } from '../api/types';
import { StatusBadge } from '../components/StatusBadge';
import { Button, Card, ErrorBox, Link } from '../components/ui';
import { navigate } from '../router';

const POLL_MS = 2000;

export function HomePage() {
  const queryClient = useQueryClient();
  const fileInput = useRef<HTMLInputElement>(null);
  const [file, setFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState<string>('invoice');
  const [error, setError] = useState<string | null>(null);

  const jobs = useQuery({
    queryKey: ['jobs'],
    queryFn: api.jobs,
    // Keep polling while any job is still in flight.
    refetchInterval: (q) => (q.state.data?.items.some((j) => !FINISHED_JOB_STATUSES.includes(j.status)) ? POLL_MS : false),
  });
  const documents = useQuery({ queryKey: ['documents'], queryFn: api.documents });
  const filenames = new Map((documents.data?.items ?? []).map((d) => [d.id, d.original_filename]));

  const submit = useMutation({
    mutationFn: async () => {
      if (!file) throw new Error('Choose a file first.');
      const uploaded = await api.upload(file);
      return api.createJob(uploaded.document.id, documentType);
    },
    onSuccess: (job) => {
      setError(null);
      setFile(null);
      if (fileInput.current) fileInput.current.value = '';
      queryClient.invalidateQueries({ queryKey: ['jobs'] });
      queryClient.invalidateQueries({ queryKey: ['documents'] });
      navigate(`/jobs/${job.id}`);
    },
    onError: (err) => setError(errorMessage(err)),
  });

  return (
    <div className="space-y-6">
      <Card title="Process a document">
        <form
          className="flex flex-wrap items-end gap-3"
          onSubmit={(e) => {
            e.preventDefault();
            submit.mutate();
          }}
        >
          <label className="text-sm">
            File (PDF or image)
            <input
              ref={fileInput}
              aria-label="Document file"
              type="file"
              accept=".pdf,.png,.jpg,.jpeg,.tiff,.bmp"
              className="mt-1 block text-sm"
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
            />
          </label>
          <label className="text-sm">
            Document type
            <select
              aria-label="Document type"
              className="mt-1 block rounded border border-slate-700 bg-slate-950 px-2 py-1.5"
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
            >
              {DOCUMENT_TYPES.map((t) => (
                <option key={t} value={t}>
                  {t.replace(/_/g, ' ')}
                </option>
              ))}
            </select>
          </label>
          <Button type="submit" disabled={!file || submit.isPending}>
            {submit.isPending ? 'Uploading…' : 'Upload and extract'}
          </Button>
        </form>
        <div className="mt-3">
          <ErrorBox message={error} />
        </div>
      </Card>

      <Card title="Jobs">
        <ErrorBox message={jobs.error ? errorMessage(jobs.error) : null} />
        {jobs.isLoading && <p className="text-sm text-slate-400">Loading…</p>}
        {jobs.data && jobs.data.items.length === 0 && <p className="text-sm text-slate-400">No jobs yet.</p>}
        {jobs.data && jobs.data.items.length > 0 && (
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-400">
              <tr>
                <th className="py-2">Document</th>
                <th>Type</th>
                <th>Status</th>
                <th>Attempts</th>
                <th>Submitted</th>
              </tr>
            </thead>
            <tbody>
              {jobs.data.items.map((job) => (
                <tr key={job.id} className="border-t border-slate-800" data-testid="job-row">
                  <td className="py-2">
                    <Link to={`/jobs/${job.id}`}>{filenames.get(job.document_id) ?? job.document_id.slice(0, 8)}</Link>
                  </td>
                  <td>{job.document_type}</td>
                  <td>
                    <StatusBadge status={job.status} />
                    {job.error_code && <span className="ml-2 font-mono text-xs text-red-300">{job.error_code}</span>}
                  </td>
                  <td>
                    {job.attempts}/{job.max_attempts}
                  </td>
                  <td className="text-slate-400">{new Date(job.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </Card>
    </div>
  );
}
