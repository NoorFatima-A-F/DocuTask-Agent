import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { workforceApiClient } from '../../services/workforceApiClient';
import { EconomicResourceBudget } from '../../types/workforce';

export const ResourceEconomyDashboard: React.FC = () => {
  const [econ, setEcon] = useState<EconomicResourceBudget | null>(null);

  useEffect(() => {
    workforceApiClient.getEconomics().then(setEcon);
  }, []);

  return (
    <div className="space-y-6">
      <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <h1 className="text-2xl font-bold text-white flex items-center gap-3">
          <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-xl">💰</span>
          Resource Economy & Budget Allocation
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Compute (GPU/CPU), Token Consumption, and Enterprise Value Return
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Total Budget (USD)</div>
          <div className="text-2xl font-bold text-white mt-1">${(econ?.total_budget_usd ?? 35000).toLocaleString()}</div>
          <div className="text-xs text-emerald-400 mt-1">Spent: ${(econ?.total_spent_usd ?? 18250).toLocaleString()}</div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">GPU Hours Used</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{econ?.used_gpu_hours ?? 1140} hrs</div>
          <div className="text-xs text-slate-400 mt-1">of {econ?.allocated_gpu_hours ?? 2000} hrs</div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Token Pool</div>
          <div className="text-2xl font-bold text-purple-400 mt-1">{((econ?.used_tokens ?? 540000000) / 1e6).toFixed(0)}M</div>
          <div className="text-xs text-slate-400 mt-1">of {((econ?.allocated_tokens ?? 1000000000) / 1e6).toFixed(0)}M tokens</div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <div className="text-xs text-slate-400 font-semibold uppercase">Value Multiplier (ROI)</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{econ?.efficiency_roi_ratio ?? 5.4}x</div>
          <div className="text-xs text-slate-400 mt-1">Net Productivity Gain</div>
        </Card>
      </div>

      <Card className="p-5 bg-slate-900/50 border-slate-800">
        <h3 className="text-base font-bold text-white mb-3">Autonomous Reallocation Directives</h3>
        <ul className="space-y-2">
          {(econ?.reallocation_recommendations ?? []).map((r, idx) => (
            <li key={idx} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800 text-xs text-slate-300 flex items-center gap-2">
              <span className="text-emerald-400 font-bold">⚡</span> {r}
            </li>
          ))}
        </ul>
      </Card>
    </div>
  );
};
