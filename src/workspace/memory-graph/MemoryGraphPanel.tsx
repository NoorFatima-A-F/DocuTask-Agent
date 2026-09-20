import React from 'react';
import { useWorkspace } from '../context/WorkspaceContext';
import { CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const MemoryGraphPanel: React.FC = () => {
  const { memoryNodes, selectedMemoryNodeId, selectMemoryNode } = useWorkspace();

  const activeNode =
    memoryNodes.find((n) => n.id === selectedMemoryNodeId) || memoryNodes[0];

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'DOCUMENT':
        return 'border-blue-500/50 text-blue-300 bg-blue-950/30';
      case 'FAILURE_MODE':
        return 'border-red-500/50 text-red-300 bg-red-950/30';
      case 'REFLECTION':
        return 'border-amber-500/50 text-amber-300 bg-amber-950/30';
      case 'LESSON_LEARNED':
        return 'border-cyan-500/50 text-cyan-300 bg-cyan-950/30';
      case 'INVARIANT_APPLIED':
        return 'border-emerald-500/50 text-emerald-300 bg-emerald-950/30';
      default:
        return 'border-slate-500/50 text-slate-300 bg-slate-950/30';
    }
  };

  return (
    <div className="w-full flex flex-col h-[700px] rounded-2xl bg-[#0F172A]/90 border border-[#1E293B] shadow-2xl overflow-hidden">
      <CardHeader className="flex flex-row items-center justify-between py-4 px-6 border-b border-[#1E293B] bg-[#131D35]/50">
        <div>
          <div className="flex items-center gap-2">
            <Badge variant="intelligence" size="sm">
              CAUSAL REASONING GRAPH
            </Badge>
            <span className="text-xs text-[#94A3B8] font-mono">
              {memoryNodes.length} Invariant Nodes
            </span>
          </div>
          <CardTitle className="mt-1 text-base font-bold text-[#F8FAFC]">
            Causal Memory & Experience Graph
          </CardTitle>
        </div>

        <div className="text-xs font-mono text-[#10B981] bg-[#0A0F1D] px-3 py-1.5 rounded-lg border border-emerald-500/30">
          Decay Half-Life: Active (R &ge; 0.90)
        </div>
      </CardHeader>

      <CardContent className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Interactive Visual Causal Nodes (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <span className="text-[11px] font-bold font-mono text-[#64748B] uppercase block">
            Causal Progression Chain:
          </span>

          {memoryNodes.map((node, i) => {
            const isSelected = selectedMemoryNodeId === node.id;
            const isLast = i === memoryNodes.length - 1;

            return (
              <div key={node.id} className="relative">
                <div
                  onClick={() => selectMemoryNode(node.id)}
                  className={`p-4 rounded-xl border transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#1E293B] border-cyan-400 shadow-[0_0_20px_rgba(0,210,255,0.25)] ring-1 ring-cyan-400'
                      : 'bg-[#131D35] hover:border-[#334155]'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className={`text-[10px] font-mono uppercase px-2 py-0.5 rounded border ${getNodeColor(node.nodeType)}`}>
                        {node.nodeType}
                      </span>
                      <h4 className="text-xs font-bold text-[#F8FAFC]">
                        {node.label}
                      </h4>
                    </div>

                    <span className="text-[11px] font-mono text-[#00D2FF]">
                      R={(node.retentionScore * 100).toFixed(0)}%
                    </span>
                  </div>

                  <p className="mt-1.5 text-xs text-[#94A3B8] leading-relaxed">
                    {node.description}
                  </p>

                  {node.metricImpact && (
                    <div className="mt-2 text-[11px] font-mono text-[#10B981]">
                      ★ Impact: {node.metricImpact}
                    </div>
                  )}
                </div>

                {!isLast && (
                  <div className="flex justify-center my-1 text-[#00D2FF] font-mono text-xs animate-pulse">
                    ↓
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Right: Selected Node Detail Inspector (5 cols) */}
        <div className="lg:col-span-5">
          {activeNode ? (
            <div className="p-6 rounded-2xl bg-[#131D35] border border-[#334155] space-y-4 h-full flex flex-col justify-between">
              <div>
                <div className="border-b border-[#1E293B] pb-3">
                  <span className="text-[10px] text-[#64748B] uppercase font-mono block">
                    Causal Memory Inspector
                  </span>
                  <h3 className="text-sm font-bold text-[#F8FAFC] mt-0.5">
                    {activeNode.label}
                  </h3>
                </div>

                <div className="mt-4 space-y-3 text-xs">
                  <div>
                    <span className="text-[#64748B] uppercase font-mono text-[10px] block">
                      Node Type:
                    </span>
                    <span className="text-[#38BDF8] font-mono font-medium block mt-0.5">
                      {activeNode.nodeType}
                    </span>
                  </div>

                  <div>
                    <span className="text-[#64748B] uppercase font-mono text-[10px] block">
                      Causal Description:
                    </span>
                    <p className="text-[#F8FAFC] leading-relaxed mt-0.5">
                      {activeNode.description}
                    </p>
                  </div>

                  {activeNode.metricImpact && (
                    <div>
                      <span className="text-[#64748B] uppercase font-mono text-[10px] block">
                        Observed Metric Shift:
                      </span>
                      <span className="text-[#10B981] font-mono font-bold block mt-0.5">
                        {activeNode.metricImpact}
                      </span>
                    </div>
                  )}
                </div>
              </div>

              <div className="pt-4 border-t border-[#1E293B] flex items-center justify-between text-xs font-mono text-[#64748B]">
                <span>Retention Weight: {(activeNode.retentionScore * 100).toFixed(0)}%</span>
                <span className="text-[#10B981]">✓ Verified Link</span>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-xs text-[#64748B]">Select a node to inspect</div>
          )}
        </div>
      </CardContent>
    </div>
  );
};
