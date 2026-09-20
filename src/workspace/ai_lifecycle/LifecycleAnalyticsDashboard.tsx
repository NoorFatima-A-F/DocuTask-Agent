import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentAnalytics } from '../../types/aiLifecycle';
import { BarChart3, TrendingUp, DollarSign, Clock, RefreshCw } from 'lucide-react';

export const LifecycleAnalyticsDashboard: React.FC = () => {
  const [analytics, setAnalytics] = useState<AgentAnalytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const data = await AILifecycleApiClient.getAnalytics('agt_acme_invoice_reconciler');
      setAnalytics(data);
      setLoading(false);
    };
    load();
  }, []);

  if (loading || !analytics) {
    return (
      <div className="p-12 text-center text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Analytics...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <BarChart3 className="w-7 h-7 text-indigo-400" />
            AI Application Business ROI & Fleet Analytics
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Quantified financial ROI in USD, developer hours saved, adoption metrics, and success rates.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-emerald-950/60 text-emerald-400 rounded-lg">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">Automation ROI</span>
              <span className="text-2xl font-bold text-white">${analytics.automation_roi_usd.toLocaleString()}</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-indigo-950/60 text-indigo-400 rounded-lg">
              <Clock className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">Developer Hours Saved</span>
              <span className="text-2xl font-bold text-white">{analytics.developer_hours_saved} Hours</span>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-cyan-950/60 text-cyan-400 rounded-lg">
              <TrendingUp className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">Enterprise Adoption</span>
              <span className="text-2xl font-bold text-cyan-400">{analytics.adoption_score}%</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white">Execution Reliability Breakdown</CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="p-4 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between">
            <span className="text-sm text-slate-300">Total Executions: {analytics.total_executions.toLocaleString()}</span>
            <Badge variant="success">Success Rate: {analytics.success_rate_pct}%</Badge>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
