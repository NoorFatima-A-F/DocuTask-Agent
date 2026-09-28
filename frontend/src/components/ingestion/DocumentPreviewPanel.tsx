import { FileSearch, X, Layers, Eye } from 'lucide-react';
import { IngestionTask } from '../../pages/IngestionStudio';

interface DocumentPreviewPanelProps {
  selectedTask: IngestionTask | null;
  onClose: () => void;
  onNavigateToReview?: (documentId: string) => void;
}

export function DocumentPreviewPanel({ selectedTask, onClose, onNavigateToReview }: DocumentPreviewPanelProps) {
  if (!selectedTask) {
    return (
      <div className="flex h-full min-h-[440px] flex-col items-center justify-center rounded-xl border border-dashed border-zinc-800 bg-zinc-900/20 p-8 text-center">
        <div className="mb-3 rounded-full border border-zinc-800 bg-zinc-900/80 p-3.5 text-zinc-500 shadow-inner">
          <FileSearch className="h-6 w-6 stroke-[1.5]" />
        </div>
        <h3 className="text-sm font-semibold text-zinc-200">No Document Selected</h3>
        <p className="mt-1.5 max-w-sm text-xs leading-relaxed text-zinc-400 font-sans">
          Drop a document on the left to initiate ingestion, or click <span className="text-zinc-200 font-medium">Inspect</span> on any task in the stream below to review bounding boxes and field validation layers.
        </p>
      </div>
    );
  }

  return (
    <div className="flex flex-col h-full rounded-xl border border-zinc-800 bg-zinc-900/60 shadow-sm backdrop-blur-sm overflow-hidden">
      {/* Inspector Header */}
      <div className="flex items-center justify-between px-5 py-3 border-b border-zinc-800 bg-zinc-950/50">
        <div className="flex items-center gap-2.5">
          <Layers className="h-4 w-4 text-indigo-400" />
          <div>
            <h3 className="text-xs font-semibold text-zinc-200 font-mono">{selectedTask.documentName}</h3>
            <p className="text-[10px] text-zinc-400">
              Schema: {selectedTask.schema} ({selectedTask.schemaBadge}) • Task ID: {selectedTask.id}
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

      {/* Inspector Workspace */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-5 flex-1 overflow-y-auto">
        {/* Visual Document Bounding Box Mock */}
        <div className="relative rounded-lg border border-zinc-800 bg-zinc-950 p-4 min-h-[280px] flex flex-col justify-between overflow-hidden">
          <div className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest pb-2 border-b border-zinc-900">
            OCR Coordinate Canvas
          </div>
          
          <div className="space-y-3 my-auto">
            <div className="relative rounded border border-emerald-500/40 bg-emerald-500/10 p-2 text-xs">
              <span className="absolute -top-2 left-2 bg-emerald-500 text-zinc-950 text-[9px] font-bold px-1 rounded uppercase">
                Header
              </span>
              <p className="font-mono text-zinc-200 mt-1">{selectedTask.documentName}</p>
            </div>

            <div className={`relative rounded border p-2 text-xs ${
              selectedTask.status === 'Tax Discrepancy'
                ? 'border-amber-500/60 bg-amber-500/10'
                : 'border-emerald-500/40 bg-emerald-500/10'
            }`}>
              <span className={`absolute -top-2 left-2 text-zinc-950 text-[9px] font-bold px-1 rounded uppercase ${
                selectedTask.status === 'Tax Discrepancy' ? 'bg-amber-400' : 'bg-emerald-500'
              }`}>
                {selectedTask.status === 'Tax Discrepancy' ? 'Anomaly' : 'Validated Field'}
              </span>
              <p className="font-mono text-zinc-200 mt-1">
                {selectedTask.statusDetails || 'Field verified against ground truth.'}
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between text-[10px] font-mono text-zinc-400 pt-2 border-t border-zinc-900">
            <span>Latency: {selectedTask.latencyMs}ms</span>
            <span>Priority: {selectedTask.priority}</span>
          </div>
        </div>

        {/* Extracted Key-Value Hierarchy */}
        <div className="flex flex-col justify-between rounded-lg border border-zinc-800 bg-zinc-950/40 p-4 space-y-3">
          <div className="space-y-2">
            <div className="text-[10px] font-mono text-zinc-400 uppercase tracking-widest pb-2 border-b border-zinc-800/80">
              Structured Extractions
            </div>
            <div className="flex flex-col gap-2 mt-1 overflow-y-auto max-h-[220px]">
              {selectedTask.extractedFields?.map((item, idx) => (
                <div key={idx} className="flex flex-col gap-0.5 rounded border border-zinc-800/60 bg-zinc-900/40 p-2">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="font-medium text-zinc-400">{item.field}</span>
                    <span className={`font-mono text-[10px] tabular-nums ${item.isAnomaly ? 'text-amber-400' : 'text-emerald-400'}`}>
                      {item.confidence.toFixed(1)}%
                    </span>
                  </div>
                  <span className="text-xs font-mono text-zinc-200">{item.value}</span>
                </div>
              ))}
            </div>
          </div>

          {onNavigateToReview && (
            <div className="pt-2 border-t border-zinc-800 flex justify-end">
              <button
                type="button"
                onClick={() => onNavigateToReview(selectedTask.id)}
                className="inline-flex items-center gap-1.5 rounded-lg bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white hover:bg-indigo-500 transition-colors shadow-sm focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none cursor-pointer"
              >
                <Eye className="w-3.5 h-3.5" />
                <span>Full HITL Canvas</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
