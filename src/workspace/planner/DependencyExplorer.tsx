import React, { useState, useEffect } from 'react';
import {
  GitCommit,
  ArrowRight,
  RefreshCw,
} from 'lucide-react';
import { ApdlePlannerApiClient } from '../../services/apdlePlannerApiClient';
import { VisualDAGSnapshotPayload } from '../../types/apdlePlanner';

export const DependencyExplorer: React.FC = () => {
  const [dag, setDag] = useState<VisualDAGSnapshotPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadDag();
  }, []);

  const loadDag = async () => {
    setLoading(true);
    try {
      const data = await ApdlePlannerApiClient.getGraph('default_mission');
      setDag(data);
    } catch (e) {
      console.error('Failed to load dependencies:', e);
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
              <GitCommit className="w-4 h-4 text-purple-400" />
              Dynamic Dependency Resolution Explorer
            </h3>
            <p className="text-xs text-slate-400 mt-0.5">
              Inspects typed dependency edges (Hard, Soft, Optional, Conditional) and runtime satisfaction states.
            </p>
          </div>

          <button
            onClick={loadDag}
            disabled={loading}
            className="text-slate-400 hover:text-cyan-400 p-1.5 rounded"
            title="Refresh"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
          </button>
        </div>

        {/* Dependency Edge List */}
        <div className="space-y-3">
          {dag?.edges.map((edge) => {
            const sourceNode = dag.nodes.find((n) => n.id === edge.source);
            const targetNode = dag.nodes.find((n) => n.id === edge.target);

            return (
              <div
                key={edge.id}
                className="p-3 bg-slate-950/80 border border-slate-800 rounded-lg flex flex-col md:flex-row md:items-center justify-between gap-3 text-xs"
              >
                <div className="flex items-center gap-3">
                  <span className="font-bold text-slate-200">
                    {sourceNode?.label || edge.source}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-500 shrink-0" />
                  <span className="font-bold text-slate-200">
                    {targetNode?.label || edge.target}
                  </span>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <span className="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 border border-slate-700">
                    {edge.edge_type}
                  </span>
                  {edge.is_critical_path && (
                    <span className="px-2 py-0.5 rounded text-[10px] bg-amber-950 text-amber-300 border border-amber-800 font-bold">
                      CRITICAL EDGE
                    </span>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
