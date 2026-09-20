import React, { useState } from 'react';
import { useMissionControl } from '../../context/MissionControlContext';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import { Badge } from '../ui/Badge';
import type { MissionDagNode } from '../../types/missionControl';

export const MissionGraphSection: React.FC = () => {
  const { state } = useMissionControl();
  const { dagNodes } = state;
  const [selectedNode, setSelectedNode] = useState<MissionDagNode | null>(dagNodes[0] || null);

  const getNodeStatusBadge = (status: MissionDagNode['status']) => {
    switch (status) {
      case 'COMPLETED':
        return <Badge variant="success" size="sm">COMPLETED</Badge>;
      case 'IN_PROGRESS':
        return <Badge variant="intelligence" size="sm" hasDot isPulsing>IN PROGRESS</Badge>;
      case 'FAILED':
        return <Badge variant="error" size="sm">FAILED</Badge>;
      case 'SKIPPED':
        return <Badge variant="default" size="sm">SKIPPED</Badge>;
      case 'PENDING':
      default:
        return <Badge variant="default" size="sm">PENDING</Badge>;
    }
  };

  return (
    <section className="w-full mt-8">
      <Card variant="default" className="border-[#1E293B] bg-[#0F172A]/80 backdrop-blur-md">
        <CardHeader className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2">
          <div>
            <div className="flex items-center gap-2">
              <Badge variant="intelligence" size="sm">
                STAGE 5 • DAG TOPOLOGY
              </Badge>
              <span className="text-xs text-[#94A3B8] font-mono">
                {dagNodes.length} Execution Units
              </span>
            </div>
            <CardTitle className="mt-2 text-lg lg:text-xl font-bold text-[#F8FAFC]">
              Mission Dependency Graph (DAG)
            </CardTitle>
            <p className="mt-1 text-xs text-[#94A3B8]">
              Topologically sorted execution graph linking goals, adaptive preprocessing, Bayesian search, reflection, SLSA proofs, and publication evolution.
            </p>
          </div>
        </CardHeader>

        <CardContent className="p-6">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* LEFT: DAG Nodes Flow Visualizer (7 cols) */}
            <div className="lg:col-span-7 space-y-3">
              {dagNodes.map((node, index) => {
                const isSelected = selectedNode?.id === node.id;
                const isRunning = node.status === 'IN_PROGRESS';

                return (
                  <div key={node.id} className="relative">
                    <div
                      onClick={() => setSelectedNode(node)}
                      className={`p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                        isSelected
                          ? 'bg-[#1E293B] border-[#00D2FF] shadow-[0_0_15px_rgba(0,210,255,0.25)]'
                          : isRunning
                          ? 'bg-[#131D35] border-cyan-400/50 shadow-[0_0_15px_rgba(0,210,255,0.2)]'
                          : node.status === 'COMPLETED'
                          ? 'bg-[#131D35]/70 border-emerald-500/20 hover:bg-[#1E293B]/50'
                          : 'bg-[#0A0F1D]/40 border-[#1E293B] opacity-60 hover:opacity-90'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div
                          className={`h-7 w-7 rounded-lg flex items-center justify-center text-xs font-mono font-bold ${
                            node.status === 'COMPLETED'
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              : isRunning
                              ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 animate-pulse'
                              : 'bg-[#1E293B] text-[#64748B]'
                          }`}
                        >
                          {index + 1}
                        </div>

                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-semibold text-[#F8FAFC]">
                              {node.label}
                            </span>
                          </div>
                          <span className="text-[11px] font-mono text-[#64748B] block mt-0.5">
                            Assigned: {node.assignedAgent} • Type: {node.nodeType}
                          </span>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        {node.runtimeSeconds !== undefined && (
                          <span className="text-[11px] font-mono text-[#94A3B8]">
                            {node.runtimeSeconds}s
                          </span>
                        )}
                        {getNodeStatusBadge(node.status)}
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* RIGHT: Node Inspector Drawer (5 cols) */}
            <div className="lg:col-span-5">
              {selectedNode ? (
                <div className="p-5 rounded-xl bg-[#131D35] border border-[#334155] h-full flex flex-col justify-between">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
                      <div>
                        <span className="text-[10px] text-[#64748B] uppercase font-mono block">
                          Node Inspector
                        </span>
                        <h4 className="text-sm font-bold text-[#F8FAFC] mt-0.5">
                          {selectedNode.label}
                        </h4>
                      </div>
                      {getNodeStatusBadge(selectedNode.status)}
                    </div>

                    <div className="space-y-2 text-xs">
                      <div>
                        <span className="text-[#94A3B8] font-medium block">Inputs:</span>
                        <div className="flex flex-wrap gap-1 mt-1 font-mono text-[11px]">
                          {selectedNode.inputs.map((inp) => (
                            <span key={inp} className="bg-[#0A0F1D] text-slate-300 px-2 py-0.5 rounded border border-[#1E293B]">
                              📥 {inp}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div>
                        <span className="text-[#94A3B8] font-medium block">Outputs:</span>
                        <div className="flex flex-wrap gap-1 mt-1 font-mono text-[11px]">
                          {selectedNode.outputs.map((out) => (
                            <span key={out} className="bg-[#0A0F1D] text-emerald-300 px-2 py-0.5 rounded border border-emerald-500/30">
                              📤 {out}
                            </span>
                          ))}
                        </div>
                      </div>

                      {selectedNode.artifactsProduced.length > 0 && (
                        <div>
                          <span className="text-[#94A3B8] font-medium block">Produced Artifacts:</span>
                          <div className="flex flex-wrap gap-1 mt-1 font-mono text-[11px]">
                            {selectedNode.artifactsProduced.map((art) => (
                              <span key={art} className="bg-cyan-950/40 text-cyan-300 px-2 py-0.5 rounded border border-cyan-500/30">
                                📄 {art}
                              </span>
                            ))}
                          </div>
                        </div>
                      )}

                      {selectedNode.sha256Digest && (
                        <div className="pt-2 border-t border-[#1E293B]">
                          <span className="text-[#64748B] text-[10px] uppercase font-mono block">
                            Cryptographic Digest:
                          </span>
                          <span className="text-[10px] font-mono text-[#A855F7] block truncate mt-0.5">
                            {selectedNode.sha256Digest}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>

                  <div className="mt-4 pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs font-mono text-[#64748B]">
                    <span>Retries: {selectedNode.retryCount}</span>
                    <span>Assigned: {selectedNode.assignedAgent}</span>
                  </div>
                </div>
              ) : (
                <div className="p-8 text-center text-xs text-[#64748B] bg-[#131D35]/30 rounded-xl border border-dashed border-[#334155]">
                  Select a DAG node to inspect execution details
                </div>
              )}
            </div>
          </div>
        </CardContent>
      </Card>
    </section>
  );
};
