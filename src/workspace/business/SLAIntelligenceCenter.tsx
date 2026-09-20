import React, { useState } from 'react';
import {
  ShieldAlert,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

export const SLAIntelligenceCenter: React.FC = () => {
  const [slaItems] = useState([
    {
      id: 'sla_inv_gold',
      process: 'End-to-End Enterprise Invoice Processing',
      target: '2h 00m',
      elapsed: '45m 12s',
      riskScore: 0.12,
      status: 'HEALTHY',
      escalationRole: 'role_finance_director',
    },
    {
      id: 'sla_vendor_kyc',
      process: 'Global Vendor Onboarding & AML Clearance',
      target: '24h 00m',
      elapsed: '20h 30m',
      riskScore: 0.88,
      status: 'ELEVATED_RISK',
      escalationRole: 'role_compliance_officer',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">SLA Intelligence & Breach Predictor</h1>
            <p className="text-sm text-slate-400">
              Proactive hazard modeling, turnaround deadline countdowns, and automated role escalations
            </p>
          </div>
        </div>
      </div>

      {/* SLA Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {slaItems.map((item) => (
          <Card key={item.id} className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-base font-bold text-white">{item.process}</h2>
                <span className="text-xs text-slate-400 font-mono">Contract: {item.id}</span>
              </div>
              <Badge variant={item.status === 'HEALTHY' ? 'success' : 'warning'}>
                {item.status}
              </Badge>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs font-mono">
              <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                <span className="text-slate-400 block text-[11px]">SLA Target</span>
                <span className="text-white font-bold text-sm">{item.target}</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                <span className="text-slate-400 block text-[11px]">Current Elapsed</span>
                <span className="text-indigo-300 font-bold text-sm">{item.elapsed}</span>
              </div>
            </div>

            {/* Risk Gauge */}
            <div>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400">Breach Hazard Probability</span>
                <span className="font-mono font-bold text-amber-400">{(item.riskScore * 100).toFixed(0)}%</span>
              </div>
              <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all ${
                    item.riskScore > 0.5 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${item.riskScore * 100}%` }}
                />
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center">
              <span>Auto-Escalation Target:</span>
              <span className="font-mono text-cyan-300">{item.escalationRole}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
