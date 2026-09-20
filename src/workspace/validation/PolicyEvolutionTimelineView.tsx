import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PolicyEvolutionTimelineView: React.FC = () => {
  const [policies, setPolicies] = useState([
    {
      id: 'pol_v5_0_cand',
      version: 'v5.0.0-candidate',
      name: 'Bayesian Multi-Objective Prior Optimization',
      stage: 'CANARY_STAGING',
      parameters: {
        weight_accuracy: 0.40,
        weight_latency: 0.20,
        weight_cost: 0.40,
        confidence_threshold: 0.88,
      },
      provenanceHash: '8b4d9e201a4f3312',
      deployedAt: '2 hours ago',
    },
    {
      id: 'pol_v4_2',
      version: 'v4.2.0',
      name: 'Baseline Balanced Pareto Optimization',
      stage: 'PRODUCTION',
      parameters: {
        weight_accuracy: 0.45,
        weight_latency: 0.25,
        weight_cost: 0.30,
        confidence_threshold: 0.85,
      },
      provenanceHash: 'a1f89c44b3e21098',
      deployedAt: '5 days ago',
    },
    {
      id: 'pol_v4_1',
      version: 'v4.1.0',
      name: 'Conservative High-Confidence Router',
      stage: 'RETIRED',
      parameters: {
        weight_accuracy: 0.60,
        weight_latency: 0.20,
        weight_cost: 0.20,
        confidence_threshold: 0.90,
      },
      provenanceHash: '3c19e598fa201b55',
      deployedAt: '2 weeks ago',
    },
  ]);

  const [rollbackLog, setRollbackLog] = useState<string[]>([]);

  const handleInstantRollback = (policyId: string) => {
    setPolicies((prev) =>
      prev.map((p) => {
        if (p.id === policyId) return { ...p, stage: 'ROLLED_BACK' };
        if (p.id === 'pol_v4_2') return { ...p, stage: 'PRODUCTION' };
        return p;
      })
    );
    setRollbackLog((prev) => [
      `[${new Date().toLocaleTimeString()}] Instant atomic rollback executed: ${policyId} reverted to safe baseline pol_v4_2.`,
      ...prev,
    ]);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🧬</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Policy Self-Evolution & Instant Rollback Timeline
              </h2>
              <Badge variant="success" size="sm">
                ATOMIC ROLLBACK READY
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Versioned policy state machine (Draft → Shadow → Canary → Production) with instant rollback governance.
            </p>
          </div>
        </div>
      </div>

      {/* Policy State Machine Cards */}
      <div className="space-y-4">
        {policies.map((p) => (
          <Card key={p.id} className="p-6 bg-[#0F172A] border-[#1E293B]">
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-mono text-cyan-400 font-bold">{p.version}</span>
                  <h3 className="text-sm font-bold font-mono text-[#F8FAFC]">{p.name}</h3>
                </div>
                <div className="text-xs font-mono text-[#64748B] mt-1">
                  SHA256 Provenance: {p.provenanceHash} • Deployed: {p.deployedAt}
                </div>
              </div>
              <div className="flex items-center gap-3">
                <Badge
                  variant={
                    p.stage === 'PRODUCTION'
                      ? 'success'
                      : p.stage === 'CANARY_STAGING'
                      ? 'info'
                      : p.stage === 'ROLLED_BACK'
                      ? 'error'
                      : 'default'
                  }
                  size="sm"
                >
                  {p.stage}
                </Badge>
                {p.stage === 'CANARY_STAGING' && (
                  <button
                    onClick={() => handleInstantRollback(p.id)}
                    className="px-3 py-1.5 rounded-lg text-xs font-mono font-bold bg-rose-600/20 border border-rose-500 text-rose-300 hover:bg-rose-600 hover:text-white transition-all shadow-md"
                  >
                    ⚡ INSTANT ROLLBACK
                  </button>
                )}
              </div>
            </div>

            {/* Parameter Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mt-4 pt-3 border-t border-[#1E293B]">
              <div className="p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs">
                <div className="text-[#94A3B8]">Weight Accuracy (w_acc):</div>
                <div className="text-cyan-400 font-bold mt-0.5">{p.parameters.weight_accuracy}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs">
                <div className="text-[#94A3B8]">Weight Latency (w_lat):</div>
                <div className="text-indigo-400 font-bold mt-0.5">{p.parameters.weight_latency}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs">
                <div className="text-[#94A3B8]">Weight Cost (w_cost):</div>
                <div className="text-emerald-400 font-bold mt-0.5">{p.parameters.weight_cost}</div>
              </div>
              <div className="p-2.5 rounded-lg bg-[#020617] border border-[#1E293B] font-mono text-xs">
                <div className="text-[#94A3B8]">Confidence Threshold:</div>
                <div className="text-[#F8FAFC] font-bold mt-0.5">{p.parameters.confidence_threshold}</div>
              </div>
            </div>
          </Card>
        ))}
      </div>

      {/* Rollback Audit Stream */}
      {rollbackLog.length > 0 && (
        <Card className="p-4 bg-rose-950/20 border-rose-900/50">
          <h4 className="text-xs font-bold font-mono text-rose-300 mb-2">⚡ Rollback Audit Log</h4>
          <div className="space-y-1 font-mono text-[11px] text-rose-200">
            {rollbackLog.map((log, i) => (
              <div key={i}>{log}</div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};
