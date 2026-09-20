/**
 * Phase 13.16: Autonomous World Modeling, Predictive Intelligence & Causal Reasoning Platform (AWMPICRP)
 * View 10: Decision Intelligence Center
 */

import React, { useEffect, useState } from 'react';
import {
  CheckCircle2,
  RefreshCw,
  Briefcase,
  Zap,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { WorldModelApiClient } from '../../services/worldModelApiClient';
import { DecisionOption, DecisionPortfolio } from '../../types/worldModelPlatform';

export const DecisionIntelligenceCenter: React.FC = () => {
  const [options, setOptions] = useState<DecisionOption[]>([]);
  const [portfolios, setPortfolios] = useState<DecisionPortfolio[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchDecisions = async () => {
    setLoading(true);
    try {
      const res = await WorldModelApiClient.getDecisions();
      setOptions(res.options || []);
      setPortfolios(res.portfolios || []);
    } catch (err) {
      console.error('Error fetching decisions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDecisions();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/80 border border-emerald-500/30 rounded-xl p-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold text-white tracking-tight">Decision Intelligence Center</h1>
              <Badge variant="intelligence">Expected Utility Optimization</Badge>
            </div>
            <p className="text-sm text-slate-400">
              Evaluates candidate actions against probabilistic world states, ranking options by multi-objective Expected Utility.
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={fetchDecisions} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      {/* Portfolios & Options Grid */}
      <div className="space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <Briefcase className="w-5 h-5 text-emerald-400" />
          Recommended Decision Portfolios
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {portfolios.map((port) => (
            <Card key={port.portfolio_id} className="bg-slate-900/60 border-slate-800 p-5 space-y-4">
              <div className="flex items-start justify-between">
                <div>
                  <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                    {port.portfolio_id}
                  </span>
                  <h4 className="text-base font-bold text-white mt-1">{port.objective}</h4>
                </div>
                <Badge variant="success">Utility: {port.aggregate_utility}</Badge>
              </div>

              <div className="grid grid-cols-2 gap-2 text-xs">
                <div className="p-2.5 bg-slate-950/80 rounded border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">Risk Profile</span>
                  <span className="text-emerald-300 font-semibold uppercase">{port.risk_profile}</span>
                </div>
                <div className="p-2.5 bg-slate-950/80 rounded border border-slate-800">
                  <span className="text-slate-400 block text-[10px] uppercase">Estimated Cost</span>
                  <span className="text-white font-mono font-bold">${port.total_cost}k/mo</span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Evaluated Options */}
      <div className="space-y-4">
        <h3 className="text-base font-semibold text-white flex items-center gap-2">
          <Zap className="w-5 h-5 text-emerald-400" />
          Evaluated Candidate Decisions
        </h3>

        <div className="space-y-3">
          {options.map((opt) => (
            <Card key={opt.option_id} className="bg-slate-900/60 border-slate-800 p-5 space-y-3 hover:border-emerald-500/40 transition-all">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">
                      {opt.option_id}
                    </span>
                    <Badge variant="intelligence">{opt.risk_profile}</Badge>
                  </div>
                  <h4 className="text-base font-bold text-white mt-1.5">{opt.title}</h4>
                </div>
                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Expected Utility</span>
                  <span className="text-lg font-bold text-emerald-400">{opt.expected_utility}</span>
                </div>
              </div>

              <p className="text-sm text-slate-300">{opt.description}</p>

              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs pt-1">
                <div className="p-2 bg-slate-950/80 rounded border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Cost</span>
                  <span className="text-white font-bold font-mono">${opt.cost}k</span>
                </div>
                <div className="p-2 bg-slate-950/80 rounded border border-slate-800">
                  <span className="text-slate-400 block text-[10px]">Time Horizon</span>
                  <span className="text-slate-200 font-mono">{opt.time_horizon_seconds ? `${opt.time_horizon_seconds / 3600}h` : '4h'}</span>
                </div>
                <div className="p-2 bg-slate-950/80 rounded border border-slate-800 col-span-2">
                  <span className="text-slate-400 block text-[10px]">Actions Enqueued</span>
                  <span className="text-emerald-300 font-mono text-[11px] truncate block">
                    {JSON.stringify(opt.actions || [])}
                  </span>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
