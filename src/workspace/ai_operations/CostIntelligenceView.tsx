import React, { useState, useEffect } from 'react';
import {
  DollarSign,
  TrendingDown,
  PieChart,
  Lightbulb,
  Zap,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';

export const CostIntelligenceView: React.FC = () => {
  const [costData, setCostData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadCostData = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getCostAnalytics();
      setCostData(data);
    } catch (err) {
      console.error('Failed to load cost analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCostData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
            <DollarSign className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Cost & Token Intelligence</h1>
            <p className="text-xs text-slate-400">Token burn analytics, model tier spend breakdown, and savings recommendations</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadCostData} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Current Spend</span>
            <DollarSign className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-2">
            <span className="text-3xl font-bold text-white">${costData?.total_cost_usd ?? 0.0}</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">{(costData?.total_tokens_consumed ?? 0).toLocaleString()} tokens processed</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Projected Monthly</span>
            <TrendingDown className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="mt-2">
            <span className="text-3xl font-bold text-white">${costData?.projected_monthly_spend_usd ?? 0.0}</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Based on trailing 24h consumption</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Optimization Potential</span>
            <Zap className="w-5 h-5 text-amber-400" />
          </div>
          <div className="mt-2">
            <span className="text-3xl font-bold text-amber-300">~25-35%</span>
          </div>
          <p className="mt-1 text-xs text-slate-500">Via prompt caching & tier routing</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Model Tier Spend Breakdown */}
        <Card className="p-6 bg-slate-900/50 border-slate-800">
          <h2 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
            <PieChart className="w-4 h-4 text-emerald-400" /> Spend by Model Tier
          </h2>
          <div className="space-y-3">
            {costData?.cost_by_model &&
              Object.entries(costData.cost_by_model).map(([model, cost]: [string, any]) => (
                <div key={model} className="p-3 bg-slate-950/60 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between text-xs mb-1">
                    <span className="font-semibold text-slate-200">{model}</span>
                    <span className="font-mono text-emerald-400">${cost}</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-emerald-400 h-full rounded-full"
                      style={{
                        width: `${Math.min(100, (cost / Math.max(0.01, costData.total_cost_usd)) * 100)}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
          </div>
        </Card>

        {/* Savings Recommendations */}
        <Card className="p-6 bg-slate-900/50 border-slate-800">
          <h2 className="text-base font-semibold text-white mb-4 flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-amber-400" /> AI Cost Optimization Recommendations
          </h2>
          <div className="space-y-3">
            {costData?.savings_recommendations?.map((rec: any) => (
              <div key={rec.recommendation_id} className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold text-white text-xs">{rec.title}</h3>
                  <Badge variant="success">Save ${rec.potential_monthly_savings_usd}/mo</Badge>
                </div>
                <div className="flex items-center justify-between mt-2.5 text-xs text-slate-400">
                  <span>Confidence: {(rec.confidence * 100).toFixed(0)}%</span>
                  <span className="text-emerald-400 font-semibold">{rec.savings_pct}% Reduction</span>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
