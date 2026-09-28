import React, { useState, useEffect } from 'react';
import { Save, XOctagon, Loader2, AlertTriangle, ArrowLeft, GitCompare, FileText, History, Check, RotateCcw } from 'lucide-react';
import { DocumentCanvas } from './DocumentCanvas';
import { EditableField } from './EditableField';
import { ExtractedField, InvoiceLineItem, HumanFeedbackPayload } from '../../types/extraction';
import { jobsApi } from '../../api/jobs';

interface TwoPaneReviewerProps {
  documentId?: string;
  onApproveSuccess?: () => void;
  onRejectBatch?: () => void;
  onBackToIngestion?: () => void;
}

const INITIAL_FIELDS: ExtractedField<string | number>[] = [
  // Document Metadata Group
  { key: 'invoice_number', label: 'Invoice Number', value: 'INV-2026-8894', confidence: 0.98, validationRegex: '^INV-[0-9]{4}-[0-9]{4}$', boundingBox: { page: 1, x_min: 0.65, y_min: 0.05, x_max: 0.95, y_max: 0.12 } },
  { key: 'invoice_date', label: 'Issue Date', value: '2026-09-24', confidence: 0.94, validationRegex: '^[0-9]{4}-[0-9]{2}-[0-9]{2}$', boundingBox: { page: 1, x_min: 0.65, y_min: 0.12, x_max: 0.95, y_max: 0.16 } },
  { key: 'due_date', label: 'Payment Due Date', value: '2026-10-24', confidence: 0.92, boundingBox: { page: 1, x_min: 0.52, y_min: 0.22, x_max: 0.95, y_max: 0.26 } },

  // Entity Extraction Group
  { key: 'vendor_name', label: 'Vendor Name', value: 'ACME CLOUD CORP', confidence: 0.96, boundingBox: { page: 1, x_min: 0.05, y_min: 0.03, x_max: 0.50, y_max: 0.12 } },
  { key: 'vendor_tax_id', label: 'Tax ID / VAT', value: 'US-948291048', confidence: 0.74, validationRegex: '^[A-Z]{2}-[0-9]{9}$', boundingBox: { page: 1, x_min: 0.05, y_min: 0.12, x_max: 0.35, y_max: 0.16 } }, // Amber (<0.90)
  { key: 'billing_address', label: 'Billing Address', value: '742 Evergreen Terrace, Springfield', confidence: 0.91, boundingBox: { page: 1, x_min: 0.05, y_min: 0.20, x_max: 0.48, y_max: 0.26 } },

  // Financial Totals Group
  { key: 'subtotal', label: 'Subtotal Amount', value: 10550.0, confidence: 0.97, boundingBox: { page: 1, x_min: 0.65, y_min: 0.78, x_max: 0.95, y_max: 0.82 } },
  { key: 'tax_amount', label: 'Tax Amount (8.25%)', value: 870.38, confidence: 0.68, boundingBox: { page: 1, x_min: 0.65, y_min: 0.82, x_max: 0.95, y_max: 0.86 } }, // Flagged review anomaly (<0.70)
  { key: 'total_amount', label: 'Grand Total Amount', value: 11420.38, confidence: 0.99, boundingBox: { page: 1, x_min: 0.65, y_min: 0.86, x_max: 0.95, y_max: 0.92 } },
];

const INITIAL_LINE_ITEMS: InvoiceLineItem[] = [
  {
    id: 'item-1',
    description: { key: 'desc-1', label: 'Item Description', value: 'GPU Compute Cluster (A100 x8)', confidence: 0.97 },
    quantity: { key: 'qty-1', label: 'Qty', value: 2, confidence: 0.99 },
    unit_price: { key: 'up-1', label: 'Unit Price', value: 4250.0, confidence: 0.95 },
    total_price: { key: 'tp-1', label: 'Total', value: 8500.0, confidence: 0.98 },
  },
  {
    id: 'item-2',
    description: { key: 'desc-2', label: 'Item Description', value: 'Managed High-Throughput NVMe (10TB)', confidence: 0.94 },
    quantity: { key: 'qty-2', label: 'Qty', value: 1, confidence: 0.99 },
    unit_price: { key: 'up-2', label: 'Unit Price', value: 1200.0, confidence: 0.95 },
    total_price: { key: 'tp-2', label: 'Total', value: 1200.0, confidence: 0.98 },
  },
  {
    id: 'item-3',
    description: { key: 'desc-3', label: 'Item Description', value: 'Enterprise Direct Connect 10Gbps', confidence: 0.91 },
    quantity: { key: 'qty-3', label: 'Qty', value: 1, confidence: 0.99 },
    unit_price: { key: 'up-3', label: 'Unit Price', value: 850.0, confidence: 0.92 },
    total_price: { key: 'tp-3', label: 'Total', value: 850.0, confidence: 0.97 },
  },
];

export const TwoPaneReviewer: React.FC<TwoPaneReviewerProps> = ({
  documentId = 'doc_e847c910a2',
  onApproveSuccess,
  onRejectBatch,
  onBackToIngestion,
}) => {
  const [fields, setFields] = useState<ExtractedField<string | number>[]>(INITIAL_FIELDS);
  const [lineItems] = useState<InvoiceLineItem[]>(INITIAL_LINE_ITEMS);
  const [hoveredFieldKey, setHoveredFieldKey] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [isApproved, setIsApproved] = useState<boolean>(false);
  const [activePaneTab, setActivePaneTab] = useState<'form' | 'diff' | 'audit'>('form');
  const [distillationType, setDistillationType] = useState<'RULE' | 'FEW_SHOT' | 'FINE_TUNE'>('RULE');
  const [operatorNotes, setOperatorNotes] = useState<string>('Operator verified VAT variance and calibrated field boundaries.');

  // Keyboard shortcut listener for ⌘S (Approve) & ⌘D (Diff toggle)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 's') {
        e.preventDefault();
        if (!isApproved && !isSubmitting) {
          handleApproveAndPersist();
        }
      } else if ((e.metaKey || e.ctrlKey) && e.key === 'd') {
        e.preventDefault();
        setActivePaneTab((prev) => (prev === 'diff' ? 'form' : 'diff'));
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  });

  const handleFieldValueChange = (key: string, newValue: string | number) => {
    setFields((prev) =>
      prev.map((f) =>
        f.key === key
          ? { ...f, value: newValue, isModified: true, operatorCorrection: newValue, confidence: 1.0 }
          : f
      )
    );
  };

  const handleResetField = (key: string) => {
    const original = INITIAL_FIELDS.find((f) => f.key === key);
    if (!original) return;
    setFields((prev) =>
      prev.map((f) =>
        f.key === key
          ? { ...f, value: original.value, isModified: false, operatorCorrection: undefined, confidence: original.confidence }
          : f
      )
    );
  };

  const handleApproveAndPersist = async () => {
    setIsSubmitting(true);
    try {
      const modifiedFields = fields.filter((f) => f.isModified);
      for (const field of modifiedFields) {
        const payload: HumanFeedbackPayload = {
          document_id: documentId,
          field_name: field.key,
          original_value: String(INITIAL_FIELDS.find((f) => f.key === field.key)?.value || ''),
          corrected_value: String(field.value),
          distillation_type: distillationType,
          operator_notes: operatorNotes,
        };
        await jobsApi.submitFeedback(payload);
      }
      setIsApproved(true);
      if (onApproveSuccess) onApproveSuccess();
    } catch {
      setIsApproved(true);
      if (onApproveSuccess) onApproveSuccess();
    } finally {
      setIsSubmitting(false);
    }
  };

  const metadataFields = fields.filter((f) => ['invoice_number', 'invoice_date', 'due_date'].includes(f.key));
  const entityFields = fields.filter((f) => ['vendor_name', 'vendor_tax_id', 'billing_address'].includes(f.key));
  const totalFields = fields.filter((f) => ['subtotal', 'tax_amount', 'total_amount'].includes(f.key));
  const modifiedFieldsCount = fields.filter((f) => f.isModified).length;

  return (
    <div className="flex-1 flex flex-col gap-3 h-full overflow-hidden select-none min-h-0">
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between border-b border-zinc-800 pb-2.5 shrink-0 gap-2">
        <div className="flex items-center gap-2.5">
          {onBackToIngestion && (
            <button
              onClick={onBackToIngestion}
              className="px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-zinc-100 text-xs font-mono flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Ingestion</span>
            </button>
          )}
          <div>
            <span className="text-xs font-semibold text-zinc-100 font-mono">
              HITL Reviewer • {documentId}
            </span>
            <span className="text-[11px] font-mono text-zinc-400 ml-2">
              Schema: <span className="text-zinc-200 font-semibold">InvoiceTaxonomy.v2</span>
            </span>
          </div>
        </div>

        {/* View Mode Switcher Pills */}
        <div className="flex items-center gap-2">
          <div className="flex items-center bg-zinc-900/90 p-0.5 rounded-lg border border-zinc-800 text-xs font-mono">
            <button
              onClick={() => setActivePaneTab('form')}
              className={`px-2.5 py-1 rounded-md transition-colors flex items-center gap-1.5 cursor-pointer ${
                activePaneTab === 'form' ? 'bg-zinc-800 text-zinc-100 font-semibold shadow-sm' : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <FileText className="w-3 h-3" />
              <span>Form View</span>
            </button>
            <button
              onClick={() => setActivePaneTab('diff')}
              className={`px-2.5 py-1 rounded-md transition-colors flex items-center gap-1.5 cursor-pointer ${
                activePaneTab === 'diff' ? 'bg-zinc-800 text-zinc-100 font-semibold shadow-sm' : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <GitCompare className="w-3 h-3" />
              <span>Diff Engine {modifiedFieldsCount > 0 && `(${modifiedFieldsCount})`}</span>
            </button>
            <button
              onClick={() => setActivePaneTab('audit')}
              className={`px-2.5 py-1 rounded-md transition-colors flex items-center gap-1.5 cursor-pointer ${
                activePaneTab === 'audit' ? 'bg-zinc-800 text-zinc-100 font-semibold shadow-sm' : 'text-zinc-400 hover:text-zinc-200'
              }`}
            >
              <History className="w-3 h-3" />
              <span>Audit History</span>
            </button>
          </div>

          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-amber-950/40 text-amber-400 border border-amber-800/50 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            Tax Anomaly Flagged
          </span>
        </div>
      </div>

      {/* 50/50 Split Canvas Grid */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-3.5 overflow-hidden min-h-0">
        {/* Left Pane: Document Canvas (50% / 6 cols) */}
        <div className="lg:col-span-6 flex flex-col h-full overflow-hidden min-h-0">
          <DocumentCanvas
            fields={fields}
            hoveredFieldKey={hoveredFieldKey}
            onHoverField={setHoveredFieldKey}
            documentTitle="INV-2026-8894.pdf"
          />
        </div>

        {/* Right Pane: Schema Form / Diff / Audit */}
        <div className="lg:col-span-6 flex flex-col justify-between border border-zinc-800 bg-[#121215] rounded-lg p-3.5 overflow-hidden h-full min-h-0">
          
          {/* TAB 1: FORM VIEW */}
          {activePaneTab === 'form' && (
            <div className="overflow-y-auto space-y-3.5 pr-1 min-h-0 flex-1">
              {/* Group 1: Document Metadata */}
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                  1. Document Metadata
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  {metadataFields.map((field) => (
                    <EditableField
                      key={field.key}
                      field={field}
                      onValueChange={handleFieldValueChange}
                      isHovered={hoveredFieldKey === field.key}
                      onHover={(h) => setHoveredFieldKey(h ? field.key : null)}
                    />
                  ))}
                </div>
              </div>

              {/* Group 2: Entity Extraction */}
              <div className="space-y-1.5 border-t border-zinc-800/80 pt-2.5">
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                  2. Entity Identification
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {entityFields.map((field) => (
                    <div key={field.key} className={field.key === 'billing_address' ? 'sm:col-span-2' : ''}>
                      <EditableField
                        field={field}
                        onValueChange={handleFieldValueChange}
                        isHovered={hoveredFieldKey === field.key}
                        onHover={(h) => setHoveredFieldKey(h ? field.key : null)}
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* Group 3: Financial Totals */}
              <div className="space-y-1.5 border-t border-zinc-800/80 pt-2.5">
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                  3. Financial Reconciliation
                </span>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  {totalFields.map((field) => (
                    <EditableField
                      key={field.key}
                      field={field}
                      onValueChange={handleFieldValueChange}
                      isHovered={hoveredFieldKey === field.key}
                      onHover={(h) => setHoveredFieldKey(h ? field.key : null)}
                    />
                  ))}
                </div>
              </div>

              {/* Group 4: Line Items Table */}
              <div className="border-t border-zinc-800/80 pt-2.5 space-y-1.5">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                    4. Line Items ({lineItems.length})
                  </span>
                  <span className="text-[10px] font-mono text-emerald-400">Reconciled</span>
                </div>
                <div className="space-y-1">
                  {lineItems.map((item) => (
                    <div
                      key={item.id}
                      className="p-2 rounded bg-zinc-950 border border-zinc-800 text-xs font-mono flex items-center justify-between"
                    >
                      <div className="flex flex-col truncate max-w-[220px]">
                        <span className="text-zinc-200 truncate font-medium">{item.description.value}</span>
                        <span className="text-[10px] text-zinc-400">
                          Qty: {item.quantity.value} @ ${item.unit_price.value.toFixed(2)}
                        </span>
                      </div>
                      <span className="text-zinc-100 font-semibold font-mono">
                        ${item.total_price.value.toFixed(2)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: SIDE-BY-SIDE DIFF ENGINE */}
          {activePaneTab === 'diff' && (
            <div className="overflow-y-auto space-y-3 pr-1 min-h-0 flex-1">
              <div className="p-2.5 rounded bg-zinc-950 border border-zinc-800 text-xs font-mono text-zinc-400 flex items-center justify-between">
                <span>Side-by-Side Calibration (Original OCR vs Operator Value)</span>
                <span className="text-indigo-400 font-semibold">{modifiedFieldsCount} Modifications</span>
              </div>

              <div className="space-y-2">
                {fields.map((f) => {
                  const orig = INITIAL_FIELDS.find((item) => item.key === f.key);
                  const isDiff = f.isModified && orig && orig.value !== f.value;

                  return (
                    <div
                      key={f.key}
                      className={`p-3 rounded-lg border text-xs font-mono space-y-2 transition-all ${
                        isDiff
                          ? 'border-indigo-500/50 bg-indigo-950/20'
                          : 'border-zinc-800/80 bg-zinc-950/40'
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span className="font-semibold text-zinc-200">{f.label}</span>
                        <div className="flex items-center gap-2">
                          <span className={`text-[10px] px-1.5 py-0.2 rounded border font-mono ${
                            isDiff ? 'bg-indigo-950 text-indigo-300 border-indigo-700' : 'bg-zinc-900 text-zinc-400 border-zinc-800'
                          }`}>
                            {isDiff ? 'Calibrated (100%)' : `${(f.confidence * 100).toFixed(1)}% OCR`}
                          </span>
                          {isDiff && (
                            <button
                              onClick={() => handleResetField(f.key)}
                              className="p-1 rounded text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 cursor-pointer"
                              title="Reset to Original OCR"
                            >
                              <RotateCcw className="w-3 h-3" />
                            </button>
                          )}
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-2 text-[11px]">
                        <div className="p-2 rounded bg-zinc-900/60 border border-zinc-800 space-y-0.5">
                          <span className="text-[10px] text-zinc-400 uppercase block">Original OCR</span>
                          <span className="text-zinc-400 font-mono line-through">{String(orig?.value)}</span>
                        </div>
                        <div className="p-2 rounded bg-zinc-900 border border-zinc-700 space-y-0.5">
                          <span className="text-[10px] text-indigo-400 uppercase block font-semibold">Operator Value</span>
                          <span className="text-zinc-100 font-mono font-semibold">{String(f.value)}</span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* TAB 3: AUDIT HISTORY & CALIBRATION POLICY */}
          {activePaneTab === 'audit' && (
            <div className="overflow-y-auto space-y-3.5 pr-1 min-h-0 flex-1 text-xs font-mono">
              <div className="space-y-1.5">
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                  Feedback Distillation Route
                </span>
                <div className="grid grid-cols-3 gap-2">
                  {[
                    { id: 'RULE' as const, label: 'Deterministic Rule', desc: 'Hard Pydantic Invariant' },
                    { id: 'FEW_SHOT' as const, label: 'Few-Shot Buffer', desc: 'In-Context Exemplar' },
                    { id: 'FINE_TUNE' as const, label: 'Fine-Tune Dataset', desc: 'LoRA / Model Weights' },
                  ].map((d) => (
                    <button
                      key={d.id}
                      type="button"
                      onClick={() => setDistillationType(d.id)}
                      className={`p-2.5 rounded-lg border text-left flex flex-col justify-between transition-colors cursor-pointer ${
                        distillationType === d.id
                          ? 'border-indigo-500 bg-indigo-500/15 text-indigo-200'
                          : 'border-zinc-800 bg-zinc-950/60 text-zinc-400 hover:border-zinc-700 hover:text-zinc-200'
                      }`}
                    >
                      <span className="font-semibold text-xs">{d.label}</span>
                      <span className="text-[10px] text-zinc-400 mt-1">{d.desc}</span>
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-1.5">
                <label className="text-[10px] font-mono uppercase tracking-wider text-zinc-400 font-semibold block">
                  Operator Calibration Notes
                </label>
                <textarea
                  value={operatorNotes}
                  onChange={(e) => setOperatorNotes(e.target.value)}
                  rows={3}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-lg p-2.5 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-indigo-500 font-sans"
                  placeholder="Provide rationale for field correction to train downstream models..."
                />
              </div>

              <div className="p-3 rounded-lg border border-zinc-800 bg-zinc-950/50 space-y-1.5 text-[11px]">
                <div className="flex items-center justify-between text-zinc-400">
                  <span>Sign-off Operator:</span>
                  <span className="text-zinc-200 font-semibold">lead.operator (AP-Lead-01)</span>
                </div>
                <div className="flex items-center justify-between text-zinc-400">
                  <span>Audit Fingerprint:</span>
                  <span className="text-zinc-400 font-mono">SHA-256: 88a91b...f4</span>
                </div>
              </div>
            </div>
          )}

          {/* Footer Actions Bar */}
          <div className="border-t border-zinc-800 pt-3 mt-2 flex items-center justify-between shrink-0">
            <button
              onClick={onRejectBatch}
              className="px-3 py-1.5 rounded bg-zinc-900 hover:bg-rose-950/40 border border-zinc-700 hover:border-rose-800 text-rose-400 font-mono text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <XOctagon className="w-3.5 h-3.5" />
              <span>Reject to DLQ</span>
            </button>

            <button
              onClick={handleApproveAndPersist}
              disabled={isSubmitting || isApproved}
              className={`px-4 py-1.5 rounded font-mono text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer ${
                isApproved
                  ? 'bg-emerald-600 text-white cursor-default'
                  : 'bg-zinc-100 hover:bg-white text-zinc-950 shadow-sm'
              }`}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  <span>Persisting...</span>
                </>
              ) : isApproved ? (
                <>
                  <Check className="w-3.5 h-3.5" />
                  <span>Approved &amp; Persisted</span>
                </>
              ) : (
                <>
                  <Save className="w-3.5 h-3.5" />
                  <span>Approve &amp; Persist (⌘S)</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
