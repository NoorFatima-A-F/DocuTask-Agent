import { useState } from 'react';
import { Search, RefreshCw, Eye, CheckCircle2, AlertTriangle, ShieldAlert, ArrowUpDown, ChevronUp, ChevronDown, Download, CheckSquare, Square } from 'lucide-react';
import { IngestionTask } from '../../pages/IngestionStudio';

export interface LiveStreamTableProps {
  tasks: IngestionTask[];
  selectedTaskId?: string | null;
  onSelectTask: (task: IngestionTask) => void;
}

type SortField = 'id' | 'confidence' | 'latencyMs';
type SortOrder = 'asc' | 'desc';

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
        <span className="text-[11px] text-zinc-400 font-sans">
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
        <span className="text-[11px] text-zinc-400 font-sans">
          {reason || 'Model confidence below 75% threshold'}
        </span>
      </div>
    );
  }
  return <span className="text-xs text-zinc-400">{status}</span>;
}

export function LiveStreamTable({
  tasks,
  selectedTaskId,
  onSelectTask,
}: LiveStreamTableProps) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [isLive, setIsLive] = useState(true);
  const [sortField, setSortField] = useState<SortField>('id');
  const [sortOrder, setSortOrder] = useState<SortOrder>('asc');
  const [selectedIds, setSelectedIds] = useState<string[]>([]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortOrder('desc');
    }
  };

  const filteredTasks = tasks
    .filter((task) => {
      const matchSearch =
        task.id.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.documentName.toLowerCase().includes(searchQuery.toLowerCase()) ||
        task.schema.toLowerCase().includes(searchQuery.toLowerCase());

      if (!matchSearch) return false;

      if (statusFilter === 'ALL') return true;
      if (statusFilter === 'ANOMALIES') {
        return task.status !== 'Completed';
      }
      if (statusFilter === 'COMPLETED') {
        return task.status === 'Completed';
      }
      return true;
    })
    .sort((a, b) => {
      let comparison = 0;
      if (sortField === 'id') {
        comparison = a.id.localeCompare(b.id);
      } else if (sortField === 'confidence') {
        comparison = a.confidence - b.confidence;
      } else if (sortField === 'latencyMs') {
        comparison = a.latencyMs - b.latencyMs;
      }
      return sortOrder === 'asc' ? comparison : -comparison;
    });

  const toggleSelectAll = () => {
    if (selectedIds.length === filteredTasks.length) {
      setSelectedIds([]);
    } else {
      setSelectedIds(filteredTasks.map((t) => t.id));
    }
  };

  const toggleSelectRow = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((i) => i !== id) : [...prev, id]
    );
  };

  const handleExportCSV = () => {
    const exportData = filteredTasks.filter((t) =>
      selectedIds.length > 0 ? selectedIds.includes(t.id) : true
    );
    const headers = ['Task ID', 'Document Name', 'Schema', 'Priority', 'Confidence', 'Latency (ms)', 'Status', 'Timestamp'];
    const rows = exportData.map((t) => [
      t.id,
      t.documentName,
      t.schema,
      t.priority,
      `${t.confidence.toFixed(1)}%`,
      `${t.latencyMs}ms`,
      t.status,
      t.timestamp,
    ]);
    const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map((e) => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `docutask_stream_export_${Date.now()}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const handleExportJSON = () => {
    const exportData = filteredTasks.filter((t) =>
      selectedIds.length > 0 ? selectedIds.includes(t.id) : true
    );
    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `docutask_stream_export_${Date.now()}.json`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="w-full max-w-full rounded-xl border border-zinc-800 bg-zinc-900/60 overflow-hidden shadow-sm">
      {/* Stream Controls Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-800 px-4 py-3 bg-zinc-900/50">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <h2 className="text-xs font-semibold tracking-wide uppercase text-zinc-200 font-mono">
              Live Ingestion Stream
            </h2>
            <span className="rounded bg-zinc-800/80 px-1.5 py-0.5 text-[10px] font-medium text-zinc-400 border border-zinc-700/60 font-mono">
              WS Active
            </span>
          </div>

          {/* Embedded Real-time Throughput Sparkline */}
          <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded bg-zinc-950/60 border border-zinc-800 text-[11px] font-mono text-zinc-400">
            <span className="text-zinc-400">Throughput:</span>
            <span className="text-zinc-200 font-semibold tabular-nums">38 docs/min</span>
            <svg viewBox="0 0 60 16" className="w-14 h-4 text-emerald-400" fill="none">
              <path
                d="M 2 12 L 12 8 L 22 10 L 32 4 L 42 7 L 52 2 L 58 5"
                stroke="currentColor"
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Quick Search Input */}
          <div className="flex items-center gap-2 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 focus-within:border-zinc-700">
            <Search className="h-3.5 w-3.5 text-zinc-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search task ID or document..."
              className="w-36 sm:w-44 bg-transparent text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none font-sans"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 font-medium focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none cursor-pointer font-sans"
          >
            <option value="ALL">All Statuses</option>
            <option value="ANOMALIES">Anomalies &amp; Review</option>
            <option value="COMPLETED">Completed</option>
          </select>

          {/* Export Dropdown Buttons */}
          <button
            type="button"
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors cursor-pointer font-mono"
            title="Export filtered records to CSV"
          >
            <Download className="h-3.5 w-3.5 text-zinc-400" />
            <span>CSV</span>
          </button>

          <button
            type="button"
            onClick={handleExportJSON}
            className="flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 hover:bg-zinc-800 hover:text-white transition-colors cursor-pointer font-mono"
            title="Export filtered records to JSON"
          >
            <Download className="h-3.5 w-3.5 text-zinc-400" />
            <span>JSON</span>
          </button>

          {/* Live Stream Toggle */}
          <button
            type="button"
            onClick={() => setIsLive((prev) => !prev)}
            className="flex items-center gap-1.5 rounded-lg border border-zinc-800 bg-zinc-900 px-2.5 py-1.5 text-xs text-zinc-300 hover:bg-zinc-800 transition-colors cursor-pointer focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none font-mono"
          >
            <RefreshCw className={`h-3.5 w-3.5 ${isLive ? 'text-emerald-400 animate-spin-slow' : 'text-zinc-500'}`} />
            <span>{isLive ? 'Live' : 'Paused'}</span>
          </button>
        </div>
      </div>

      {/* Bulk Action Notification Bar when items selected */}
      {selectedIds.length > 0 && (
        <div className="bg-indigo-950/60 border-b border-indigo-800/80 px-4 py-2 flex items-center justify-between text-xs font-mono text-indigo-200">
          <div className="flex items-center gap-2">
            <CheckSquare className="w-4 h-4 text-indigo-400" />
            <span>{selectedIds.length} document tasks selected</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => setSelectedIds([])}
              className="px-2 py-0.5 rounded bg-indigo-900/60 hover:bg-indigo-900 border border-indigo-700 text-indigo-200 cursor-pointer"
            >
              Deselect All
            </button>
            <button
              onClick={handleExportCSV}
              className="px-2.5 py-0.5 rounded bg-indigo-600 hover:bg-indigo-500 text-white font-semibold cursor-pointer shadow-sm"
            >
              Export Selected ({selectedIds.length})
            </button>
          </div>
        </div>
      )}

      {/* Constrained Table Scroll Container */}
      <div className="w-full overflow-x-auto rounded-b-lg border-t border-zinc-800/80">
        <table className="w-full text-left text-sm">
          <thead className="border-b border-zinc-800 bg-zinc-900/80 text-[11px] font-mono uppercase tracking-wider text-zinc-400 select-none">
            <tr>
              <th scope="col" className="py-3 px-3 w-10 text-center">
                <button
                  type="button"
                  onClick={toggleSelectAll}
                  aria-label="Select all rows"
                  className="text-zinc-400 hover:text-zinc-200 cursor-pointer inline-flex items-center"
                >
                  {selectedIds.length === filteredTasks.length && filteredTasks.length > 0 ? (
                    <CheckSquare className="w-4 h-4 text-indigo-400" />
                  ) : (
                    <Square className="w-4 h-4 text-zinc-500" />
                  )}
                </button>
              </th>
              <th
                scope="col"
                onClick={() => handleSort('id')}
                className="py-3 px-4 font-semibold cursor-pointer hover:text-zinc-200 transition-colors"
              >
                <div className="flex items-center gap-1.5">
                  <span>Task ID</span>
                  {sortField === 'id' ? (
                    sortOrder === 'asc' ? <ChevronUp className="w-3 h-3 text-indigo-400" /> : <ChevronDown className="w-3 h-3 text-indigo-400" />
                  ) : (
                    <ArrowUpDown className="w-3 h-3 text-zinc-600 opacity-60" />
                  )}
                </div>
              </th>
              <th scope="col" className="py-3 px-4 font-semibold">Document / Schema</th>
              <th scope="col" className="py-3 px-3 font-semibold text-center">Priority</th>
              <th
                scope="col"
                onClick={() => handleSort('confidence')}
                className="py-3 px-4 font-semibold cursor-pointer hover:text-zinc-200 transition-colors"
              >
                <div className="flex items-center gap-1.5">
                  <span>Confidence</span>
                  {sortField === 'confidence' ? (
                    sortOrder === 'asc' ? <ChevronUp className="w-3 h-3 text-indigo-400" /> : <ChevronDown className="w-3 h-3 text-indigo-400" />
                  ) : (
                    <ArrowUpDown className="w-3 h-3 text-zinc-600 opacity-60" />
                  )}
                </div>
              </th>
              <th
                scope="col"
                onClick={() => handleSort('latencyMs')}
                className="py-3 px-3 font-semibold text-right cursor-pointer hover:text-zinc-200 transition-colors"
              >
                <div className="flex items-center justify-end gap-1.5">
                  <span>Latency</span>
                  {sortField === 'latencyMs' ? (
                    sortOrder === 'asc' ? <ChevronUp className="w-3 h-3 text-indigo-400" /> : <ChevronDown className="w-3 h-3 text-indigo-400" />
                  ) : (
                    <ArrowUpDown className="w-3 h-3 text-zinc-600 opacity-60" />
                  )}
                </div>
              </th>
              <th scope="col" className="py-3 px-4 font-semibold">Status &amp; Verification</th>
              <th scope="col" className="py-3 px-4 font-semibold text-right">Action</th>
            </tr>
          </thead>
          <tbody aria-live="polite" className="divide-y divide-zinc-800/60 text-zinc-300 text-xs">
            {filteredTasks.map((task) => {
              const isSelected = selectedIds.includes(task.id);

              return (
                <tr
                  key={task.id}
                  onClick={() => onSelectTask(task)}
                  className={`hover:bg-zinc-800/40 cursor-pointer transition-colors ${
                    selectedTaskId === task.id ? 'bg-zinc-800/30' : ''
                  } ${isSelected ? 'bg-indigo-950/20' : ''}`}
                >
                  {/* Row Checkbox */}
                  <td className="py-3.5 px-3 text-center">
                    <button
                      type="button"
                      onClick={(e) => toggleSelectRow(task.id, e)}
                      aria-label={`Select row for ${task.id}`}
                      className="text-zinc-400 hover:text-zinc-200 cursor-pointer inline-flex items-center"
                    >
                      {isSelected ? (
                        <CheckSquare className="w-4 h-4 text-indigo-400" />
                      ) : (
                        <Square className="w-4 h-4 text-zinc-600" />
                      )}
                    </button>
                  </td>

                  {/* Task ID */}
                  <td className="py-3.5 px-4 font-mono font-semibold text-zinc-200">
                    {task.id}
                  </td>

                  {/* Document & Human-readable schema */}
                  <td className="py-3.5 px-4">
                    <div className="flex flex-col">
                      <span className="font-medium text-zinc-100">{task.documentName}</span>
                      <span className="text-[11px] text-zinc-400 font-sans">
                        {task.schema} ({task.schemaBadge})
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
                    <StatusCell status={task.status} reason={task.statusDetails} />
                  </td>

                  {/* Action Button */}
                  <td className="py-3.5 px-4 text-right">
                    <button
                      type="button"
                      aria-label={`Inspect extraction for ${task.documentName}`}
                      onClick={(e) => {
                        e.stopPropagation();
                        onSelectTask(task);
                      }}
                      className={`inline-flex items-center gap-1.5 rounded-md border px-2.5 py-1 text-xs font-medium transition-all focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none cursor-pointer ${
                        selectedTaskId === task.id
                          ? 'border-indigo-500 bg-indigo-500/20 text-indigo-300'
                          : 'border-zinc-800 bg-zinc-800/40 text-zinc-300 hover:border-zinc-700 hover:bg-zinc-700/60 hover:text-white'
                      }`}
                    >
                      <Eye className="h-3.5 w-3.5 text-zinc-400" />
                      <span>Inspect</span>
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
