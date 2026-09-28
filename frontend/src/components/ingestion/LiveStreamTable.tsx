import React, { useState } from 'react';
import { Search, RefreshCw, Eye, CheckCircle2, AlertTriangle, ShieldAlert } from 'lucide-react';
import { IngestionQueueRow, SCHEMA_CONFIG } from './IngestionDock';

export interface LiveStreamTableProps {
  tasks: IngestionQueueRow[];
  selectedTaskId?: string | null;
  onInspectTask: (task: IngestionQueueRow) => void;
}

export function StatusCell({ status, reason }: { status: string; reason?: string }) {
  if (status === 'Completed' || status === 'COMPLETED') {
    return (
      <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-2.5 py-0.5 text-xs font-medium text-emerald-400">
        <CheckCircle2 className="h-3 w-3" />
        Completed
      </span>
    );
  }
  if (status === 'Tax Discrepancy' || status === 'TAX_ANOMALY') {
    return (
      <div className="flex flex-col items-start gap-0.5">
        <span className="inline-flex items-center gap-1 rounded-full border border-amber-500/20 bg-amber-500/10 px-2 py-0.5 text-xs font-medium text-amber-400">
          <AlertTriangle className="h-3 w-3" />
          Tax Discrepancy
        </span>
        <span className="text-[11px] text-zinc-400">
          {reason || 'Calculated variance (68% vs 85% expected)'}
        </span>
      </div>
    );
  }
  if (status === 'Needs Review' || status === 'LOW_CONFIDENCE' || status === 'REVIEW_REQ') {
    return (
      <div className="flex flex-col items-start gap-0.5">
        <span className="inline-flex items-center gap-1 rounded-full border border-rose-500/20 bg-rose-500/10 px-2 py-0.5 text-xs font-medium text-rose-400">
          <ShieldAlert className="h-3 w-3" />
          Needs Review
        </span>
        <span className="text-[11px] text-zinc-400">
          {reason || 'Model confidence below 75% threshold'}
        </span>
      </div>
    );
  }
  return <span className="text-xs text-zinc-400">{status}</span>;
}

export const LiveStreamTable: React.FC<LiveStreamTableProps> = ({
  tasks,
  selectedTaskId,
  onInspectTask,
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLive, setIsLive] = useState(true);

  const filteredTasks = tasks.filter((task) => {
    const matchSearch =
      task.taskId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.filename.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.schemaType.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchSearch) return false;

    if (statusFilter === 'ALL') return true;
    if (statusFilter === 'ANOMALIES') {
      return task.status !== 'COMPLETED' && task.status !== 'Completed';
    }
    if (statusFilter === 'COMPLETED') {
      return task.status === 'COMPLETED' || task.status === 'Completed';
    }
    return true;
  });

  return (
    <div className="w-full max-w-full rounded-xl border border-zinc-800 bg-zinc-900/60 overflow-hidden shadow-sm">
      {/* Stream Controls Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 px-4 py-3 bg-zinc-900/50">
        <div className="flex items-center gap-2">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <h2 className="text-sm font-semibold tracking-wide uppercase text-zinc-200">
            Live Ingestion Stream
          </h2>
          <span className="rounded bg-zinc-800/80 px-1.5 py-0.5 text-[10px] font-medium text-zinc-400 border border-zinc-700/60">
            WebSocket Connected
          </span>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 focus-within:border-zinc-700">
            <Search className="h-3.5 w-3.5 text-zinc-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search task ID or document..."
              className="w-44 bg-transparent text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none font-sans"
            />
          </div>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 font-medium focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none cursor-pointer"
          >
            <option value="ALL">All Statuses</option>
            <option value="ANOMALIES">Anomalies &amp; Review</option>
            <option value="COMPLETED">Completed</option>
          </select>

          <button
            type="button"
            onClick={() => setIsLive((prev) => !prev)}
            className="flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 hover:bg-zinc-800 transition-colors cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isLive ? 'text-emerald-400 animate-spin-slow' : 'text-zinc-500'}`} />
            <span>{isLive ? 'Streaming Live' : 'Paused'}</span>
          </button>
        </div>
      </div>

      {/* Constrained Table Scroll Container */}
      <div className="w-full overflow-x-auto rounded-b-lg border-t border-zinc-800/80">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-zinc-800 bg-zinc-900/80 text-[11px] font-mono uppercase tracking-wider text-zinc-400">
            <tr>
              <th scope="col" className="py-3 px-4 font-semibold">Task ID</th>
              <th scope="col" className="py-3 px-4 font-semibold">Document / Schema</th>
              <th scope="col" className="py-3 px-3 font-semibold text-center">Priority</th>
              <th scope="col" className="py-3 px-4 font-semibold">Confidence</th>
              <th scope="col" className="py-3 px-3 font-semibold text-right">Latency</th>
              <th scope="col" className="py-3 px-4 font-semibold">Status &amp; Verification</th>
              <th scope="col" className="py-3 px-4 font-semibold text-right">Action</th>
            </tr>
          </thead>
          <tbody aria-live="polite" className="divide-y divide-zinc-800/60 text-zinc-300 text-xs">
            {filteredTasks.map((task) => (
              <tr
                key={task.taskId}
                onClick={() => onInspectTask(task)}
                className={`hover:bg-zinc-800/40 cursor-pointer transition-colors ${
                  selectedTaskId === task.taskId ? 'bg-zinc-800/30' : ''
                }`}
              >
                {/* Task ID */}
                <td className="py-3.5 px-4 font-mono font-semibold text-zinc-200">
                  {task.taskId}
                </td>

                {/* Document & Human-readable schema */}
                <td className="py-3.5 px-4">
                  <div className="flex flex-col">
                    <span className="font-medium text-zinc-100">{task.filename}</span>
                    <span className="text-[11px] text-zinc-400 font-sans">
                      {SCHEMA_CONFIG[task.schemaType]?.label || task.schemaType}
                    </span>
                  </div>
                </td>

                {/* Priority */}
                <td className="py-3.5 px-3 text-center">
                  <span className="rounded bg-zinc-800 px-2 py-0.5 text-[11px] font-mono font-medium text-zinc-300 border border-zinc-700/60">
                    {task.priority}
                  </span>
                </td>

                {/* Confidence with percentage and visual mini-bar */}
                <td className="py-3.5 px-4">
                  <div className="flex items-center gap-2.5">
                    <span className="font-mono text-xs tabular-nums text-zinc-200 font-medium">
                      {task.confidence.toFixed(1)}%
                    </span>
                    <div className="h-1.5 w-14 rounded-full bg-zinc-800 overflow-hidden shrink-0">
                      <div
                        className={`h-full ${
                          task.confidence >= 90
                            ? 'bg-emerald-500'
                            : task.confidence >= 75
                            ? 'bg-amber-500'
                            : 'bg-rose-500'
                        }`}
                        style={{ width: `${Math.min(100, Math.max(0, task.confidence))}%` }}
                      />
                    </div>
                  </div>
                </td>

                {/* Latency with monospace tabular nums and no space */}
                <td className="py-3.5 px-3 text-right font-mono tabular-nums text-zinc-300 font-medium">
                  {task.latencyMs}ms
                </td>

                {/* Status & Verification */}
                <td className="py-3.5 px-4">
                  <StatusCell status={task.status} reason={task.reviewReason} />
                </td>

                {/* Action Button */}
                <td className="py-3.5 px-4 text-right">
                  <button
                    type="button"
                    aria-label={`Inspect extraction for ${task.filename}`}
                    onClick={(e) => {
                      e.stopPropagation();
                      onInspectTask(task);
                    }}
                    className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-medium transition-all focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none ${
                      selectedTaskId === task.taskId
                        ? 'border-indigo-500 bg-indigo-500/20 text-indigo-300'
                        : 'border-zinc-800 bg-zinc-800/40 text-zinc-300 hover:border-zinc-700 hover:bg-zinc-700/60 hover:text-white'
                    }`}
                  >
                    <Eye className="h-3.5 w-3.5 text-zinc-400" />
                    <span>Inspect</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
