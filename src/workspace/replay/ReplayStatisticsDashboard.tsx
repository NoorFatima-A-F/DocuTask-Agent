import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { BarChart3, Activity } from 'lucide-react';

export const ReplayStatisticsDashboard: React.FC = () => {
  const stats = [
    { title: 'Replay Total Duration', value: '680.0ms', sub: 'Across 10 Events' },
    { title: 'Peak Event Density', value: '14.7 evt/s', sub: 'During Parallel OCR' },
    { title: 'Worker Utilization', value: '88.5%', sub: 'Zero Idle Bottlenecks' },
    { title: 'Total Dollar Cost', value: '$0.0034', sub: 'Model & Tool Calls' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-cyan-500/20 to-teal-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <BarChart3 className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Replay Operational Statistics
                <Badge variant="intelligence" size="sm">Subsystem Profiler</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Operational telemetry, event density distribution, latency breakdown, and cost trajectories.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="sm">Optimal Efficiency</Badge>
        </div>
      </div>

      {/* Summary Stat Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        {stats.map((s, idx) => (
          <Card key={idx} className="p-4 bg-[#0F172A] border-[#1E293B]">
            <div className="text-xs text-slate-400">{s.title}</div>
            <div className="text-2xl font-bold text-white mt-1">{s.value}</div>
            <div className="text-[11px] text-emerald-400 mt-0.5">{s.sub}</div>
          </Card>
        ))}
      </div>

      {/* Subsystem Latency Breakdown */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] font-mono text-xs space-y-3">
        <div className="flex items-center justify-between border-b border-slate-800 pb-2">
          <span className="font-bold text-slate-200 flex items-center gap-2">
            <Activity className="w-4 h-4 text-indigo-400" />
            Subsystem Latency Share
          </span>
          <Badge variant="outline" size="sm">Total: 680ms</Badge>
        </div>

        <div className="space-y-2">
          <div>
            <div className="flex justify-between text-slate-400 mb-1">
              <span>OCR & Image Preprocessing</span>
              <span className="text-cyan-400">285ms (41.9%)</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
              <div className="bg-cyan-400 h-2 rounded-full" style={{ width: '41.9%' }}></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-slate-400 mb-1">
              <span>Schema Matching & Invariant Solving</span>
              <span className="text-indigo-400">235ms (34.5%)</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
              <div className="bg-indigo-400 h-2 rounded-full" style={{ width: '34.5%' }}></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-slate-400 mb-1">
              <span>Confidence Engine & Truth Merkle Sealing</span>
              <span className="text-emerald-400">160ms (23.6%)</span>
            </div>
            <div className="w-full bg-slate-800 rounded-full h-2">
              <div className="bg-emerald-400 h-2 rounded-full" style={{ width: '23.6%' }}></div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};
