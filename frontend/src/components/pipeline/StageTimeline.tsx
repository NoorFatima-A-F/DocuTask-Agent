import React from 'react';
import {
  CheckCircle2,
  Loader2,
  Clock,
  AlertTriangle,
  FileCheck,
  ScanLine,
  TableProperties,
  Sparkles,
  ShieldCheck,
} from 'lucide-react';
import { MilestoneProgress, PipelineMilestone } from '../../types/job';

interface StageTimelineProps {
  milestones: MilestoneProgress[];
}

const MILESTONE_ICONS: Record<PipelineMilestone, React.ComponentType<{ className?: string }>> = {
  FILE_INGESTED: FileCheck,
  OCR_DISPATCH: ScanLine,
  SCHEMA_MAPPING: TableProperties,
  LLM_EXTRACTION: Sparkles,
  QUALITY_AUDIT: ShieldCheck,
};

export const StageTimeline: React.FC<StageTimelineProps> = ({ milestones }) => {
  return (
    <div className="space-y-3">
      {milestones.map((milestone, idx) => {
        const Icon = MILESTONE_ICONS[milestone.step] || FileCheck;
        const isCompleted = milestone.status === 'COMPLETED';
        const isRunning = milestone.status === 'RUNNING';
        const isFailed = milestone.status === 'FAILED';
        const isPending = milestone.status === 'PENDING';

        return (
          <div
            key={milestone.step}
            className={`p-4 rounded-xl border transition-all flex items-start justify-between gap-4 ${
              isRunning
                ? 'bg-indigo-950/20 border-indigo-500/40 shadow-sm shadow-indigo-500/10'
                : isCompleted
                ? 'bg-slate-900/40 border-slate-800/80 hover:border-slate-700'
                : isFailed
                ? 'bg-rose-950/20 border-rose-500/40'
                : 'bg-slate-950/30 border-slate-900 opacity-60'
            }`}
          >
            <div className="flex items-start gap-3.5">
              {/* Step Number & Icon */}
              <div
                className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 border ${
                  isCompleted
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                    : isRunning
                    ? 'bg-indigo-500/20 border-indigo-500/50 text-indigo-300'
                    : isFailed
                    ? 'bg-rose-500/20 border-rose-500/50 text-rose-300'
                    : 'bg-slate-900 border-slate-800 text-slate-500'
                }`}
              >
                <Icon className="w-4 h-4" />
              </div>

              {/* Title & Description */}
              <div className="space-y-0.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-slate-400 font-bold">
                    0{idx + 1}.
                  </span>
                  <h4
                    className={`text-xs font-semibold ${
                      isRunning
                        ? 'text-indigo-200'
                        : isCompleted
                        ? 'text-slate-100'
                        : 'text-slate-400'
                    }`}
                  >
                    {milestone.title}
                  </h4>
                  <span className="text-[10px] font-mono px-1.5 py-0.2 rounded bg-slate-950 border border-slate-800 text-slate-400">
                    {milestone.engine}
                  </span>
                </div>
                <p className="text-[11px] text-slate-400 leading-relaxed">
                  {milestone.description}
                </p>
              </div>
            </div>

            {/* Status & Latency Badge */}
            <div className="flex flex-col items-end gap-1 shrink-0 font-mono text-xs">
              {isCompleted && (
                <span className="flex items-center gap-1 text-emerald-400 text-[11px] bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30 font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  DONE
                </span>
              )}
              {isRunning && (
                <span className="flex items-center gap-1 text-indigo-300 text-[11px] bg-indigo-500/20 px-2 py-0.5 rounded border border-indigo-500/40 animate-pulse font-semibold">
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  PROCESSING
                </span>
              )}
              {isFailed && (
                <span className="flex items-center gap-1 text-rose-400 text-[11px] bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/30 font-semibold">
                  <AlertTriangle className="w-3.5 h-3.5" />
                  ERROR
                </span>
              )}
              {isPending && (
                <span className="flex items-center gap-1 text-slate-500 text-[11px]">
                  <Clock className="w-3 h-3" />
                  PENDING
                </span>
              )}

              {milestone.latencyMs && (
                <span className="text-[10px] text-slate-400">
                  {milestone.latencyMs}ms
                </span>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
};
