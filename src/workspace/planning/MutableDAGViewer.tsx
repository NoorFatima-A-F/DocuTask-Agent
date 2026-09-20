/**
 * Mutable Execution DAG Visualizer & Interactive Mutation Console.
 * Visualizes dynamic execution topology, node states, and supports runtime DAG splitting, replacement, and cloning.
 */

import React, { useState, useEffect } from 'react';
import { MutableExecutionDAG } from '../../types/autonomousPlanning';
import { PlanningApiClient } from '../../services/planningApiClient';

interface MutableDAGViewerProps {
  missionId?: string;
}

export const MutableDAGViewerView: React.FC<MutableDAGViewerProps> = ({
  missionId = 'mission_active_001',
}) => {
  const [dag, setDag] = useState<MutableExecutionDAG | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);
  const [mutationActionLoading, setMutationActionLoading] = useState<boolean>(false);

  useEffect(() => {
    loadDAG();
  }, [missionId]);

  const loadDAG = async () => {
    setLoading(true);
    try {
      const activeDag = await PlanningApiClient.getDAG(missionId);
      setDag(activeDag);
      const nodeKeys = Object.keys(activeDag.nodes);
      const firstKey = nodeKeys[0];
      if (firstKey) {
        setSelectedNodeId(firstKey);
      }
    } catch (err) {
      console.error('Failed to load DAG', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSplitNode = async (nodeId: string) => {
    setMutationActionLoading(true);
    try {
      const updatedDag = await PlanningApiClient.mutateDAG(missionId, 'NODE_SPLIT', nodeId, 2);
      setDag(updatedDag);
    } catch (err) {
      console.error('Split failed', err);
    } finally {
      setMutationActionLoading(false);
    }
  };

  const handleReplaceNode = async (nodeId: string) => {
    setMutationActionLoading(true);
    try {
      const updatedDag = await PlanningApiClient.mutateDAG(missionId, 'NODE_REPLACE', nodeId, 2);
      setDag(updatedDag);
    } catch (err) {
      console.error('Replace failed', err);
    } finally {
      setMutationActionLoading(false);
    }
  };

  if (loading || !dag) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-500 mr-3"></div>
        <span>Constructing Mutable Execution Topology...</span>
      </div>
    );
  }

  const nodesList = Object.values(dag.nodes);
  const selectedNode = selectedNodeId ? dag.nodes[selectedNodeId] : null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 text-slate-100 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between border-b border-slate-800 pb-4 gap-4">
        <div>
          <div className="flex items-center space-x-3">
            <span className="px-2.5 py-1 text-xs font-bold uppercase tracking-wider bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 rounded-md">
              Dynamic Execution Topology
            </span>
            <span className="text-xs text-slate-400 font-mono">DAG: {dag.dag_id} (v{dag.version})</span>
          </div>
          <h2 className="text-xl font-bold text-white mt-1">Mutable Execution DAG & Live Mutations</h2>
          <p className="text-sm text-slate-400">
            Runtime-adaptable graph supporting live shard splitting, capability hot-swapping, and branch rewiring.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={loadDAG}
            className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-semibold border border-slate-700 transition"
          >
            Refresh DAG
          </button>
        </div>
      </div>

      {/* DAG Visual Nodes Canvas */}
      <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-5 overflow-x-auto">
        <div className="flex items-center space-x-4 min-w-[700px]">
          {nodesList.map((node, index) => {
            const isSelected = node.node_id === selectedNodeId;
            const isCompleted = node.status === 'COMPLETED';
            const isRunning = node.status === 'RUNNING';
            const isMutated = node.status === 'MUTATED';

            return (
              <React.Fragment key={node.node_id}>
                {index > 0 && (
                  <div className="flex items-center text-slate-600 font-mono text-lg select-none">
                    →
                  </div>
                )}
                <div
                  onClick={() => setSelectedNodeId(node.node_id)}
                  className={`flex-1 min-w-[180px] p-3.5 rounded-lg border cursor-pointer transition-all duration-200 ${
                    isSelected
                      ? 'border-indigo-500 bg-indigo-950/40 shadow-lg shadow-indigo-500/10'
                      : isCompleted
                      ? 'border-emerald-700/60 bg-emerald-950/20 hover:border-emerald-600'
                      : isRunning
                      ? 'border-cyan-500/60 bg-cyan-950/30 animate-pulse'
                      : isMutated
                      ? 'border-slate-800 bg-slate-900/40 opacity-50'
                      : 'border-slate-800 bg-slate-900/80 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1.5">
                    <span className="text-[10px] font-mono text-slate-400 truncate">
                      {node.node_id}
                    </span>
                    <span className={`text-[9px] font-bold uppercase px-1.5 py-0.5 rounded ${
                      isCompleted
                        ? 'bg-emerald-500/20 text-emerald-400'
                        : isRunning
                        ? 'bg-cyan-500/20 text-cyan-300'
                        : isMutated
                        ? 'bg-slate-800 text-slate-500'
                        : 'bg-slate-800 text-slate-400'
                    }`}>
                      {node.status}
                    </span>
                  </div>

                  <div className="font-semibold text-xs text-white truncate">{node.name}</div>
                  <div className="text-[11px] font-mono text-indigo-300 mt-1 truncate">{node.provider}</div>
                </div>
              </React.Fragment>
            );
          })}
        </div>
      </div>

      {/* Node Inspector & Live Mutation Controls */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {selectedNode ? (
          <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
              <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
                Node Inspector: <span className="text-indigo-400 font-mono">{selectedNode.node_id}</span>
              </h4>
              <span className="text-xs font-mono text-emerald-400">{selectedNode.status}</span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-xs font-mono">
              <div>
                <span className="text-slate-500 block text-[10px]">CAPABILITY</span>
                <span className="text-slate-300">{selectedNode.capability_id}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">PROVIDER</span>
                <span className="text-slate-300">{selectedNode.provider}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">RETRIES</span>
                <span className="text-slate-300">{selectedNode.retry_count} / {selectedNode.max_retries}</span>
              </div>
              <div>
                <span className="text-slate-500 block text-[10px]">TIMEOUT</span>
                <span className="text-slate-300">{selectedNode.timeout_ms} ms</span>
              </div>
            </div>

            {/* Mutation Action Buttons */}
            <div className="pt-2 border-t border-slate-800 flex flex-wrap gap-2">
              <button
                onClick={() => handleSplitNode(selectedNode.node_id)}
                disabled={mutationActionLoading || selectedNode.status === 'COMPLETED'}
                className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white rounded text-xs font-semibold transition"
              >
                Split into 2 Shards
              </button>
              <button
                onClick={() => handleReplaceNode(selectedNode.node_id)}
                disabled={mutationActionLoading || selectedNode.status === 'COMPLETED'}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-slate-200 border border-slate-700 rounded text-xs font-semibold transition"
              >
                Hot-Swap Capability
              </button>
            </div>
          </div>
        ) : (
          <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4 text-xs text-slate-500 flex items-center justify-center">
            Select a DAG node to inspect properties and trigger mutations.
          </div>
        )}

        {/* Mutation History Audit Trail */}
        <div className="bg-slate-950/60 border border-slate-800 rounded-lg p-4 space-y-2">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
              DAG Mutation Audit Trail
            </h4>
            <span className="text-[10px] font-mono text-slate-500">{dag.mutation_history.length} events</span>
          </div>

          <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
            {dag.mutation_history.length === 0 ? (
              <p className="text-xs text-slate-500 font-mono">No mutations applied to current topology.</p>
            ) : (
              dag.mutation_history.map((m) => (
                <div key={m.mutation_id} className="p-2 bg-slate-900/90 rounded border border-slate-800 text-xs font-mono">
                  <div className="flex items-center justify-between text-[10px]">
                    <span className="font-bold text-cyan-400">{m.mutation_type}</span>
                    <span className="text-slate-500">{new Date(m.timestamp).toLocaleTimeString()}</span>
                  </div>
                  <div className="text-slate-300 mt-1 font-sans">{m.diff_summary}</div>
                  <div className="text-[10px] text-slate-500 mt-0.5">{m.rationale}</div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
