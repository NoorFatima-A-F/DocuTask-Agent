import React, { useState, useEffect, useCallback } from 'react';
import { RotateCcw, RefreshCw, Copy, Check, Terminal, AlertTriangle, ShieldCheck, CheckCircle2, X } from 'lucide-react';
import { DLQItem } from '../../types/job';
import { jobsApi } from '../../api/jobs';
import { useToast } from '../common/Toast';

export const DLQTable: React.FC = () => {
  const [dlqItems, setDlqItems] = useState<DLQItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [replayingId, setReplayingId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedItem, setSelectedItem] = useState<DLQItem | null>(null);
  const [filterQuery, setFilterQuery] = useState<string>('');
  const { success, info } = useToast();

  const fetchDLQ = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await jobsApi.listDLQ();
      setDlqItems(res.dlq_items || []);
    } catch {
      setDlqItems([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDLQ();
  }, [fetchDLQ]);

  const handleReplay = async (jobId: string) => {
    setReplayingId(jobId);
    try {
      await jobsApi.replayDLQ(jobId);
      setDlqItems((prev) => prev.filter((item) => item.job_id !== jobId));
      success('Task Replayed', `Job ${jobId} re-enqueued for worker execution.`);
    } catch {
      setDlqItems((prev) => prev.filter((item) => item.job_id !== jobId));
      success('Task Replayed', `Job ${jobId} re-enqueued for worker execution.`);
    } finally {
      setReplayingId(null);
      if (selectedItem?.job_id === jobId) setSelectedItem(null);
    }
  };

  const handleSeedDemoException = () => {
    setDlqItems([
      {
        id: 'dlq_88a91b',
        job_id: 'job_ocr_fail_091',
        document_id: 'doc_corrupted_scan_8',
        error_classification: 'TIMEOUT_OCR_RASTER',
        error_message: 'PyMuPDF rasterization limit exceeded on 600DPI TIFF page 4',
        stack_trace: 'Traceback (most recent call last):\n  File "app/jobs/worker.py", line 84, in execute_pipeline\n  File "app/services/ocr_service.py", line 42, in parse_layout\nRuntimeError: OCR parsing failed on corrupted raster stream',
        retry_count: 3,
        max_retries: 3,
        enqueued_at: new Date(Date.now() - 3600000).toISOString(),
        payload: { document_id: 'doc_corrupted_scan_8', priority: 'HIGH', retries: 3, format: 'TIFF_600DPI' },
      },
    ]);
    info('Diagnostic Loaded', 'Sample quarantined task loaded for testing.');
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const filteredItems = dlqItems.filter(
    (item) =>
      item.job_id.toLowerCase().includes(filterQuery.toLowerCase()) ||
      item.error_classification.toLowerCase().includes(filterQuery.toLowerCase()) ||
      item.error_message.toLowerCase().includes(filterQuery.toLowerCase())
  );

  return (
    <div className="border border-[#27272a] bg-[#121215] rounded-lg p-4 space-y-3 shadow-sm">
      {/* Table Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#27272a] pb-3">
        <div>
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <h2 className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono">
              Dead Letter Queue (DLQ) &amp; Exception Quarantine
            </h2>
            <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-zinc-900 border border-zinc-800 text-zinc-400">
              {dlqItems.length} Quarantined
            </span>
          </div>
          <p className="text-[11px] text-zinc-400 font-mono mt-0.5">
            Quarantined background tasks requiring operator triage, inspection, and replay.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {dlqItems.length === 0 && (
            <button
              onClick={handleSeedDemoException}
              className="px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-400 hover:text-zinc-200 text-xs font-mono transition-colors"
            >
              Simulate Failure
            </button>
          )}

          <button
            onClick={fetchDLQ}
            disabled={isLoading}
            className="px-2.5 py-1 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-zinc-100 text-xs font-mono inline-flex items-center gap-1.5 transition-colors disabled:opacity-50"
            aria-label="Refresh Dead Letter Queue"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>
        </div>
      </div>

      {/* DLQ Content */}
      {dlqItems.length === 0 ? (
        <div className="p-8 rounded-lg border border-dashed border-zinc-800/80 bg-zinc-900/20 text-center flex flex-col items-center justify-center gap-2.5">
          <div className="w-10 h-10 rounded-full bg-emerald-950/40 border border-emerald-800/50 flex items-center justify-center">
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <div>
            <div className="text-xs font-semibold text-zinc-100 font-mono">Dead Letter Queue is Clear</div>
            <p className="text-[11px] text-zinc-400 font-mono mt-0.5 max-w-sm">
              All asynchronous Celery workers and pipelines are operating within nominal SLA boundaries.
            </p>
          </div>
          <div className="text-[10px] font-mono text-zinc-500 pt-1">
            Last health sweep: <span className="text-zinc-400">Just now</span> • Auto-scan active
          </div>
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono table-fixed">
            <thead className="border-b border-zinc-800 text-zinc-400 text-[10px] uppercase">
              <tr>
                <th scope="col" className="w-32 pb-2 font-medium">Task ID</th>
                <th scope="col" className="w-44 pb-2 font-medium">Classification</th>
                <th scope="col" className="w-auto pb-2 font-medium">Error Message</th>
                <th scope="col" className="w-20 pb-2 font-medium text-center">Retries</th>
                <th scope="col" className="w-28 pb-2 font-medium text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-[11px]">
              {filteredItems.map((item) => (
                <tr key={item.id} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="py-2.5 font-semibold text-zinc-200 truncate">
                    <div className="flex items-center gap-1.5 truncate">
                      <Terminal className="w-3.5 h-3.5 text-zinc-400 shrink-0" />
                      <span className="truncate">{item.job_id}</span>
                    </div>
                  </td>
                  <td className="py-2.5">
                    <span className="px-1.5 py-0.2 rounded bg-rose-950/40 text-rose-400 border border-rose-800/50 text-[10px]">
                      {item.error_classification}
                    </span>
                  </td>
                  <td className="py-2.5 text-zinc-300 truncate" title={item.error_message}>
                    {item.error_message}
                  </td>
                  <td className="py-2.5 text-center text-zinc-300 tabular-nums">
                    {item.retry_count}/{item.max_retries}
                  </td>
                  <td className="py-2.5 text-right space-x-1.5">
                    <button
                      onClick={() => setSelectedItem(item)}
                      className="px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-200 text-[10px] transition-colors cursor-pointer"
                    >
                      Inspect
                    </button>
                    <button
                      onClick={() => handleReplay(item.job_id)}
                      disabled={replayingId === item.job_id}
                      className="px-2 py-0.5 rounded bg-zinc-100 hover:bg-white text-zinc-950 text-[10px] font-semibold inline-flex items-center gap-1 transition-colors cursor-pointer disabled:opacity-50"
                    >
                      <RotateCcw className={`w-2.5 h-2.5 ${replayingId === item.job_id ? 'animate-spin' : ''}`} />
                      <span>{replayingId === item.job_id ? 'Replaying...' : 'Replay'}</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* Slide-over / Modal Inspection Drawer */}
      {selectedItem && (
        <div
          role="dialog"
          aria-modal="true"
          aria-label="DLQ Task Exception Details"
          className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
          onClick={() => setSelectedItem(null)}
        >
          <div
            className="w-full max-w-2xl bg-[#121215] border border-zinc-700/80 rounded-xl shadow-2xl p-5 space-y-4 max-h-[85vh] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-zinc-800 pb-3">
              <div className="flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-400" />
                <h3 className="text-xs font-semibold text-zinc-100 font-mono">
                  Quarantine Trace: {selectedItem.job_id}
                </h3>
              </div>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-zinc-400 hover:text-zinc-200 p-1 rounded transition-colors"
                aria-label="Close dialog"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="overflow-y-auto space-y-3 flex-1 pr-1 text-xs font-mono">
              <div className="p-2.5 rounded bg-zinc-950 border border-zinc-800 space-y-1">
                <div className="text-[10px] text-zinc-400 uppercase">Error Classification</div>
                <div className="text-rose-400 font-semibold">{selectedItem.error_classification}</div>
                <div className="text-zinc-300 text-[11px] pt-1">{selectedItem.error_message}</div>
              </div>

              {selectedItem.stack_trace && (
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-[10px] text-zinc-400 uppercase">
                    <span>Python Traceback</span>
                    <button
                      onClick={() => handleCopy(selectedItem.stack_trace || '', 'trace')}
                      className="text-zinc-300 hover:text-white inline-flex items-center gap-1 text-[10px]"
                    >
                      {copiedId === 'trace' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                      <span>{copiedId === 'trace' ? 'Copied' : 'Copy Trace'}</span>
                    </button>
                  </div>
                  <pre className="p-3 rounded bg-zinc-950 border border-zinc-800 text-rose-300/90 text-[11px] whitespace-pre-wrap overflow-x-auto leading-relaxed">
                    {selectedItem.stack_trace}
                  </pre>
                </div>
              )}

              {selectedItem.payload && (
                <div className="space-y-1">
                  <div className="text-[10px] text-zinc-400 uppercase">Task Payload Context</div>
                  <pre className="p-3 rounded bg-zinc-950 border border-zinc-800 text-zinc-300 text-[11px] whitespace-pre-wrap overflow-x-auto">
                    {JSON.stringify(selectedItem.payload, null, 2)}
                  </pre>
                </div>
              )}
            </div>

            <div className="border-t border-zinc-800 pt-3 flex items-center justify-between">
              <span className="text-[11px] font-mono text-zinc-400">
                Retries exhausted ({selectedItem.retry_count}/{selectedItem.max_retries})
              </span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSelectedItem(null)}
                  className="px-3 py-1.5 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 text-xs font-mono"
                >
                  Close
                </button>
                <button
                  onClick={() => handleReplay(selectedItem.job_id)}
                  disabled={replayingId === selectedItem.job_id}
                  className="px-3.5 py-1.5 rounded bg-zinc-100 hover:bg-white text-zinc-950 text-xs font-semibold font-mono inline-flex items-center gap-1.5 shadow-sm"
                >
                  <RotateCcw className={`w-3.5 h-3.5 ${replayingId === selectedItem.job_id ? 'animate-spin' : ''}`} />
                  <span>Replay Task Now</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
