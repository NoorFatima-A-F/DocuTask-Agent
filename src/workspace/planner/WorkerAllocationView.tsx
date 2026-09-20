import React, { useState, useEffect } from 'react';
import {
  Server,
  RefreshCw,
} from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
import { ScheduleStatusPayload } from '../../types/apdlePlanner';

export const WorkerAllocationView: React.FC = () => {
  const [schedule, setSchedule] = useState<ScheduleStatusPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadSchedule();
  }, []);

  const loadSchedule = async () => {
    setLoading(true);
    try {
      const data = await ApdlePlannerApiClient.getSchedule('default_mission');
      setSchedule(data);
    } catch (e) {
      console.error('Failed to load schedule:', e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Server className="w-4 h-4 text-cyan-400" />
              Heterogeneous Worker Allocation & Capability Matching
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Multi-factor capability matching, load balancing, and active concurrency limits across dedicated worker pools.
            </p>
          </div>

          <button
            onClick={loadSchedule}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Worker Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {schedule?.workers.map((w) => {
            const loadPct = (w.active_tasks / Math.max(1, w.max_concurrency)) * 100;
            return (
              <div
                key={w.worker_id}
                className="p-4 bg-slate-950/80 border border-slate-800 rounded-xl space-y-3 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-100">{w.name}</span>
                  <span
                    className={`text-[9px] px-2 py-0.5 rounded border font-bold ${
                      w.status === 'BUSY'
                        ? 'bg-amber-950 text-amber-300 border-amber-800'
                        : 'bg-emerald-950 text-emerald-300 border-emerald-800'
                    }`}
                  >
                    {w.status}
                  </span>
                </div>

                <div className="flex flex-wrap gap-1">
                  {w.capabilities.map((cap) => (
                    <span
                      key={cap}
                      className="px-1.5 py-0.5 rounded text-[9px] bg-slate-800 text-cyan-300 border border-slate-700"
                    >
                      {cap}
                    </span>
                  ))}
                </div>

                {/* Utilization Progress Bar */}
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px] text-slate-400">
                    <span>Concurrency Load</span>
                    <span>
                      {w.active_tasks} / {w.max_concurrency} ({loadPct.toFixed(0)}%)
                    </span>
                  </div>
                  <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                    <div
                      style={{ width: `${loadPct}%` }}
                      className={`h-full transition-all ${
                        loadPct >= 75 ? 'bg-amber-500' : 'bg-cyan-500'
                      }`}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-400 pt-2 border-t border-slate-800/60">
                  <div>
                    Success: <span className="text-emerald-400 font-bold">{(w.historical_success_rate * 100).toFixed(0)}%</span>
                  </div>
                  <div>
                    Avg Latency: <span className="text-amber-300 font-bold">{w.average_latency_ms.toFixed(0)}ms</span>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
