import React, { useState, useEffect } from 'react';
import { Zap, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { OptimizationOpportunity } from '../../types/cognitive';

export const AutonomousOptimizationCenter: React.FC = () => {
  const [opportunities, setOpportunities] = useState<OptimizationOpportunity[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.listOptimizations();
    setOpportunities(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleApply = async (id: string) => {
    await cognitiveApiClient.applyOptimization(id);
    await loadData();
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Zap className="w-7 h-7 text-indigo-400" />
            Autonomous Optimization Center
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Continuous auto-tuning of model routing, prompt templates, concurrency pools, and embedding caches.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {opportunities.map((opt) => (
          <Card key={opt.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
            <div className="flex justify-between items-center">
              <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                {opt.subsystem}
              </Badge>
              <Badge variant={opt.status === 'APPLIED' ? 'success' : 'info'}>
                {opt.status}
              </Badge>
            </div>
            <h3 className="text-base font-semibold text-slate-200">{opt.recommended_change}</h3>
            <div className="p-3 bg-slate-800/40 rounded border border-slate-700/60 flex justify-between items-center text-xs">
              <span className="text-slate-400">Target: {opt.target_resource}</span>
              <span className="text-emerald-400 font-mono font-bold">+${opt.projected_savings_monthly_usd}/mo savings</span>
            </div>
            <div className="pt-2 flex justify-end">
              <Button
                variant="intelligence"
                size="sm"
                disabled={opt.status === 'APPLIED'}
                onClick={() => handleApply(opt.id)}
              >
                {opt.status === 'APPLIED' ? 'Applied' : 'Execute Auto-Tune'}
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
