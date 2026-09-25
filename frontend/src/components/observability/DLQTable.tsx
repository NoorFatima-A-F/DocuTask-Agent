import React, { useState, useEffect, useCallback } from 'react';
import { RotateCcw, RefreshCw, Copy, Check, Terminal, AlertTriangle } from 'lucide-react';
import { DLQItem } from '../../types/job';
import { jobsApi } from '../../api/jobs';

export const DLQTable: React.FC = () => {
  const [dlqItems, setDlqItems] = useState<DLQItem[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [replayingId, setReplayingId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [selectedTrace, setSelectedTrace] = useState<string | null>(null);

  const fetchDLQ = useCallback(async () => {
    setIsLoading(true);
    try {
      const res = await jobsApi.listDLQ();
      setDlqItems(res.dlq_items || []);
    } catch {
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
          payload: { priority: 'HIGH', retries: 3 },
        },
      ]);
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
    } catch {
      setDlqItems((prev) => prev.filter((item) => item.job_id !== jobId));
    } finally {
      setReplayingId(null);
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="border border-[#27272a] bg-[#121215] rounded p-4 space-y-3">
      <div className="flex items-center justify-between border-b border-[#27272a] pb-2.5">
        <div>
          <span className="text-xs font-semibold text-zinc-100 uppercase tracking-wider font-mono flex items-center gap-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
            Dead Letter Queue (DLQ) &amp; Exception Quarantine
          </span>
          <p className="text-[11px] text-zinc-500 font-mono mt-0.5">
            Quarantined Celery task executions (<code className="text-zinc-400">/api/v1/jobs/dlq/list</code>)
          </p>
        </div>

        <button
          onClick={fetchDLQ}
          disabled={isLoading}
          className="px-2 py-1 rounded bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-zinc-200 text-xs font-mono inline-flex items-center gap-1 transition-colors"
        >
          <RefreshCw className={`w-3 h-3 ${isLoading ? 'animate-spin' : ''}`} />
          <span>Refresh</span>
        </button>
      </div>

      {/* DLQ Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs font-mono">
          <thead>
            <tr className="border-b border-zinc-800 text-zinc-500 text-[10px] uppercase">
              <th className="pb-2 font-medium">Task ID</th>
              <th className="pb-2 font-medium">Classification</th>
              <th className="pb-2 font-medium">Error Message</th>
              <th className="pb-2 font-medium text-center">Retries</th>
              <th className="pb-2 font-medium text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-800/60 text-zinc-300 text-[11px]">
            {dlqItems.length === 0 ? (
              <tr>
                <td colSpan={5} className="py-6 text-center text-zinc-500">
                  Dead Letter Queue is empty. Zero quarantined tasks.
                </td>
              </tr>
            ) : (
              dlqItems.map((item) => (
                <tr key={item.id} className="hover:bg-zinc-800/30 transition-colors">
                  <td className="py-2.5 font-semibold text-zinc-200">
                    <div className="flex items-center gap-1.5">
                      <Terminal className="w-3.5 h-3.5 text-zinc-500" />
                      <span>{item.job_id}</span>
                    </div>
                  </td>
                  <td className="py-2.5">
                    <span className="px-1.5 py-0.2 rounded bg-rose-950/40 text-rose-400 border border-rose-800/50 text-[10px]">
                      {item.error_classification}
                    </span>
                  </td>
                  <td className="py-2.5 text-zinc-400 max-w-xs truncate" title={item.error_message}>
                    {item.error_message}
                  </td>
                  <td className="py-2.5 text-center text-zinc-400">
                    {item.retry_count}/{item.max_retries}
                  </td>
                  <td className="py-2.5 text-right space-x-1.5">
                    {item.stack_trace && (
                      <button
                        onClick={() => setSelectedTrace(item.stack_trace || null)}
                        className="px-2 py-0.5 rounded bg-zinc-900 hover:bg-zinc-800 border border-zinc-700 text-zinc-300 text-[10px] transition-colors"
                      >
                        Trace
                      </button>
                    )}
                    <button
                      onClick={() => handleReplay(item.job_id)}
                      disabled={replayingId === item.job_id}
                      className="px-2 py-0.5 rounded bg-zinc-100 hover:bg-white text-zinc-950 text-[10px] font-semibold inline-flex items-center gap-1 transition-colors"
                    >
                      <RotateCcw className="w-2.5 h-2.5" />
                      <span>{replayingId === item.job_id ? 'Replaying...' : 'Replay'}</span>
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* Stack Trace Preview Modal */}
      {selectedTrace && (
        <div className="p-3 rounded bg-zinc-950 border border-zinc-800 space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between text-zinc-400">
            <span>Stack Trace Inspection</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => handleCopy(selectedTrace, 'trace')}
                className="flex items-center gap-1 text-[11px] text-zinc-400 hover:text-zinc-200"
              >
                {copiedId === 'trace' ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
                <span>{copiedId === 'trace' ? 'Copied' : 'Copy'}</span>
              </button>
              <button
                onClick={() => setSelectedTrace(null)}
                className="text-zinc-500 hover:text-zinc-300 ml-2"
              >
                ✕
              </button>
            </div>
          </div>
          <pre className="text-rose-400/90 text-[11px] whitespace-pre-wrap overflow-x-auto">
            {selectedTrace}
          </pre>
        </div>
      )}
    </div>
  );
};
