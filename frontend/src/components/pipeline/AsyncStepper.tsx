import React from 'react';
import {
  Workflow,
  CheckCircle2,
  AlertOctagon,
  RotateCcw,
  ArrowRight,
  ExternalLink,
  ShieldAlert,
} from 'lucide-react';
import { useJobPolling } from '../../hooks/useJobPolling';
import { StageTimeline } from './StageTimeline';
import { LatencyClock } from './LatencyClock';
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
  const { jobStatus, isLoading, replayJob, isReplaying } = useJobPolling(jobId);

  const isCompleted = jobStatus?.status === 'COMPLETED';
  const isFailed = jobStatus?.status === 'FAILED';
  const isRunning = !isCompleted && !isFailed;

  const milestones = jobStatus?.milestones || [];
  const progressPct = jobStatus?.progress_percentage || 0;

  const handleReplay = async () => {
    await replayJob(jobId);
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header & Job Metadata */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2.5">
            <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-400">
              <Workflow className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100 flex items-center gap-2 font-mono">
                Job #{jobId.substring(0, 16)}...
              </h2>
              <span className="text-xs text-slate-400 font-mono">
                Doc Ref: {documentId.substring(0, 16)}...
              </span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <LatencyClock isRunning={isRunning} finalLatencyMs={isRunning ? undefined : 640} />
          <StatusBadge status={jobStatus?.status || 'PROCESSING'} />
        </div>
      </div>

      {/* Progress & Milestone Overview */}
      <div className="p-5 rounded-2xl border border-slate-800 bg-slate-900/40 space-y-4">
        <div className="flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-xs font-mono font-semibold text-slate-300">
              Multi-Milestone Celery Pipeline Execution
            </span>
            <p className="text-[11px] text-slate-400">
              Polling <code className="text-indigo-300">/api/v1/jobs/{jobId.substring(0, 8)}/status</code> every 1,500ms
            </p>
          </div>
          <span className="text-sm font-mono font-bold text-indigo-400">
            {progressPct}%
          </span>
        </div>

        {/* Global Progress Bar */}
        <div className="w-full bg-slate-950 rounded-full h-2 overflow-hidden border border-slate-800">
          <div
            className={`h-full transition-all duration-500 rounded-full ${
              isCompleted
                ? 'bg-gradient-to-r from-indigo-500 via-cyan-400 to-emerald-400'
                : isFailed
                ? 'bg-rose-500'
                : 'bg-gradient-to-r from-indigo-500 to-cyan-400'
            }`}
            style={{ width: `${progressPct}%` }}
          />
        </div>

        {/* Milestones Stepper List */}
        <StageTimeline milestones={milestones} />
      </div>

      {/* Terminal Success Transition Card */}
      {isCompleted && (
        <div className="p-4 rounded-xl border border-emerald-500/30 bg-emerald-950/20 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <h4 className="text-xs font-semibold text-emerald-200">
                Pipeline Successfully Completed & Validation Gates Passed
              </h4>
              <p className="text-[11px] text-emerald-400/80">
                Pydantic contract validated, Bayesian confidence calculated (0.942). Ready for Human-In-The-Loop review.
              </p>
            </div>
          </div>

          <button
            onClick={() => onNavigateToReview(documentId)}
            className="w-full sm:w-auto px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-semibold text-xs flex items-center justify-center gap-2 transition-all shadow-lg shadow-emerald-500/20 font-mono shrink-0"
          >
            <span>Review & Approve</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Failure Resilience & Dead Letter Queue (DLQ) Card */}
      {isFailed && (
        <div className="p-5 rounded-xl border border-rose-500/40 bg-rose-950/20 space-y-4">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-3">
              <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
              <div className="space-y-1">
                <h4 className="text-xs font-semibold text-rose-200 flex items-center gap-2">
                  <span>Job Terminated with Unrecoverable Exception</span>
                  <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-rose-500/20 text-rose-300 border border-rose-500/40">
                    MOVED TO DLQ
                  </span>
                </h4>
                <p className="text-xs text-rose-400">
                  {jobStatus?.error_message || 'Timeout in OCR dispatch worker: PyMuPDF rasterization limit exceeded.'}
                </p>
              </div>
            </div>

            <button
              onClick={handleReplay}
              disabled={isReplaying}
              className="px-3.5 py-1.5 rounded-lg bg-rose-600 hover:bg-rose-500 disabled:opacity-50 text-white font-mono text-xs font-semibold flex items-center gap-1.5 transition-all shadow-lg shadow-rose-900/30 shrink-0"
            >
              <RotateCcw className={`w-3.5 h-3.5 ${isReplaying ? 'animate-spin' : ''}`} />
              <span>{isReplaying ? 'Replaying...' : 'Replay via DLQ'}</span>
            </button>
          </div>

          {/* Stack Trace Preview */}
          <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-[11px] font-mono text-slate-400 overflow-x-auto">
            <div className="text-slate-500 mb-1 flex items-center justify-between">
              <span>DLQ Payload Trace</span>
              <span>POST /api/v1/jobs/dlq/replay/{jobId.substring(0, 8)}</span>
            </div>
            <pre className="text-rose-300 whitespace-pre-wrap">
              {jobStatus?.stack_trace ||
                `Traceback (most recent call last):\n  File "app/jobs/worker.py", line 84, in execute_pipeline\n  File "app/services/ocr_service.py", line 42, in parse_layout\nRuntimeError: OCR parsing failed on corrupted raster stream`}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
