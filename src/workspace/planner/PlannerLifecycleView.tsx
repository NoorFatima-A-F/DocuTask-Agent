import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { GitBranch, ShieldCheck } from 'lucide-react';

export const PlannerLifecycleView: React.FC = () => {
  const [selectedState, setSelectedState] = useState<string>('EXECUTING');

  const lifecycleStages = [
    { state: 'CREATED', phase: 'INITIAL', status: 'COMPLETED', time: '14:20:00.120', desc: 'Planner instance instantiated with correlation token.' },
    { state: 'INITIALIZING', phase: 'INITIAL', status: 'COMPLETED', time: '14:20:00.180', desc: 'Loaded runtime configurations and execution quotas.' },
    { state: 'CONTEXT_LOADING', phase: 'CONTEXT', status: 'COMPLETED', time: '14:20:00.220', desc: 'Fetched mission prompt and attached PDF document handles.' },
    { state: 'MEMORY_SEARCH', phase: 'CONTEXT', status: 'COMPLETED', time: '14:20:00.280', desc: 'Retrieved 3 historical invoice DAG templates from memory graph.' },
    { state: 'CAPABILITY_DISCOVERY', phase: 'DISCOVERY', status: 'COMPLETED', time: '14:20:00.310', desc: 'Discovered 6 active worker types (OCR, Schema, Validator, Ledger).' },
    { state: 'GOAL_ANALYSIS', phase: 'REASONING', status: 'COMPLETED', time: '14:20:00.350', desc: 'Extracted SLA constraint (30s) and financial arithmetic invariant.' },
    { state: 'PLAN_SYNTHESIS', phase: 'REASONING', status: 'COMPLETED', time: '14:20:00.420', desc: 'Generated multi-stage topology with parallel raster chunks.' },
    { state: 'TASK_DECOMPOSITION', phase: 'DAG_BUILD', status: 'COMPLETED', time: '14:20:00.510', desc: 'Decomposed goal into 9 typed execution task nodes.' },
    { state: 'DEPENDENCY_ANALYSIS', phase: 'DAG_BUILD', status: 'COMPLETED', time: '14:20:00.600', desc: 'Computed critical path (425ms) and topological dependencies.' },
    { state: 'WORKER_ASSIGNMENT', phase: 'DISPATCH', status: 'COMPLETED', time: '14:20:00.720', desc: 'Matched tasks to optimal worker capabilities.' },
    { state: 'READY', phase: 'DISPATCH', status: 'COMPLETED', time: '14:20:00.890', desc: 'Execution DAG validated and locked into runtime state.' },
    { state: 'EXECUTING', phase: 'RUNTIME', status: 'ACTIVE', time: '14:20:01.100', desc: 'Wavefront 1 & 2 dispatched and running across worker pool.' },
    { state: 'REPLANNING', phase: 'RESILIENCE', status: 'STANDBY', time: '---', desc: 'Autonomous recovery trigger ready upon invariant or failure signal.' },
    { state: 'COMPLETED', phase: 'FINAL', status: 'PENDING', time: '---', desc: 'Mission objective satisfied and truth ledger committed.' },
    { state: 'FAILED', phase: 'FINAL', status: 'STANDBY', time: '---', desc: 'Terminal failure containment circuit.' },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-indigo-500/20 to-blue-500/20 border border-indigo-500/30 rounded-xl text-indigo-400">
              <GitBranch className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Autonomous Planner 14-State Lifecycle Engine
                <Badge variant="success" size="sm">Phase 13.2 Live</Badge>
              </h1>
              <p className="text-xs text-[#94A3B8] font-mono">
                Observable state machine driven exclusively by immutable Phase 13.1 domain events
              </p>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 font-mono text-xs">
          <span className="text-[#94A3B8]">Active State:</span>
          <Badge variant="intelligence" size="md">EXECUTING (Wavefront 2)</Badge>
        </div>
      </div>

      {/* 14-State Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">
        {lifecycleStages.map((stage, idx) => {
          const isSelected = selectedState === stage.state;
          const isCompleted = stage.status === 'COMPLETED';
          const isActive = stage.status === 'ACTIVE';

          return (
            <Card
              key={stage.state}
              className={`p-3.5 rounded-xl border transition-all cursor-pointer ${
                isSelected
                  ? 'border-indigo-500 bg-[#131D35] shadow-[0_0_15px_rgba(99,102,241,0.25)]'
                  : isActive
                  ? 'border-cyan-500/50 bg-[#0F172A]'
                  : isCompleted
                  ? 'border-emerald-500/30 bg-[#0F172A]/70'
                  : 'border-[#1E293B] bg-[#0A0F1D]/50 opacity-60'
              }`}
              onClick={() => setSelectedState(stage.state)}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono text-[#64748B]">STEP {idx + 1}</span>
                <Badge
                  variant={isActive ? 'intelligence' : isCompleted ? 'success' : 'outline'}
                  size="sm"
                >
                  {stage.status}
                </Badge>
              </div>

              <div className="text-xs font-mono font-bold text-white mb-1">{stage.state}</div>
              <div className="text-[11px] text-[#94A3B8] line-clamp-2 mb-2">{stage.desc}</div>

              <div className="text-[10px] font-mono text-[#64748B] flex items-center justify-between pt-2 border-t border-[#1E293B]">
                <span>{stage.phase}</span>
                <span>{stage.time}</span>
              </div>
            </Card>
          );
        })}
      </div>

      {/* Selected State Provenance Inspector */}
      <Card className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4 font-mono">
        <div className="flex items-center justify-between border-b border-[#1E293B] pb-3">
          <div className="flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-cyan-400" />
            <h3 className="text-sm font-semibold text-white">
              State Detail & Cryptographic Provenance: {selectedState}
            </h3>
          </div>
          <Badge variant="info" size="sm">Deterministic Runtime Event</Badge>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
          <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
            <span className="text-[#64748B] block text-[10px]">CORRESPONDING EVENT TYPE</span>
            <span className="text-white font-bold">PlannerStateChanged</span>
          </div>
          <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
            <span className="text-[#64748B] block text-[10px]">EVENT ID</span>
            <span className="text-cyan-400 font-bold">evt-state-{selectedState.toLowerCase()}-01</span>
          </div>
          <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
            <span className="text-[#64748B] block text-[10px]">TRUTH LEDGER COMMIT</span>
            <span className="text-emerald-400 font-bold">hash-state-verified-c8a1</span>
          </div>
          <div className="p-3 bg-[#131D35] rounded-xl border border-[#1E293B]">
            <span className="text-[#64748B] block text-[10px]">REPLAY STREAM OFFSET</span>
            <span className="text-purple-400 font-bold">Offset #04</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
