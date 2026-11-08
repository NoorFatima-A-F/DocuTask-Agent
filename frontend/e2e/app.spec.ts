import { expect, test, type Page, type Route } from '@playwright/test';

const USER = { id: 'u1', email: 'a@example.com', username: 'alice', role: 'reviewer', is_active: true, is_superuser: false };
const JOB_ID = '11111111-1111-1111-1111-111111111111';
const DOC_ID = '22222222-2222-2222-2222-222222222222';
const EXT_ID = '33333333-3333-3333-3333-333333333333';
const ok = (data: unknown) => ({ status: 200, contentType: 'application/json', body: JSON.stringify({ success: true, message: '', data }) });
const job = (status: string, extra: Record<string, unknown> = {}) => ({
  id: JOB_ID, document_id: DOC_ID, document_type: 'invoice', status, attempts: 1, max_attempts: 4,
  error_code: null, last_error: null, started_at: null, completed_at: null,
  created_at: '2026-11-08T10:00:00Z', updated_at: `2026-11-08T10:00:0${status.length % 10}Z`, ...extra,
});
const details = {
  score: 0.62,
  fields: {
    vendor_name: { value: 'Northwind Traders', grounded: false, score: 40, required: true },
    total_amount: { value: 1250, grounded: true, score: 100, required: true },
  },
  required_missing: [], required_ungrounded: ['vendor_name'], checks: [], failed_checks: [], ocr_confidence: 0.93,
};

async function stubApi(page: Page, jobStatuses: string[]) {
  let polls = 0;
  const calls: { method: string; path: string; body: unknown }[] = [];
  await page.route('**/api/v1/**', async (route: Route) => {
    const req = route.request();
    const path = new URL(req.url()).pathname.replace('/api/v1', '');
    const isJson = (req.headers()['content-type'] ?? '').includes('application/json');
    calls.push({ method: req.method(), path, body: isJson ? req.postDataJSON() : null });
    if (path === '/auth/login') return route.fulfill(ok({ access_token: 'a', refresh_token: 'r', token_type: 'bearer' }));
    if (path === '/auth/me') return route.fulfill(ok(USER));
    if (path === '/documents/upload')
      return route.fulfill({ ...ok({ document: { id: DOC_ID, original_filename: 'inv.png' }, is_duplicate: false, message: '' }), status: 201 });
    if (path === '/documents') return route.fulfill(ok({ items: [{ id: DOC_ID, original_filename: 'inv.png' }], total: 1, page: 1, page_size: 50 }));
    if (path === '/jobs' && req.method() === 'POST') return route.fulfill({ ...ok(job('QUEUED')), status: 202 });
    if (path === '/jobs') return route.fulfill(ok({ items: [job(jobStatuses.at(-1)!)], total: 1, page: 1, page_size: 50 }));
    if (path === `/jobs/${JOB_ID}`) return route.fulfill(ok(job(jobStatuses[Math.min(polls++, jobStatuses.length - 1)])));
    if (path === `/ai/result/${DOC_ID}`)
      return route.fulfill(ok({
        id: EXT_ID,
        metadata: { document_id: DOC_ID, document_type: 'invoice', provider: 'gemini', model: 'gemini-3.8-flash', created_at: '' },
        statistics: { processing_time_ms: 1800, estimated_cost: null },
        result: { status: 'NEEDS_REVIEW', structured_json: { vendor_name: 'Northwind Traders', total_amount: 1250 }, final_json: null,
          confidence: 0.62, confidence_details: details, error_code: null, error_message: null },
      }));
    if (path === '/reviews') return route.fulfill(ok({ items: [{ extraction_id: EXT_ID, document_id: DOC_ID, document_type: 'invoice', status: 'NEEDS_REVIEW', confidence: 0.62, created_at: '2026-11-08T10:00:00Z' }], total: 1, page: 1, page_size: 20 }));
    if (path === `/reviews/${EXT_ID}`)
      return route.fulfill(ok({ extraction_id: EXT_ID, document_id: DOC_ID, document_type: 'invoice', status: 'NEEDS_REVIEW', confidence: 0.62,
        created_at: '', structured_json: { vendor_name: 'Northwind Traders', total_amount: 1250 }, final_json: null,
        confidence_details: details, error_code: null, ocr_text: 'INVOICE Contoso Ltd Total 1,250.00', document_filename: 'inv.png',
        document_download_url: `/api/v1/reviews/${EXT_ID}/document` }));
    if (path === `/reviews/${EXT_ID}/document`) return route.fulfill({ status: 200, contentType: 'image/png', body: Buffer.from('89504e470d0a1a0a', 'hex') });
    if (path === `/reviews/${EXT_ID}/approve`) return route.fulfill(ok({ status: 'COMPLETED' }));
    return route.fulfill({ status: 404, contentType: 'application/json', body: JSON.stringify({ success: false, message: `unstubbed ${path}` }) });
  });
  return calls;
}

async function signIn(page: Page) {
  await page.goto('/');
  await page.getByLabel('Username or email').fill('alice');
  await page.getByLabel('Password').fill('Password123!');
  await page.getByRole('button', { name: 'Sign in' }).click();
}

test('upload -> job polls to NEEDS_REVIEW -> evidence shown', async ({ page }) => {
  const calls = await stubApi(page, ['QUEUED', 'RUNNING', 'NEEDS_REVIEW']);
  await signIn(page);
  await page.getByLabel('Document file').setInputFiles({ name: 'inv.png', mimeType: 'image/png', buffer: Buffer.from('89504e47', 'hex') });
  await page.getByRole('button', { name: 'Upload and extract' }).click();

  await expect(page).toHaveURL(new RegExp(`/jobs/${JOB_ID}$`));
  await expect(page.getByText('Not final: a reviewer must approve')).toBeVisible({ timeout: 15_000 });
  await expect(page.getByTestId('field-vendor_name')).toContainText('Not found in document');
  await expect(page.getByTestId('field-total_amount')).toContainText('Found in document');
  expect(calls.filter((c) => c.path === `/jobs/${JOB_ID}`).length).toBeGreaterThanOrEqual(3);
  expect(calls.find((c) => c.path === '/jobs' && c.method === 'POST')?.body).toEqual({ document_id: DOC_ID, document_type: 'invoice' });
});

test('reviewer corrects a field and approves', async ({ page }) => {
  const calls = await stubApi(page, ['NEEDS_REVIEW']);
  await signIn(page);
  await page.getByRole('link', { name: 'Review queue' }).click();
  await page.getByRole('link', { name: EXT_ID.slice(0, 8) }).click();
  await expect(page.getByTestId('ocr-text')).toContainText('Contoso Ltd');
  await page.getByLabel('vendor_name').fill('Contoso Ltd');
  await page.getByRole('button', { name: 'Approve with corrections' }).click();
  await expect(page).toHaveURL(/\/reviews$/);
  expect(calls.find((c) => c.path.endsWith('/approve'))?.body).toEqual({ corrections: { vendor_name: 'Contoso Ltd' } });
});
