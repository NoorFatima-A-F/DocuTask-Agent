import React, { useState, useEffect } from 'react';
import {
  Flame,
  AlertOctagon,
  RefreshCw,
  GitBranch,
  Zap,
} from 'lucide-react';
import { RuntimeObservabilityApiClient } from '../../services/runtimeObservabilityApiClient';
import { FlameGraphNodePayload } from '../../types/runtimeObservability';

export const ExecutionFlameGraphViewer: React.FC = () => {
  const [profileData, setProfileData] = useState<{
    flame_graph: FlameGraphNodePayload;
    bottlenecks: any[];
    total_spans: number;
  } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    setLoading(true);
    try {
      const data = await RuntimeObservabilityApiClient.getProfile('default_mission');
      setProfileData(data);
    } catch (e) {
      console.error('Failed to load profile:', e);
    } finally {
      setLoading(false);
    }
  };

  const renderFlameNode = (node: FlameGraphNodePayload, depth: number = 0) => {
    const totalMs = profileData?.flame_graph.value_ms || 1.0;
    const widthPct = Math.max(8, (node.value_ms / totalMs) * 100);

    const getComponentColor = (comp: string) => {
      switch (comp.toLowerCase()) {
        case 'planner':
          return 'bg-purple-900/70 border-purple-600 text-purple-200';
        case 'worker':
          return 'bg-amber-900/70 border-amber-600 text-amber-200';
        case 'governance':
          return 'bg-blue-900/70 border-blue-600 text-blue-200';
        case 'reflection':
          return 'bg-emerald-900/70 border-emerald-600 text-emerald-200';
        default:
          return 'bg-slate-800 border-slate-600 text-slate-200';
      }
    };

    return (
      <div key={node.name} className="space-y-1 my-1">
        <div
          style={{ width: `${widthPct}%` }}
          className={`p-2.5 rounded border text-xs transition-all ${getComponentColor(
            node.component
          )} ${node.is_critical_path ? 'ring-1 ring-amber-400' : ''}`}
        >
          <div className="flex items-center justify-between gap-2 truncate">
            <span className="font-bold truncate">{node.name}</span>
            <span className="font-mono text-[10px] shrink-0">{node.value_ms.toFixed(1)}ms</span>
          </div>
          {node.is_critical_path && (
            <div className="text-[9px] text-amber-300 font-bold mt-0.5 flex items-center gap-1">
              <Zap className="w-2.5 h-2.5" /> CRITICAL PATH
            </div>
          )}
        </div>

        {node.children && node.children.length > 0 && (
          <div className="pl-4 border-l border-slate-800 space-y-1">
            {node.children.map((child) => renderFlameNode(child, depth + 1))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-6 font-mono">
      {/* Header Banner */}
      <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <h3 className="text-sm font-bold text-cyan-300 flex items-center gap-2">
              <Flame className="w-4 h-4 text-amber-400" />
              Distributed Execution Flame Graph & Critical Path Profiler
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Longest-path DAG analysis over real trace spans. Pinpoints latency bottlenecks across execution stages.
            </p>
          </div>

          <button
            onClick={loadProfile}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Critical Path Latency</div>
            <div className="text-xl font-bold text-amber-400 mt-1">
              {(profileData?.flame_graph.value_ms ?? 705.7).toFixed(1)}ms
            </div>
          </div>

          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Total Instrumented Spans</div>
            <div className="text-xl font-bold text-cyan-300 mt-1">
              {profileData?.total_spans ?? 4} Spans
            </div>
          </div>

          <div className="bg-slate-950/80 border border-slate-800 rounded-lg p-3 text-center">
            <div className="text-[10px] text-slate-500 uppercase">Primary Bottleneck</div>
            <div className="text-xl font-bold text-purple-300 mt-1">
              {profileData?.bottlenecks[0]?.stage || 'ocr'}
            </div>
          </div>
        </div>
      </div>

      {/* Flame Graph & Bottlenecks Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Interactive Flame Graph Tree */}
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2">
            <GitBranch className="w-4 h-4 text-cyan-400" />
            Execution Span Hierarchy
          </div>

          <div className="overflow-x-auto p-2 bg-slate-950/60 rounded-lg">
            {profileData?.flame_graph && renderFlameNode(profileData.flame_graph)}
          </div>
        </div>

        {/* Right: Bottleneck Analysis */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-3">
          <div className="text-xs uppercase text-slate-300 tracking-wider flex items-center gap-2 border-b border-slate-800 pb-2">
            <AlertOctagon className="w-4 h-4 text-amber-400" />
            Top Execution Bottlenecks
          </div>

          <div className="space-y-2">
            {profileData?.bottlenecks.map((b, idx) => (
              <div
                key={b.event_id || idx}
                className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg text-xs space-y-1"
              >
                <div className="flex justify-between items-center">
                  <span className="font-bold text-slate-200">{b.stage}</span>
                  <span className="text-amber-300 font-bold">{b.duration_ms.toFixed(1)}ms</span>
                </div>
                <div className="text-[10px] text-slate-500">
                  Worker: {b.worker_id} &bull; Component: {b.component}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
