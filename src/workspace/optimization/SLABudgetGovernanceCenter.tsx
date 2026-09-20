import React, { useState } from 'react';
import {
  ShieldAlert,
  Clock,
  DollarSign,
  AlertTriangle,
  CheckCircle2,
  Lock,
  PieChart,
  RefreshCw,
  Scale
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface SLABudgetGovernanceCenterProps {
  missionId?: string;
}

export const SLABudgetGovernanceCenter: React.FC<SLABudgetGovernanceCenterProps> = ({
  missionId = 'mission-current',
}) => {
  const [budgetCap, setBudgetCap] = useState<number>(0.15);
  const [currentSpend] = useState<number>(0.042);
  const [deadlineMs, setDeadlineMs] = useState<number>(5000);
  const [currentLatency] = useState<number>(1420);
  const [penaltyPerSecLate] = useState<number>(0.05);

  const budgetUtilization = (currentSpend / budgetCap) * 100;
  const timeUtilization = (currentLatency / deadlineMs) * 100;

  const policies = [
    {
      id: 'POL-SLA-01',
      name: 'Hard Budget Kill-Switch',
      rule: 'Spend <= $0.150 per document payload',
      status: 'ENFORCED',
      violationCount: 0,
      severity: 'CRITICAL',
    },
    {
      id: 'POL-SLA-02',
      name: 'P99 Latency SLA Bound',
      rule: 'Total Mission Duration <= 5,000 ms',
      status: 'HEALTHY',
      violationCount: 0,
      severity: 'HIGH',
    },
    {
      id: 'POL-SLA-03',
      name: 'Scientific Confidence Floor',
      rule: 'Consensus Confidence >= 92.0%',
      status: 'HEALTHY',
      violationCount: 0,
      severity: 'CRITICAL',
    },
    {
      id: 'POL-SLA-04',
      name: 'Adaptive Fallback on Rate-Limit',
      rule: 'Switch to local Quantized LLM on 429 error > 2 retries',
      status: 'ACTIVE_GUARD',
      violationCount: 1,
      severity: 'MEDIUM',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-emerald-400" />
            SLA & Financial Budget Governance Center
          </h2>
          <p className="text-sm text-slate-400">
            Real-time enforcement of hard budgets, deadline SLAs, degradation penalties, and compliance guards for mission: <code className="text-emerald-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            SLA Guard: ACTIVE & COMPLIANT
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Sync Ledger
          </button>
        </div>
      </div>

      {/* Primary KPI Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Financial Spend Envelope</span>
            <DollarSign className="w-4 h-4 text-emerald-400" />
          </div>
          <div className="text-2xl font-bold text-emerald-400 font-mono">
            ${currentSpend.toFixed(3)}
            <span className="text-xs text-slate-400 font-normal"> / ${budgetCap.toFixed(3)}</span>
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${
                budgetUtilization > 85 ? 'bg-rose-500' : budgetUtilization > 65 ? 'bg-amber-500' : 'bg-emerald-500'
              }`}
              style={{ width: `${Math.min(100, budgetUtilization)}%` }}
            />
          </div>
          <span className="text-[10px] text-slate-400 mt-1 block">{budgetUtilization.toFixed(1)}% consumed</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Turnaround SLA Deadline</span>
            <Clock className="w-4 h-4 text-amber-400" />
          </div>
          <div className="text-2xl font-bold text-amber-400 font-mono">
            {currentLatency}ms
            <span className="text-xs text-slate-400 font-normal"> / {deadlineMs}ms</span>
          </div>
          <div className="mt-2 w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full ${
                timeUtilization > 85 ? 'bg-rose-500' : timeUtilization > 65 ? 'bg-amber-500' : 'bg-amber-500'
              }`}
              style={{ width: `${Math.min(100, timeUtilization)}%` }}
            />
          </div>
          <span className="text-[10px] text-slate-400 mt-1 block">{(deadlineMs - currentLatency)}ms headroom</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Late Penalty Risk</span>
            <AlertTriangle className="w-4 h-4 text-purple-400" />
          </div>
          <div className="text-2xl font-bold text-purple-400 font-mono">
            $0.000
          </div>
          <p className="text-[11px] text-slate-400 mt-2">Rate: ${penaltyPerSecLate.toFixed(2)} / sec overrun</p>
          <span className="text-[10px] text-emerald-400 mt-1 block">0 violations recorded</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-medium text-slate-400">Enforcement Lock</span>
            <Lock className="w-4 h-4 text-indigo-400" />
          </div>
          <div className="text-lg font-bold text-indigo-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            STRICT_ZERO_TOLERANCE
          </div>
          <p className="text-[11px] text-slate-400 mt-2">Auto-abort on budget overrun</p>
          <span className="text-[10px] text-slate-500 mt-1 block">Cryptographically Signed Policy</span>
        </Card>
      </div>

      {/* Budget & SLA Threshold Adjuster & Governance Rules */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-4">
          <Card className="p-5 bg-slate-900 border-slate-800 space-y-4">
            <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
              <Scale className="w-4 h-4 text-indigo-400" />
              Runtime Envelope Governors
            </h3>

            <div className="space-y-3">
              <div>
                <label className="text-xs text-slate-400 flex justify-between mb-1">
                  <span>Max Budget Cap (USD)</span>
                  <span className="text-emerald-400 font-mono font-bold">${budgetCap.toFixed(3)}</span>
                </label>
                <input
                  type="range"
                  min="0.02"
                  max="0.50"
                  step="0.01"
                  value={budgetCap}
                  onChange={(e) => setBudgetCap(parseFloat(e.target.value))}
                  className="w-full accent-emerald-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg appearance-none"
                />
              </div>

              <div>
                <label className="text-xs text-slate-400 flex justify-between mb-1">
                  <span>SLA Max Turnaround (ms)</span>
                  <span className="text-amber-400 font-mono font-bold">{deadlineMs} ms</span>
                </label>
                <input
                  type="range"
                  min="1000"
                  max="15000"
                  step="500"
                  value={deadlineMs}
                  onChange={(e) => setDeadlineMs(parseInt(e.target.value))}
                  className="w-full accent-amber-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg appearance-none"
                />
              </div>

              <div className="p-3 rounded-lg bg-slate-950 border border-slate-800 text-xs space-y-1.5">
                <div className="flex justify-between text-slate-400">
                  <span>Calculated Target Throughput:</span>
                  <span className="text-slate-200 font-mono">{(1000 / (currentLatency || 1)).toFixed(1)} doc/s</span>
                </div>
                <div className="flex justify-between text-slate-400">
                  <span>Projected 10k Run Cost:</span>
                  <span className="text-emerald-400 font-mono">${(currentSpend * 10000).toFixed(2)}</span>
                </div>
              </div>
            </div>
          </Card>
        </div>

        <div className="lg:col-span-2">
          <Card className="p-5 bg-slate-900 border-slate-800">
            <h3 className="text-sm font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <PieChart className="w-4 h-4 text-purple-400" />
              Active SLA Enforcement Policies & Invariant Guardrails
            </h3>

            <div className="space-y-3">
              {policies.map(pol => (
                <div key={pol.id} className="p-3.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-mono text-indigo-400">{pol.id}</span>
                      <span className="text-xs font-semibold text-slate-200">{pol.name}</span>
                      <Badge variant={pol.severity === 'CRITICAL' ? 'error' : 'warning'} size="sm">
                        {pol.severity}
                      </Badge>
                    </div>
                    <p className="text-[11px] text-slate-400 font-mono">{pol.rule}</p>
                  </div>
                  <div className="text-right">
                    <Badge variant={pol.status === 'HEALTHY' || pol.status === 'ENFORCED' ? 'success' : 'warning'} size="sm">
                      {pol.status}
                    </Badge>
                    <span className="text-[10px] text-slate-500 block mt-1">
                      {pol.violationCount} Violations
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
