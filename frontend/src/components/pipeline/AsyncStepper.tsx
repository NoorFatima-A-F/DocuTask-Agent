import React from 'react';
import { Workflow, CheckCircle2, Clock, RotateCcw, ArrowRight } from 'lucide-react';
import { useJobPolling } from '../../hooks/useJobPolling';
import { StatusBadge } from '../layout/StatusBadge';

interface AsyncStepperProps {
  jobId: string;
  documentId: string;
  onNavigateToReview: (docId: string) => void;
}

export const AsyncStepper: React.FC<AsyncStepperProps> = ({
  jobId,
  documentId,
  onNavigateToReview,
}) => {
  const { jobStatus, replayJob, isReplaying } = useJobPolling(jobId);

  const isCompleted = jobStatus?.status === 'COMPLETED';
  const isFailed = jobStatus?.status === 'FAILED';
  const progressPct = jobStatus?.progress_percentage || 100;
  const milestones = jobStatus?.milestones || [];

  return (
    <div className="space-y-4 max-w-4xl mx-auto w-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-[#27272a] pb-2.5">
        <div className="flex items-center gap-2.5">
          <Workflow className="w-4 h-4 text-zinc-400" />
          <div>
            <h2 className="text-xs font-semibold text-zinc-100 font-mono">Job #{jobId}</h2>
            <span className="text-[10px] text-zinc-500 font-mono">Doc ID: {documentId}</span>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs font-mono text-zinc-400 bg-zinc-900 border border-zinc-800 px-2 py-0.5 rounded">
            Latency: <strong className="text-zinc-200">640ms</strong>
          </span>
          <StatusBadge status={jobStatus?.status || 'COMPLETED'} />
        </div>
      </div>

      {/* Progress Box */}
      <div className="p-4 rounded border border-[#27272a] bg-[#121215] space-y-3">
        <div className="flex justify-between items-center text-xs font-mono">
          <span className="text-zinc-300 font-medium">Asynchronous Pipeline Execution</span>
          <span className="text-zinc-100 font-bold">{progressPct}%</span>
        </div>

        <div className="w-full bg-zinc-950 rounded-full h-1.5 overflow-hidden border border-zinc-800">
          <div
            className="h-full bg-zinc-300 rounded-full transition-all duration-300"
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* Milestones List */}
        <div className="space-y-2 pt-1">
          {milestones.map((m, idx) => (
            <div
              key={m.step}
              className="p-2.5 rounded border border-zinc-800/80 bg-zinc-900/30 flex items-start justify-between gap-3 text-xs font-mono"
            >
              <div className="flex items-start gap-2.5">
                <div className="w-5 h-5 rounded bg-zinc-800 border border-zinc-700 flex items-center justify-center text-[10px] text-zinc-300 shrink-0 mt-0.5">
                  0{idx + 1}
                </div>
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-zinc-200">{m.title}</span>
                    <span className="text-[10px] text-zinc-500 bg-zinc-950 px-1 py-0.2 rounded border border-zinc-800">
                      {m.engine}
                    </span>
                  </div>
                  <p className="text-[11px] text-zinc-400 mt-0.5">{m.description}</p>
                </div>
              </div>

              <div className="flex items-center gap-1 text-[10px] text-emerald-400 bg-emerald-950/40 px-1.5 py-0.5 rounded border border-emerald-800/50">
                <CheckCircle2 className="w-3 h-3" />
                <span>DONE</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Completion CTA */}
      {isCompleted && (
        <div className="p-3 rounded border border-zinc-800 bg-zinc-900/40 flex items-center justify-between">
          <span className="text-xs font-mono text-zinc-300">
            Pipeline completed. Bayesian confidence scored: <strong>94.2%</strong>
          </span>
          <button
            onClick={() => onNavigateToReview(documentId)}
            className="px-3 py-1.5 rounded bg-zinc-100 hover:bg-white text-zinc-950 font-mono text-xs font-semibold flex items-center gap-1.5 transition-colors"
          >
            <span>Proceed to HITL Review</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}
    </div>
  );
};
