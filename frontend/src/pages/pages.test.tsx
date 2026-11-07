import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import type { ReactNode } from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { api } from '../api/api';
import { extraction, job, reviewDetail } from '../test/fixtures';
import { HomePage } from './HomePage';
import { JobPage } from './JobPage';
import { ReviewPage, buildCorrections } from './ReviewPages';

vi.mock('../api/api', () => ({
  api: {
    jobs: vi.fn(),
    documents: vi.fn(),
    upload: vi.fn(),
    createJob: vi.fn(),
    job: vi.fn(),
    retryJob: vi.fn(),
    extraction: vi.fn(),
    review: vi.fn(),
    approve: vi.fn(),
    reject: vi.fn(),
    documentBlob: vi.fn(),
  },
}));

const mocked = vi.mocked(api);

function wrap(ui: ReactNode) {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(<QueryClientProvider client={client}>{ui}</QueryClientProvider>);
}

beforeEach(() => {
  vi.clearAllMocks();
  mocked.documents.mockResolvedValue({ items: [], total: 0, page: 1, page_size: 50 });
  mocked.documentBlob.mockResolvedValue(new Blob(['x'], { type: 'image/png' }));
  globalThis.URL.createObjectURL = vi.fn(() => 'blob:doc');
  globalThis.URL.revokeObjectURL = vi.fn();
});

describe('HomePage', () => {
  it('uploads, creates a job with the chosen type and lists real job statuses', async () => {
    mocked.jobs.mockResolvedValue({ items: [job({ status: 'FAILED', error_code: 'LLM_TIMEOUT' })], total: 1, page: 1, page_size: 50 });
    mocked.upload.mockResolvedValue({
      document: { id: 'doc-1', original_filename: 'r.png', mime_type: 'image/png', file_size: 1, upload_status: 'UPLOADED', created_at: '' },
      is_duplicate: false,
      message: 'ok',
    });
    mocked.createJob.mockResolvedValue(job({ id: 'job-1' }));
    wrap(<HomePage />);

    const row = await screen.findByTestId('job-row');
    expect(within(row).getByText('Failed')).toBeInTheDocument();
    expect(within(row).getByText('LLM_TIMEOUT')).toBeInTheDocument();

    const user = userEvent.setup();
    await user.upload(screen.getByLabelText('Document file'), new File(['png'], 'r.png', { type: 'image/png' }));
    await user.selectOptions(screen.getByLabelText('Document type'), 'receipt');
    await user.click(screen.getByRole('button', { name: 'Upload and extract' }));

    await waitFor(() => expect(mocked.createJob).toHaveBeenCalledWith('doc-1', 'receipt'));
    expect(window.location.pathname).toBe('/jobs/job-1');
  });

  it('shows the backend error code when the queue is down', async () => {
    mocked.jobs.mockResolvedValue({ items: [], total: 0, page: 1, page_size: 50 });
    mocked.upload.mockResolvedValue({
      document: { id: 'doc-1', original_filename: 'r.png', mime_type: 'image/png', file_size: 1, upload_status: 'UPLOADED', created_at: '' },
      is_duplicate: false,
      message: 'ok',
    });
    const err = Object.assign(new Error('x'), {
      isAxiosError: true,
      response: { status: 503, data: { message: 'Job queue is not reachable', errors: { error_code: 'QUEUE_UNAVAILABLE' } } },
    });
    mocked.createJob.mockRejectedValue(err);
    wrap(<HomePage />);
    const user = userEvent.setup();
    await user.upload(screen.getByLabelText('Document file'), new File(['png'], 'r.png', { type: 'image/png' }));
    await user.click(screen.getByRole('button', { name: 'Upload and extract' }));
    expect(await screen.findByRole('alert')).toHaveTextContent('Job queue is not reachable (QUEUE_UNAVAILABLE)');
  });
});

describe('JobPage', () => {
  it('polls until the job finishes, then shows grounding evidence and marks NEEDS_REVIEW as not final', async () => {
    mocked.job.mockResolvedValueOnce(job({ status: 'RUNNING' })).mockResolvedValue(job({ status: 'NEEDS_REVIEW' }));
    mocked.extraction.mockResolvedValue(extraction('NEEDS_REVIEW'));
    wrap(<JobPage jobId="11111111-1111-1111-1111-111111111111" />);

    expect(await screen.findByText('Running OCR and extraction.')).toBeInTheDocument();
    expect(await screen.findByText(/Not final/, {}, { timeout: 4000 })).toBeInTheDocument();
    expect(within(screen.getByTestId('field-vendor_name')).getByText('Not found in document')).toBeInTheDocument();
    expect(within(screen.getByTestId('field-total_amount')).getByText('Found in document')).toBeInTheDocument();
    expect(within(screen.getByTestId('field-notes')).getByText('Not checked')).toBeInTheDocument();
    expect(screen.getByTestId('confidence-summary')).toHaveTextContent('62%');
    expect(screen.getByTestId('confidence-summary')).toHaveTextContent('Check failed: line_items_sum');
    expect(mocked.job.mock.calls.length).toBeGreaterThanOrEqual(2);
  });

  it('shows the final (approved) values for COMPLETED extractions', async () => {
    mocked.job.mockResolvedValue(job({ status: 'COMPLETED' }));
    mocked.extraction.mockResolvedValue(extraction('COMPLETED'));
    wrap(<JobPage jobId="j" />);
    expect(await screen.findByText('Contoso Ltd')).toBeInTheDocument();
    expect(screen.queryByText(/Not final/)).not.toBeInTheDocument();
  });

  it('shows the failure code and offers a retry; no extraction is fetched', async () => {
    mocked.job.mockResolvedValue(job({ status: 'FAILED', error_code: 'LLM_AUTH_FAILED', last_error: 'rejected credentials' }));
    mocked.retryJob.mockResolvedValue(job({ status: 'QUEUED' }));
    wrap(<JobPage jobId="j" />);
    expect(await screen.findByTestId('job-error')).toHaveTextContent('LLM_AUTH_FAILED: rejected credentials');
    expect(mocked.extraction).not.toHaveBeenCalled();
    await userEvent.setup().click(screen.getByRole('button', { name: 'Retry' }));
    expect(mocked.retryJob).toHaveBeenCalledWith('j');
    expect(await screen.findByText('Waiting for a worker.')).toBeInTheDocument();
  });
});

describe('ReviewPage', () => {
  it('shows OCR text and sends only changed fields as typed corrections', async () => {
    mocked.review.mockResolvedValue(reviewDetail());
    mocked.approve.mockResolvedValue({});
    wrap(<ReviewPage extractionId="33333333-3333-3333-3333-333333333333" />);
    expect(await screen.findByTestId('ocr-text')).toHaveTextContent('Contoso Ltd');

    const user = userEvent.setup();
    const vendor = screen.getByLabelText('vendor_name');
    await user.clear(vendor);
    await user.type(vendor, 'Contoso Ltd');
    await user.click(screen.getByRole('button', { name: 'Approve with corrections' }));
    await waitFor(() =>
      expect(mocked.approve).toHaveBeenCalledWith('33333333-3333-3333-3333-333333333333', { vendor_name: 'Contoso Ltd' }),
    );
  });

  it('requires a reason to reject', async () => {
    mocked.review.mockResolvedValue(reviewDetail());
    mocked.reject.mockResolvedValue({});
    wrap(<ReviewPage extractionId="e" />);
    const reject = await screen.findByRole('button', { name: 'Reject' });
    expect(reject).toBeDisabled();
    await userEvent.setup().type(screen.getByLabelText('Rejection reason'), 'wrong vendor');
    await userEvent.setup().click(reject);
    expect(mocked.reject).toHaveBeenCalledWith('e', 'wrong vendor');
  });
});

describe('buildCorrections', () => {
  it('keeps types and drops unchanged values', () => {
    expect(buildCorrections({ a: 1, b: 'x', c: null }, { a: '2', b: 'x', c: '' })).toEqual({ a: 2 });
    expect(buildCorrections({ a: 1 }, { a: '' })).toEqual({ a: null });
    expect(buildCorrections({ a: 1 }, {})).toBeNull();
  });
});
