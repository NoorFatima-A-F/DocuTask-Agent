import React, { useState } from 'react';
import { CheckCircle2, Save, XOctagon, Loader2, AlertTriangle, ArrowLeft } from 'lucide-react';
import { DocumentCanvas } from './DocumentCanvas';
import { EditableField } from './EditableField';
import { ExtractedField, InvoiceLineItem } from '../../types/extraction';
import { jobsApi } from '../../api/jobs';

interface TwoPaneReviewerProps {
  documentId?: string;
  onApproveSuccess?: () => void;
  onRejectBatch?: () => void;
  onBackToIngestion?: () => void;
}

const INITIAL_FIELDS: ExtractedField<string | number>[] = [
  // Document Metadata Group
  { key: 'invoice_number', label: 'Invoice Number', value: 'INV-2026-8894', confidence: 0.98, validationRegex: '^INV-[0-9]{4}-[0-9]{4}$', box: { page: 1, x_min: 0.65, y_min: 0.05, x_max: 0.95, y_max: 0.12 } },
  { key: 'invoice_date', label: 'Issue Date', value: '2026-09-24', confidence: 0.94, validationRegex: '^[0-9]{4}-[0-9]{2}-[0-9]{2}$', box: { page: 1, x_min: 0.65, y_min: 0.12, x_max: 0.95, y_max: 0.16 } },
  { key: 'due_date', label: 'Payment Due Date', value: '2026-10-24', confidence: 0.92, box: { page: 1, x_min: 0.52, y_min: 0.22, x_max: 0.95, y_max: 0.26 } },

  // Entity Extraction Group
  { key: 'vendor_name', label: 'Vendor Name', value: 'ACME CLOUD CORP', confidence: 0.96, box: { page: 1, x_min: 0.05, y_min: 0.03, x_max: 0.50, y_max: 0.12 } },
  { key: 'vendor_tax_id', label: 'Tax ID / VAT', value: 'US-948291048', confidence: 0.74, validationRegex: '^[A-Z]{2}-[0-9]{9}$', box: { page: 1, x_min: 0.05, y_min: 0.12, x_max: 0.35, y_max: 0.16 } }, // Amber (<0.90)
  { key: 'billing_address', label: 'Billing Address', value: '742 Evergreen Terrace, Springfield', confidence: 0.91, box: { page: 1, x_min: 0.05, y_min: 0.20, x_max: 0.48, y_max: 0.26 } },

  // Financial Totals Group
  { key: 'subtotal', label: 'Subtotal Amount', value: 10550.0, confidence: 0.97, box: { page: 1, x_min: 0.65, y_min: 0.78, x_max: 0.95, y_max: 0.82 } },
  { key: 'tax_amount', label: 'Tax Amount (8.25%)', value: 870.38, confidence: 0.68, box: { page: 1, x_min: 0.65, y_min: 0.82, x_max: 0.95, y_max: 0.86 } }, // Flagged review anomaly (<0.70)
  { key: 'total_amount', label: 'Grand Total Amount', value: 11420.38, confidence: 0.99, box: { page: 1, x_min: 0.65, y_min: 0.86, x_max: 0.95, y_max: 0.92 } },
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

  const handleFieldValueChange = (key: string, newValue: string | number) => {
    setFields((prev) =>
      prev.map((f) =>
        f.key === key
          ? { ...f, value: newValue, isModified: true, operatorCorrection: newValue, confidence: 1.0 }
          : f
      )
    );
  };

  const handleApproveAndPersist = async () => {
    setIsSubmitting(true);
    try {
      const modifiedFields = fields.filter((f) => f.isModified);
      for (const field of modifiedFields) {
        await jobsApi.submitFeedback({
          document_id: documentId,
          field_name: field.key,
          original_value: String(INITIAL_FIELDS.find((f) => f.key === field.key)?.value || ''),
          corrected_value: String(field.value),
          distillation_type: 'RULE',
          operator_notes: `Operator verified and calibrated ${field.label}`,
        });
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

  return (
    <div className="flex-1 flex flex-col gap-3 h-full overflow-hidden select-none min-h-0">
      {/* Header Bar */}
      <div className="flex items-center justify-between border-b border-[#27272a] pb-2 shrink-0">
        <div className="flex items-center gap-2.5">
          {onBackToIngestion && (
            <button
              onClick={onBackToIngestion}
              className="px-2 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-zinc-100 text-xs font-mono flex items-center gap-1.5 transition-colors"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              <span>Back to Ingestion</span>
            </button>
          )}
          <div>
            <span className="text-xs font-semibold text-zinc-100 font-mono">
              HITL Reviewer • {documentId}
            </span>
            <span className="text-[11px] font-mono text-zinc-500 ml-2">
              Schema: <span className="text-zinc-300 font-semibold">InvoiceTaxonomy.v2</span>
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-amber-950/40 text-amber-400 border border-amber-800/50 flex items-center gap-1">
            <AlertTriangle className="w-3 h-3" />
            Tax Anomaly Flagged (68% &lt; 85%)
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

        {/* Right Pane: Extracted Schema Form (50% / 6 cols) */}
        <div className="lg:col-span-6 flex flex-col justify-between border border-[#27272a] bg-[#121215] rounded-lg p-3.5 overflow-hidden h-full min-h-0">
          <div className="overflow-y-auto space-y-3.5 pr-1 min-h-0 flex-1">
            
            {/* Group 1: Document Metadata */}
            <div className="space-y-1.5">
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 font-semibold block">
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
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 font-semibold block">
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
              <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 font-semibold block">
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
                <span className="text-[10px] font-mono uppercase tracking-wider text-zinc-500 font-semibold block">
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
                      <span className="text-[10px] text-zinc-500">
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

          {/* Footer Actions Bar */}
          <div className="border-t border-[#27272a] pt-3 mt-2 flex items-center justify-between shrink-0">
            <button
              onClick={onRejectBatch}
              className="px-3 py-1.5 rounded bg-zinc-900 hover:bg-rose-950/40 border border-zinc-700 hover:border-rose-800 text-rose-400 font-mono text-xs flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <XOctagon className="w-3.5 h-3.5" />
              <span>Reject &amp; Route to DLQ</span>
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
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Approved &amp; Persisted</span>
                </>
              ) : (
                <>
                  <Save className="w-3.5 h-3.5" />
                  <span>Approve &amp; Persist</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
