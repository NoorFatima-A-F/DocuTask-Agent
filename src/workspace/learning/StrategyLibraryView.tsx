import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Layers, CheckCircle2, ShieldCheck } from 'lucide-react';

export const StrategyLibraryView: React.FC = () => {
  const strategies = [
    {
      id: 'strat-001',
      name: 'Dynamic High-Throughput Wavefront Strategy',
      goalType: 'DYNAMIC_EXTRACTION',
      gain: '+26.4%',
      version: '1.2.0',
      status: 'ACTIVE_IN_PRODUCTION',
      tactics: [
        'Concurrent OCR Sharding (4 workers)',
        'Pre-verification Schema Invariance Checks',
        'Exponential Retry with 250ms Base Backoff',
      ],
      applicableGoals: ['EXTRACTION', 'OCR', 'SCHEMA_MAPPING'],
    },
    {
      id: 'strat-002',
      name: 'SMT-Gated High-Assurance Reasoning Strategy',
      goalType: 'VERIFICATION_AND_REASONING',
      gain: '100% Invariance',
      version: '1.0.0',
      status: 'ACTIVE_IN_PRODUCTION',
      tactics: [
        'Multi-agent cross validation referee',
        'Z3 Symbolic SMT constraint proving',
        'Cryptographic truth ledger anchor before output',
      ],
      applicableGoals: ['REASONING', 'VALIDATION', 'LEGAL_AUDIT'],
    },
    {
      id: 'strat-003',
      name: 'Low-Latency Jittered Throttle Recovery Strategy',
      goalType: 'RESILIENCE_AND_RECOVERY',
      gain: '0% Task Loss',
      version: '1.1.0',
      status: 'ACTIVE_IN_PRODUCTION',
      tactics: [
        'Adaptive sliding rate-limit throttle monitoring',
        'Automatic task rerouting to secondary worker pool',
        'Circuit breaker tripped after 3 consecutive failures',
      ],
      applicableGoals: ['WORKER_EXECUTION', 'API_DISPATCH', 'RETRY'],
    },
  ];

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30 rounded-xl text-amber-400">
            <Layers className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Autonomous Execution Strategy Library
              <Badge variant="intelligence" size="sm">Phase 13.5</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Reusable, high-utility execution templates synthesized from empirical reflections and validated by governance
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">3 Active Strategies</Badge>
        </div>
      </div>

      {/* Strategy Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 font-mono">
        {strategies.map((strat) => (
          <Card key={strat.id} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <Badge variant="intelligence" size="sm">{strat.goalType}</Badge>
                <Badge variant="outline" size="sm">v{strat.version}</Badge>
              </div>

              <div>
                <h3 className="text-sm font-bold text-white">{strat.name}</h3>
                <span className="text-emerald-400 text-xs font-bold block mt-1">Expected Gain: {strat.gain}</span>
              </div>

              {/* Tactics list */}
              <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl space-y-2 text-xs">
                <span className="text-[10px] text-[#64748B] block font-bold">PRESCRIBED TACTICS:</span>
                {strat.tactics.map((tactic, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-[#94A3B8]">
                    <CheckCircle2 className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
                    <span>{tactic}</span>
                  </div>
                ))}
              </div>

              {/* Applicable Goal Types */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                {strat.applicableGoals.map((g, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 rounded text-[10px]">
                    {g}
                  </span>
                ))}
              </div>
            </div>

            <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs">
              <span className="text-emerald-400 font-bold flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5" />
                {strat.status}
              </span>
              <span className="text-[11px] text-[#64748B]">ID: {strat.id}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
