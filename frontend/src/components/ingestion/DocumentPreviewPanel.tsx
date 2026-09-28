import { FileSearch, X, Layers, Eye, ShieldCheck, AlertCircle } from 'lucide-react';
import { IngestionTask } from '../../pages/IngestionStudio';

interface DocumentPreviewPanelProps {
  selectedTask: IngestionTask | null;
  onClose: () => void;
  onNavigateToReview?: (documentId: string) => void;
}

export function DocumentPreviewPanel({ selectedTask, onClose, onNavigateToReview }: DocumentPreviewPanelProps) {
  if (!selectedTask) {
    return (
      <div className="flex h-full min-h-[420px] flex-col items-center justify-center rounded-xl border border-dashed border-zinc-800 bg-zinc-900/30 p-8 text-center justify-between">
        <div className="my-auto flex flex-col items-center">
          <div className="mb-3 rounded-full border border-zinc-800 bg-zinc-900/80 p-4 text-zinc-400 shadow-inner">
            <FileSearch className="h-7 w-7 stroke-[1.5] text-indigo-400" />
          </div>
          <h3 className="text-sm font-semibold text-zinc-200 font-sans">No Document Selected</h3>
          <p className="mt-2 max-w-md text-xs leading-relaxed text-zinc-400 font-sans">
            Upload and dispatch a file using the Ingestion Dock on the left, or click <span className="text-zinc-200 font-medium">Inspect</span> on any task in the stream below to review real-time OCR bounding boxes, confidence distributions, and field extractions.
          </p>
        </div>

        <div className="w-full pt-4 border-t border-zinc-800/60 flex items-center justify-between text-[11px] font-mono text-zinc-400">
          <span>Dual-Pane Inspection Studio</span>
          <span>OCR Ground-Truth Layer Active</span>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-zinc-800 bg-zinc-900/70 shadow-sm backdrop-blur-sm overflow-hidden justify-between">
      {/* Inspector Header */}
      <div>
        <div className="flex items-center justify-between px-5 py-3 border-b border-zinc-800 bg-zinc-950/60">
          <div className="flex items-center gap-2.5">
            <Layers className="h-4 w-4 text-indigo-400" />
            <div>
              <h3 className="text-xs font-semibold text-zinc-200 font-mono">{selectedTask.documentName}</h3>
              <p className="text-[10px] text-zinc-400 font-mono">
                Schema: {selectedTask.schema} ({selectedTask.schemaBadge}) • Task: {selectedTask.id}
              </p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <div className="flex items-center gap-1.5 bg-zinc-900 px-2 py-1 rounded border border-zinc-800">
              <span className="text-[10px] text-zinc-400 uppercase font-medium">Score:</span>
              <span className="text-xs font-mono font-bold tabular-nums text-emerald-400">
                {selectedTask.confidence.toFixed(1)}%
              </span>
            </div>
            <button
              onClick={onClose}
              aria-label="Close Inspector"
              className="rounded p-1 text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200 transition-colors cursor-pointer"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Inspector Workspace Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4">
          {/* Visual Document Bounding Box Mock */}
          <div className="relative rounded-lg border border-zinc-800 bg-zinc-950 p-4 min-h-[260px] flex flex-col justify-between overflow-hidden">
            <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 uppercase tracking-widest pb-2 border-b border-zinc-900">
              <span>OCR Coordinate Canvas</span>
              <span className="text-zinc-400">Page 1/1</span>
            </div>
            
            <div className="space-y-2.5 my-auto">
              <div className="relative rounded border border-emerald-500/40 bg-emerald-500/10 p-2.5 text-xs">
                <span className="absolute -top-2 left-2 bg-emerald-500 text-zinc-950 text-[9px] font-bold px-1 rounded uppercase">
                  Header Entity
                </span>
                <p className="font-mono text-zinc-200 mt-1">{selectedTask.documentName}</p>
              </div>

              <div className={`relative rounded border p-2.5 text-xs ${
                selectedTask.status === 'Tax Discrepancy'
                  ? 'border-amber-500/60 bg-amber-500/10'
                  : 'border-emerald-500/40 bg-emerald-500/10'
              }`}>
                <span className={`absolute -top-2 left-2 text-zinc-950 text-[9px] font-bold px-1 rounded uppercase flex items-center gap-1 ${
                  selectedTask.status === 'Tax Discrepancy' ? 'bg-amber-400' : 'bg-emerald-500'
                }`}>
                  {selectedTask.status === 'Tax Discrepancy' ? <AlertCircle className="w-2.5 h-2.5" /> : <ShieldCheck className="w-2.5 h-2.5" />}
                  {selectedTask.status === 'Tax Discrepancy' ? 'Anomaly Flagged' : 'Field Validated'}
                </span>
                <p className="font-mono text-zinc-200 mt-1 text-[11px]">
                  {selectedTask.statusDetails || 'Field verified against ground truth invariants.'}
                </p>
              </div>
            </div>

            <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 pt-2 border-t border-zinc-900">
              <span>Latency: {selectedTask.latencyMs}ms</span>
              <span>Priority: {selectedTask.priority}</span>
            </div>
          </div>

          {/* Extracted Key-Value Hierarchy */}
          <div className="flex flex-col justify-between rounded-lg border border-zinc-800 bg-zinc-950/50 p-4 space-y-3">
            <div className="space-y-2">
              <div className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest pb-2 border-b border-zinc-800/80">
                Structured Extractions
              </div>
              <div className="flex flex-col gap-2 mt-1 overflow-y-auto max-h-[190px] pr-1">
                {selectedTask.extractedFields?.map((item, idx) => (
                  <div key={idx} className="flex flex-col gap-0.5 rounded border border-zinc-800/60 bg-zinc-900/50 p-2">
                    <div className="flex items-center justify-between text-[11px]">
                      <span className="font-medium text-zinc-400">{item.field}</span>
                      <span className={`font-mono text-[10px] tabular-nums font-semibold ${item.isAnomaly ? 'text-amber-400' : 'text-emerald-400'}`}>
                        {item.confidence.toFixed(1)}%
                      </span>
                    </div>
                    <span className="text-xs font-mono text-zinc-200">{item.value}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Footer Navigation CTA */}
      {onNavigateToReview && (
        <div className="px-5 py-3 border-t border-zinc-800 bg-zinc-950/40 flex items-center justify-between">
          <span className="text-[11px] font-mono text-zinc-400">
            Audit trail &amp; operator sign-off available in full canvas
          </span>
          <button
            type="button"
            onClick={() => onNavigateToReview(selectedTask.id)}
            className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3.5 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors shadow-sm focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none cursor-pointer"
          >
            <Eye className="w-3.5 h-3.5" />
            <span>Full HITL Canvas</span>
          </button>
        </div>
      )}
    </div>
  );
}
