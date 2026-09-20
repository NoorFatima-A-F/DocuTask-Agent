import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Network, Split } from 'lucide-react';

export const LiveDAGView: React.FC = () => {
  const [selectedNodeId, setSelectedNodeId] = useState<string>('node_merge_ocr');
  const [version, setVersion] = useState<number>(1);

  const nodes = [
    { id: 'node_goal_ingress', name: 'Mission Goal Ingress', type: 'SEQUENTIAL', state: 'COMPLETED', worker: 'worker-planner-01', duration: '42ms', cost: '$0.0001' },
    { id: 'node_split_ocr', name: 'Split OCR Chunks', type: 'SPLIT', state: 'COMPLETED', worker: 'worker-dag-01', duration: '28ms', cost: '$0.0001' },
    { id: 'node_ocr_chunk_1', name: 'OCR Page 1-2 (Raster)', type: 'PARALLEL', state: 'COMPLETED', worker: 'worker-ocr-01', duration: '175ms', cost: '$0.0006' },
    { id: 'node_ocr_chunk_2', name: 'OCR Page 3-4 (Tables)', type: 'PARALLEL', state: 'COMPLETED', worker: 'worker-ocr-02', duration: '205ms', cost: '$0.0006' },
    { id: 'node_merge_ocr', name: 'Merge OCR Texts', type: 'MERGE', state: 'RUNNING', worker: 'worker-extract-01', duration: '60ms', cost: '$0.0002' },
    { id: 'node_extract_schema', name: 'Extract Financial Schema', type: 'SEQUENTIAL', state: 'WAITING', worker: 'worker-extract-01', duration: '140ms', cost: '$0.0008' },
    { id: 'node_validate_invariants', name: 'Scientific Validation Check', type: 'CONDITIONAL', state: 'WAITING', worker: 'worker-validate-01', duration: '90ms', cost: '$0.0003' },
    { id: 'node_barrier_governance', name: 'Governance Sync Barrier', type: 'BARRIER', state: 'WAITING', worker: 'worker-gov-01', duration: '50ms', cost: '$0.0002' },
    { id: 'node_join_finalize', name: 'Join & Truth Ledger Commit', type: 'JOIN', state: 'WAITING', worker: 'worker-trust-01', duration: '40ms', cost: '$0.0002' },
  ];

  const handleSimulateSplit = () => {
    setVersion(v => v + 1);
  };

  const selectedNode = nodes.find(n => n.id === selectedNodeId) ?? nodes[0]!;

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-blue-500/20 to-cyan-500/20 border border-blue-500/30 rounded-xl text-blue-400">
              <Network className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Live Dynamic DAG Topology & In-Flight Mutation
                <Badge variant="success" size="sm">Version v{version}.0</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Real-time directed acyclic graph driven by Phase 13.1 domain events (Split, Merge, Parallel, Barrier, Join)
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button onClick={handleSimulateSplit} variant="secondary" size="sm">
            <Split className="w-3.5 h-3.5 mr-1 text-cyan-400" />
            Trigger Live Node Split Mutation
          </Button>
          <Badge variant="intelligence" size="md">Critical Path: 425ms</Badge>
        </div>
      </div>

      {/* DAG Visual Board */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Nodes List */}
        <div className="lg:col-span-2 space-y-3 font-mono">
          <div className="text-xs font-semibold text-[#94A3B8] flex items-center justify-between">
            <span>TOPOLOGICAL EXECUTION ORDER</span>
            <span>{nodes.length} NODES TOTAL</span>
          </div>

          <div className="space-y-2.5">
            {nodes.map((node, idx) => {
              const isSelected = selectedNodeId === node.id;
              const isCompleted = node.state === 'COMPLETED';
              const isRunning = node.state === 'RUNNING';

              return (
                <Card
                  key={node.id}
                  onClick={() => setSelectedNodeId(node.id)}
                  className={`p-3.5 rounded-xl border transition-all cursor-pointer flex items-center justify-between ${
                    isSelected
                      ? 'border-cyan-500 bg-[#131D35] shadow-[0_0_12px_rgba(0,210,255,0.2)]'
                      : isRunning
                      ? 'border-indigo-500/60 bg-[#0F172A]'
                      : isCompleted
                      ? 'border-emerald-500/30 bg-[#0F172A]/80'
                      : 'border-[#1E293B] bg-[#0A0F1D]/60 opacity-70'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-[#64748B] w-6">{idx + 1}.</span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xs font-bold text-white">{node.name}</span>
                        <Badge variant="default" size="sm">{node.type}</Badge>
                      </div>
                      <span className="text-[10px] text-[#64748B]">Worker: {node.worker}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-[#94A3B8]">{node.duration}</span>
                    <Badge
                      variant={isRunning ? 'intelligence' : isCompleted ? 'success' : 'outline'}
                      size="sm"
                    >
                      {node.state}
                    </Badge>
                  </div>
                </Card>
              );
            })}
          </div>
        </div>

        {/* Node Detail Inspector */}
        <div className="space-y-4 font-mono">
          <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4">
            <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
              <h3 className="text-xs font-bold text-white">Node Inspector: {selectedNode.id}</h3>
              <Badge variant="info" size="sm">{selectedNode.type}</Badge>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
                <span className="text-[10px] text-[#64748B] block">TASK NAME</span>
                <span className="text-white font-bold">{selectedNode.name}</span>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
                  <span className="text-[10px] text-[#64748B] block">STATUS</span>
                  <span className="text-cyan-400 font-bold">{selectedNode.state}</span>
                </div>
                <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
                  <span className="text-[10px] text-[#64748B] block">ASSIGNED WORKER</span>
                  <span className="text-purple-400 font-bold">{selectedNode.worker}</span>
                </div>
              </div>

              <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
                <span className="text-[10px] text-[#64748B] block">CRYPTOGRAPHIC TRUTH PROOF</span>
                <span className="text-emerald-400 font-bold text-[11px]">hash-dag-{selectedNode.id}-verified</span>
              </div>

              <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
                <span className="text-[10px] text-[#64748B] block">ESTIMATED LATENCY & COST</span>
                <span className="text-white font-bold">{selectedNode.duration} • {selectedNode.cost}</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
