import React, { useState } from 'react';
import { Search, FileText, CheckCircle2, AlertTriangle, X, Eye, ExternalLink, ShieldCheck } from 'lucide-react';
import { IngestionQueueRow, SCHEMA_CONFIG } from './IngestionDock';

export interface DocumentPreviewPanelProps {
  selectedTask: IngestionQueueRow | null;
  onClearSelection: () => void;
  onNavigateToReview?: (documentId: string) => void;
}

export const DocumentPreviewPanel: React.FC<DocumentPreviewPanelProps> = ({
  selectedTask,
  onClearSelection,
  onNavigateToReview,
}) => {
  const [hoveredField, setHoveredField] = useState<string | null>(null);

  if (!selectedTask) {
    return (
      <div className="flex h-full min-h-[460px] flex-col items-center justify-center rounded-xl border border-dashed border-zinc-800 bg-zinc-900/20 p-8 text-center">
        <div className="mb-3 rounded-full border border-zinc-800 bg-zinc-900/80 p-3.5 text-zinc-500 shadow-inner">
          <Search className="h-6 w-6 stroke-[1.5]" />
        </div>
        <h3 className="text-sm font-semibold text-zinc-200">No Document Selected</h3>
        <p className="mt-1.5 max-w-sm text-xs leading-relaxed text-zinc-500 font-sans">
          Drop a document on the left to initiate ingestion, or click{' '}
          <span className="text-zinc-400 font-medium">Inspect</span> on any task in the stream below to review bounding boxes and field validation layers.
        </p>
      </div>
    );
  }

  const sampleFields = [
    { key: 'invoice_num', label: 'Invoice #', value: selectedTask.filename.replace('.pdf', ''), confidence: 0.98, box: { top: '8%', left: '60%', width: '32%', height: '8%' } },
    { key: 'vendor_name', label: 'Vendor Name', value: 'ACME CLOUD CORP', confidence: 0.96, box: { top: '6%', left: '6%', width: '42%', height: '10%' } },
    { key: 'issue_date', label: 'Issue Date', value: '2026-09-24', confidence: 0.94, box: { top: '22%', left: '55%', width: '38%', height: '6%' } },
    { key: 'subtotal', label: 'Subtotal Amount', value: '$10,550.00', confidence: 0.97, box: { top: '74%', left: '58%', width: '35%', height: '6%' } },
    { key: 'tax_amount', label: 'Tax Amount', value: '$870.38', confidence: 0.68, isWarning: true, box: { top: '81%', left: '58%', width: '35%', height: '6%' } },
    { key: 'total_amount', label: 'Total Amount', value: '$11,420.38', confidence: 0.99, box: { top: '88%', left: '58%', width: '35%', height: '8%' } },
  ];

  return (
    <div className="flex h-full min-h-[460px] flex-col justify-between rounded-xl border border-zinc-800 bg-zinc-900/60 p-5 shadow-sm space-y-4">
      {/* Header Info */}
      <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
        <div className="flex items-center gap-2.5 min-w-0">
          <div className="w-7 h-7 rounded-lg bg-zinc-800 border border-zinc-700 flex items-center justify-center shrink-0">
            <FileText className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="min-w-0">
            <div className="flex items-center gap-2">
              <h3 className="text-xs font-semibold text-zinc-100 truncate font-mono">
                {selectedTask.filename}
              </h3>
              <span className="rounded bg-zinc-800 px-1.5 py-0.2 text-[10px] font-mono text-zinc-400 border border-zinc-700/60">
                {SCHEMA_CONFIG[selectedTask.schemaType]?.badge || 'v2.1'}
              </span>
            </div>
            <p className="text-[11px] text-zinc-400 font-sans">
              Task ID: <span className="font-mono text-zinc-300">{selectedTask.taskId}</span> • Latency: <span className="font-mono tabular-nums text-zinc-300">{selectedTask.latencyMs}ms</span>
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span
            className={`inline-flex items-center gap-1 font-mono text-xs px-2.5 py-0.5 rounded-full border tabular-nums ${
              selectedTask.confidence >= 90
                ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-400 border-amber-500/20'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            {selectedTask.confidence.toFixed(1)}% Confidence
          </span>

          <button
            type="button"
            onClick={onClearSelection}
            className="p-1.5 rounded-lg text-zinc-400 hover:text-zinc-100 hover:bg-zinc-800 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
            aria-label="Close Inspection"
            title="Close Inspection"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Populated Body: Simulated Canvas (Left) + Key-Value Extractions (Right) */}
      <div className="grid grid-cols-1 md:grid-cols-12 gap-4 flex-1 min-h-[300px]">
        {/* Left: Document OCR Canvas Preview */}
        <div className="md:col-span-6 rounded-lg border border-zinc-800 bg-zinc-950 p-3 flex items-center justify-center relative overflow-hidden">
          <div className="relative bg-white text-zinc-900 rounded p-4 shadow-md w-full max-w-[280px] h-[300px] text-[8px] font-mono leading-tight select-none">
            <div className="border-b border-zinc-200 pb-1 flex justify-between">
              <span className="font-bold text-zinc-800">ACME CLOUD CORP</span>
              <span className="font-bold text-zinc-700">INVOICE</span>
            </div>
            <div className="py-2 text-[7px] text-zinc-600 space-y-0.5">
              <div>Billed to: Enterprise Dynamics Inc.</div>
              <div>Issue Date: 2026-09-24</div>
            </div>
            <div className="border-t border-b border-zinc-200 py-1 my-2 text-[7px]">
              <div className="flex justify-between"><span>GPU Cluster x2</span><span>$8,500.00</span></div>
              <div className="flex justify-between"><span>DirectConnect 10G</span><span>$2,050.00</span></div>
            </div>
            <div className="absolute bottom-4 right-4 text-right text-[7px] space-y-0.5">
              <div>Subtotal: $10,550.00</div>
              <div className="text-amber-700 font-bold">Tax: $870.38</div>
              <div className="font-bold text-zinc-900 border-t border-zinc-300 pt-0.5">Total: $11,420.38</div>
            </div>

            {/* Bounding Box Overlays */}
            {sampleFields.map((f) => {
              const isHovered = hoveredField === f.key;
              return (
                <div
                  key={f.key}
                  onMouseEnter={() => setHoveredField(f.key)}
                  onMouseLeave={() => setHoveredField(null)}
                  style={{
                    position: 'absolute',
                    top: f.box.top,
                    left: f.box.left,
                    width: f.box.width,
                    height: f.box.height,
                  }}
                  className={`border-2 rounded transition-all cursor-pointer ${
                    f.isWarning
                      ? 'border-amber-500 bg-amber-500/15'
                      : 'border-emerald-500 bg-emerald-500/10'
                  } ${isHovered ? 'ring-2 ring-indigo-600 z-20' : ''}`}
                >
                  <span
                    className={`absolute -top-2.5 left-0 px-1 py-0.2 rounded text-[6px] font-bold text-white ${
                      f.isWarning ? 'bg-amber-600' : 'bg-emerald-600'
                    }`}
                  >
                    {f.label}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Right: Field Key-Value Summary */}
        <div className="md:col-span-6 flex flex-col justify-between space-y-2">
          <div className="space-y-1.5 overflow-y-auto max-h-[280px] pr-1">
            <span className="text-[10px] uppercase font-mono tracking-wider text-zinc-400 font-semibold block">
              Extracted Entities &amp; Proof Gates
            </span>
            {sampleFields.map((f) => (
              <div
                key={f.key}
                onMouseEnter={() => setHoveredField(f.key)}
                onMouseLeave={() => setHoveredField(null)}
                className={`p-2 rounded-lg border text-xs transition-colors flex items-center justify-between ${
                  hoveredField === f.key
                    ? 'border-indigo-500/80 bg-zinc-800/80'
                    : 'border-zinc-800 bg-zinc-900/40 hover:bg-zinc-800/40'
                }`}
              >
                <div>
                  <span className="text-[10px] text-zinc-400 block font-mono">{f.label}</span>
                  <span className="text-zinc-100 font-medium">{f.value}</span>
                </div>
                <div className="text-right">
                  <span
                    className={`text-[10px] font-mono tabular-nums font-semibold ${
                      f.isWarning ? 'text-amber-400' : 'text-emerald-400'
                    }`}
                  >
                    {(f.confidence * 100).toFixed(0)}%
                  </span>
                  {f.isWarning && (
                    <span className="text-[9px] text-amber-400 block">Variance flag</span>
                  )}
                </div>
              </div>
            ))}
          </div>

          <div className="pt-2 border-t border-zinc-800/80 flex items-center justify-between">
            <button
              type="button"
              onClick={onClearSelection}
              className="px-3 py-1.5 rounded-lg border border-zinc-800 bg-zinc-900 text-xs text-zinc-400 hover:text-zinc-200 transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
            >
              Close Inspection
            </button>
            {onNavigateToReview && (
              <button
                type="button"
                onClick={() => onNavigateToReview(selectedTask.documentId)}
                className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors shadow-sm focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Full HITL Canvas</span>
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
