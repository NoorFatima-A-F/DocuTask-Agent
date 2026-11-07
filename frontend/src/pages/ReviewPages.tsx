import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useEffect, useState } from 'react';
import { api } from '../api/api';
import { errorMessage } from '../api/client';
import type { ReviewDetail } from '../api/types';
import { ConfidenceSummary, FieldTable } from '../components/FieldTable';
import { StatusBadge } from '../components/StatusBadge';
import { Button, Card, ErrorBox, Link } from '../components/ui';
import { navigate } from '../router';

export function ReviewQueuePage() {
  const reviews = useQuery({ queryKey: ['reviews'], queryFn: api.reviews });
  return (
    <Card title="Review queue">
      <ErrorBox message={reviews.error ? errorMessage(reviews.error) : null} />
      {reviews.data && reviews.data.items.length === 0 && <p className="text-sm text-slate-400">Nothing to review.</p>}
      {reviews.data && reviews.data.items.length > 0 && (
        <table className="w-full text-left text-sm">
          <thead className="text-xs uppercase text-slate-400">
            <tr>
              <th className="py-2">Extraction</th>
              <th>Type</th>
              <th>Confidence</th>
              <th>Created</th>
            </tr>
          </thead>
          <tbody>
            {reviews.data.items.map((r) => (
              <tr key={r.extraction_id} className="border-t border-slate-800" data-testid="review-row">
                <td className="py-2">
                  <Link to={`/reviews/${r.extraction_id}`}>{r.extraction_id.slice(0, 8)}</Link>
                </td>
                <td>{r.document_type}</td>
                <td>{r.confidence === null ? '—' : `${Math.round(r.confidence * 100)}%`}</td>
                <td className="text-slate-400">{new Date(r.created_at).toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </Card>
  );
}

/** Only fields the reviewer changed are sent, converted back to the original JSON type. */
export function buildCorrections(original: Record<string, unknown>, edits: Record<string, string>): Record<string, unknown> | null {
  const corrections: Record<string, unknown> = {};
  for (const [field, text] of Object.entries(edits)) {
    const before = original[field];
    const current = before === null || before === undefined ? '' : String(before);
    if (text === current) continue;
    if (text.trim() === '') corrections[field] = null;
    else if (typeof before === 'number' && !Number.isNaN(Number(text))) corrections[field] = Number(text);
    else corrections[field] = text;
  }
  return Object.keys(corrections).length ? corrections : null;
}

export function ReviewPage({ extractionId }: { extractionId: string }) {
  const queryClient = useQueryClient();
  const review = useQuery({ queryKey: ['review', extractionId], queryFn: () => api.review(extractionId) });
  const [edits, setEdits] = useState<Record<string, string>>({});
  const [reason, setReason] = useState('');

  const done = () => {
    queryClient.invalidateQueries({ queryKey: ['reviews'] });
    navigate('/reviews');
  };
  const approve = useMutation({
    mutationFn: () => api.approve(extractionId, buildCorrections(review.data?.structured_json ?? {}, edits)),
    onSuccess: done,
  });
  const reject = useMutation({ mutationFn: () => api.reject(extractionId, reason), onSuccess: done });

  if (review.error) return <ErrorBox message={errorMessage(review.error)} />;
  if (!review.data) return <p className="text-sm text-slate-400">Loading…</p>;
  const r = review.data;
  const mutationError = approve.error ?? reject.error;

  return (
    <div className="space-y-4">
      <Link to="/reviews">← Review queue</Link>
      <div className="grid gap-4 lg:grid-cols-2">
        <div className="space-y-4">
          <DocumentPreview review={r} />
          <Card title="OCR text">
            <pre className="max-h-96 overflow-auto whitespace-pre-wrap text-xs text-slate-300" data-testid="ocr-text">
              {r.ocr_text || '(no text)'}
            </pre>
          </Card>
        </div>
        <Card title={`Extracted ${r.document_type}`} actions={<StatusBadge status={r.status} />}>
          <ConfidenceSummary confidence={r.confidence} details={r.confidence_details} />
          <div className="mt-4">
            {r.structured_json ? (
              <FieldTable
                data={r.structured_json}
                details={r.confidence_details}
                edits={edits}
                onChange={(field, value) => setEdits((prev) => ({ ...prev, [field]: value }))}
              />
            ) : (
              <p className="text-sm text-slate-400">No data.</p>
            )}
          </div>
          <div className="mt-4 space-y-3">
            <ErrorBox message={mutationError ? errorMessage(mutationError) : null} />
            <Button onClick={() => approve.mutate()} disabled={approve.isPending || reject.isPending}>
              Approve{Object.keys(edits).length ? ' with corrections' : ''}
            </Button>
            <div className="flex gap-2">
              <input
                aria-label="Rejection reason"
                placeholder="Reason for rejection"
                className="flex-1 rounded border border-slate-700 bg-slate-950 px-2 py-1 text-sm"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
              />
              <Button
                variant="danger"
                onClick={() => reject.mutate()}
                disabled={reason.trim().length < 3 || approve.isPending || reject.isPending}
              >
                Reject
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

function DocumentPreview({ review }: { review: ReviewDetail }) {
  const [url, setUrl] = useState<string | null>(null);
  const [type, setType] = useState('');
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    let objectUrl: string | null = null;
    api
      .documentBlob(review.document_download_url)
      .then((blob) => {
        objectUrl = URL.createObjectURL(blob);
        setType(blob.type);
        setUrl(objectUrl);
      })
      .catch((err) => setError(errorMessage(err)));
    return () => {
      if (objectUrl) URL.revokeObjectURL(objectUrl);
    };
  }, [review.document_download_url]);

  return (
    <Card title={review.document_filename ?? 'Document'}>
      <ErrorBox message={error} />
      {url && type.startsWith('image/') && <img src={url} alt="Source document" className="max-h-[32rem] w-full object-contain" />}
      {url && type === 'application/pdf' && <iframe title="Source document" src={url} className="h-[32rem] w-full" />}
      {url && (
        <a className="mt-2 inline-block text-sm text-blue-400 hover:underline" href={url} download={review.document_filename ?? 'document'}>
          Download original
        </a>
      )}
    </Card>
  );
}
