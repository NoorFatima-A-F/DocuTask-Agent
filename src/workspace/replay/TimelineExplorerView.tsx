import React, { useState, useEffect } from 'react';
import type { TimelineSummary, TimelineEntry } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface TimelineExplorerViewProps {
  missionId: string;
  onSelectEvent?: (entry: TimelineEntry) => void;
}

export const TimelineExplorerView: React.FC<TimelineExplorerViewProps> = ({
  missionId,
  onSelectEvent,
}) => {
  const [timeline, setTimeline] = useState<TimelineSummary | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [selectedStage, setSelectedStage] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    EsmrReplayApiClient.getTimeline(missionId)
      .then(setTimeline)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [missionId]);

  if (loading || !timeline) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Reconstructing Chronological Event Stream from Immutable Event Log...
      </div>
    );
  }

  const filteredEntries = timeline.entries.filter((e) => {
    if (selectedCategory !== 'ALL' && e.category !== selectedCategory) return false;
    if (selectedStage !== 'ALL' && e.stage !== selectedStage) return false;
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      return (
        e.summary.toLowerCase().includes(q) ||
        e.event_type.toLowerCase().includes(q) ||
        e.event_id.toLowerCase().includes(q) ||
        (e.task_id && e.task_id.toLowerCase().includes(q))
      );
    }
    return true;
  });

  const categories = ['ALL', ...Object.keys(timeline.categories)];
  const stages = ['ALL', ...timeline.stages];

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>📜</span> Event-Sourced Mission Timeline Explorer
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Total Events: <span className="font-mono text-cyan-400">{timeline.total_events}</span> | Duration:{' '}
            <span className="font-mono text-emerald-400">{timeline.total_duration_ms.toFixed(1)} ms</span>
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap items-center gap-3">
          <input
            type="text"
            placeholder="Search event type, summary..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
          />

          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
          >
            {categories.map((c) => (
              <option key={c} value={c}>
                Category: {c}
              </option>
            ))}
          </select>

          <select
            value={selectedStage}
            onChange={(e) => setSelectedStage(e.target.value)}
            className="px-3 py-1.5 bg-slate-900 border border-slate-700 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
          >
            {stages.map((s) => (
              <option key={s} value={s}>
                Stage: {s}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Timeline Stream Table */}
      <div className="overflow-x-auto max-h-[500px] overflow-y-auto border border-slate-800 rounded-lg">
        <table className="w-full text-left border-collapse font-mono text-xs">
          <thead className="bg-slate-900/90 sticky top-0 border-b border-slate-800 text-slate-400">
            <tr>
              <th className="py-2.5 px-3">#</th>
              <th className="py-2.5 px-3">Stage</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Event Type</th>
              <th className="py-2.5 px-3">Summary</th>
              <th className="py-2.5 px-3">Worker</th>
              <th className="py-2.5 px-3">Duration</th>
              <th className="py-2.5 px-3">Hash Pointer</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {filteredEntries.map((e) => {
              const categoryColor: Record<string, string> = {
                MISSION: 'text-cyan-400 bg-cyan-950/50 border-cyan-500/30',
                PLANNER: 'text-purple-400 bg-purple-950/50 border-purple-500/30',
                EXECUTION: 'text-emerald-400 bg-emerald-950/50 border-emerald-500/30',
                GOVERNANCE: 'text-amber-400 bg-amber-950/50 border-amber-500/30',
                REFLECTION: 'text-pink-400 bg-pink-950/50 border-pink-500/30',
                WORKER: 'text-blue-400 bg-blue-950/50 border-blue-500/30',
              };
              const badgeClass =
                categoryColor[e.category] || 'text-slate-400 bg-slate-900 border-slate-700';

              return (
                <tr
                  key={e.event_id}
                  onClick={() => onSelectEvent && onSelectEvent(e)}
                  className="hover:bg-slate-900/60 cursor-pointer transition-colors"
                >
                  <td className="py-2.5 px-3 text-slate-400">{e.sequence_number}</td>
                  <td className="py-2.5 px-3 font-semibold text-slate-200">{e.stage}</td>
                  <td className="py-2.5 px-3">
                    <span className={`px-2 py-0.5 rounded border text-[10px] ${badgeClass}`}>
                      {e.category}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 text-slate-300">{e.event_type}</td>
                  <td className="py-2.5 px-3 text-slate-200 font-sans">{e.summary}</td>
                  <td className="py-2.5 px-3 text-slate-400">{e.worker_id || '-'}</td>
                  <td className="py-2.5 px-3 text-emerald-400">
                    {e.duration_ms ? `${e.duration_ms.toFixed(1)} ms` : '-'}
                  </td>
                  <td className="py-2.5 px-3 text-slate-500 font-mono text-[10px]">
                    {e.hash.slice(0, 8)}...{e.hash.slice(-6)}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};
