import React from 'react';
import { Layers, ArrowRight, CheckCircle2, Loader2 } from 'lucide-react';
import { UploadResponse } from '../../types/document';
import { JobSubmitResponse } from '../../types/job';

interface UploadQueueProps {
  isUploading: boolean;
  progress: number;
  uploadedDocument: UploadResponse | null;
  submittedJob: JobSubmitResponse | null;
  onNavigateToJob: (jobId: string) => void;
}

export const UploadQueue: React.FC<UploadQueueProps> = ({
  isUploading,
  progress,
  uploadedDocument,
  submittedJob,
  onNavigateToJob,
}) => {
  if (!isUploading && !uploadedDocument && !submittedJob) return null;

  return (
    <div className="p-4 rounded-xl border border-slate-800 bg-slate-900/40 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-xs font-mono font-semibold text-slate-300 flex items-center gap-2">
          <Layers className="w-3.5 h-3.5 text-indigo-400" />
          Ingestion & Asynchronous Dispatch Queue
        </span>
        {isUploading ? (
          <span className="text-xs font-mono text-cyan-400 flex items-center gap-1.5">
            <Loader2 className="w-3 h-3 animate-spin" />
            Dispatching ({progress}%)
          </span>
        ) : (
          <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Enqueued &lt;100ms
          </span>
        )}
      </div>

      {/* Progress Bar */}
      {isUploading && (
        <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
          <div
            className="bg-gradient-to-r from-indigo-500 via-cyan-500 to-emerald-400 h-full transition-all duration-300 rounded-full"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* Result Cards */}
      {uploadedDocument && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs font-mono">
          <div className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 space-y-1">
            <span className="text-[10px] text-slate-400 uppercase">Document Ingestion</span>
            <div className="flex items-center justify-between text-slate-200">
              <span className="truncate">{uploadedDocument.filename}</span>
              <span className="text-emerald-400 font-bold">201 CREATED</span>
            </div>
            <div className="text-[10px] text-slate-400 truncate">
              ID: {uploadedDocument.id}
            </div>
          </div>

          {submittedJob && (
            <div className="p-2.5 rounded-lg bg-indigo-950/20 border border-indigo-500/30 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-[10px] text-indigo-400 uppercase">Celery Job Dispatched</span>
                <span className="text-[10px] text-amber-400 bg-amber-500/10 px-1.5 py-0.5 rounded border border-amber-500/30">
                  PRIORITY: HIGH
                </span>
              </div>
              <div className="flex items-center justify-between text-slate-200">
                <span className="text-cyan-300 truncate">Job #{submittedJob.job_id.substring(0, 12)}...</span>
                <button
                  onClick={() => onNavigateToJob(submittedJob.job_id)}
                  className="flex items-center gap-1 text-[11px] text-indigo-300 hover:text-indigo-100 underline underline-offset-2"
                >
                  Monitor
                  <ArrowRight className="w-3 h-3" />
                </button>
              </div>
              <div className="text-[10px] text-slate-400 truncate">
                Idempotency Key: {submittedJob.idempotency_key.substring(0, 16)}...
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
