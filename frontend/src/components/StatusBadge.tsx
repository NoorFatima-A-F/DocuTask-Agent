import clsx from 'clsx';

const STYLES: Record<string, string> = {
  QUEUED: 'bg-slate-700 text-slate-100',
  RUNNING: 'bg-blue-700 text-blue-50',
  RETRYING: 'bg-amber-700 text-amber-50',
  COMPLETED: 'bg-emerald-700 text-emerald-50',
  NEEDS_REVIEW: 'bg-orange-600 text-orange-50',
  FAILED: 'bg-red-700 text-red-50',
};

const LABELS: Record<string, string> = { NEEDS_REVIEW: 'Needs review' };

export function StatusBadge({ status }: { status: string }) {
  return (
    <span
      data-testid="status-badge"
      className={clsx('rounded px-2 py-0.5 text-xs font-semibold', STYLES[status] ?? 'bg-slate-600 text-white')}
    >
      {LABELS[status] ?? status.charAt(0) + status.slice(1).toLowerCase()}
    </span>
  );
}
