import type { ConfidenceDetails } from '../api/types';

/** Grounding of a value in the OCR text: shown per field so reviewers see what is unverified. */
export function GroundingBadge({ grounded }: { grounded: boolean | null | undefined }) {
  if (grounded === true) {
    return (
      <span className="rounded bg-emerald-900 px-1.5 py-0.5 text-xs text-emerald-200" title="Value found in the document text">
        Found in document
      </span>
    );
  }
  if (grounded === false) {
    return (
      <span className="rounded bg-red-900 px-1.5 py-0.5 text-xs text-red-200" title="Value not found in the document text">
        Not found in document
      </span>
    );
  }
  return (
    <span className="rounded bg-slate-700 px-1.5 py-0.5 text-xs text-slate-300" title="Empty or free-text field">
      Not checked
    </span>
  );
}

export function formatValue(value: unknown): string {
  if (value === null || value === undefined || value === '') return '—';
  if (typeof value === 'object') return JSON.stringify(value);
  return String(value);
}

interface Props {
  data: Record<string, unknown>;
  details: ConfidenceDetails | null;
  /** When set, values are editable and changes are reported here. */
  onChange?: (field: string, value: string) => void;
  edits?: Record<string, string>;
}

export function FieldTable({ data, details, onChange, edits }: Props) {
  const missing = new Set(details?.required_missing ?? []);
  return (
    <table className="w-full text-left text-sm">
      <thead className="text-xs uppercase text-slate-400">
        <tr>
          <th className="py-2 pr-4">Field</th>
          <th className="py-2 pr-4">Value</th>
          <th className="py-2">Evidence</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(data).map(([name, value]) => {
          const evidence = details?.fields?.[name];
          const editable = onChange && (value === null || typeof value !== 'object');
          return (
            <tr key={name} className="border-t border-slate-800" data-testid={`field-${name}`}>
              <td className="py-2 pr-4 font-mono text-xs text-slate-300">
                {name}
                {evidence?.required && <span className="ml-1 text-orange-400" title="Required field">*</span>}
              </td>
              <td className="py-2 pr-4">
                {editable ? (
                  <input
                    aria-label={name}
                    className="w-full rounded border border-slate-700 bg-slate-900 px-2 py-1"
                    value={edits?.[name] ?? (value === null ? '' : String(value))}
                    onChange={(e) => onChange(name, e.target.value)}
                  />
                ) : (
                  <span className="break-all">{formatValue(value)}</span>
                )}
              </td>
              <td className="py-2">
                {missing.has(name) ? (
                  <span className="rounded bg-red-900 px-1.5 py-0.5 text-xs text-red-200">Required, missing</span>
                ) : (
                  <GroundingBadge grounded={evidence?.grounded} />
                )}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export function ConfidenceSummary({ confidence, details }: { confidence: number | null; details: ConfidenceDetails | null }) {
  return (
    <div className="space-y-1 text-sm" data-testid="confidence-summary">
      <div>
        Confidence:{' '}
        <strong>{confidence === null ? 'not available' : `${Math.round(confidence * 100)}%`}</strong>
        {details?.ocr_confidence != null && (
          <span className="ml-3 text-slate-400">OCR word confidence {Math.round(details.ocr_confidence * 100)}%</span>
        )}
      </div>
      {details && details.required_ungrounded.length > 0 && (
        <div className="text-red-300">Not found in document: {details.required_ungrounded.join(', ')}</div>
      )}
      {details && details.required_missing.length > 0 && (
        <div className="text-red-300">Missing required: {details.required_missing.join(', ')}</div>
      )}
      {details?.checks
        .filter((c) => !c.passed)
        .map((c) => (
          <div key={c.name} className="text-amber-300">
            Check failed: {c.name} — {c.detail}
          </div>
        ))}
    </div>
  );
}
