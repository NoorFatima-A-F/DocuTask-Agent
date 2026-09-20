import React, { useState, useEffect } from 'react';
import { Brain, Cpu, Sparkles, TrendingUp, ShieldCheck, RefreshCw, Zap } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { ExecutiveInsightReport } from '../../types/cognitive';

export const ExecutiveIntelligenceDashboard: React.FC = () => {
  const [insights, setInsights] = useState<ExecutiveInsightReport | null>(null);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await cognitiveApiClient.getExecutiveInsights();
      setInsights(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Brain className="w-7 h-7 text-indigo-400" />
            Enterprise Executive Cognitive Intelligence
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Top-level organizational reasoning, autonomous learning insights, cross-process discovery, and strategic guidance.
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" onClick={loadData}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={() => cognitiveApiClient.getExecutiveInsights()}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              Synthesize Insights
            </span>
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Cognitive Health</span>
            <Brain className="w-4 h-4 text-indigo-400" />
          </div>
          <p className="text-2xl font-bold text-slate-100 mt-2">
            {((insights?.cognitive_health_index || 0.98) * 100).toFixed(0)}%
          </p>
          <p className="text-xs text-emerald-400 mt-1">Autonomous reasoning active</p>
        </Card>

        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Hypotheses</span>
            <Cpu className="w-4 h-4 text-cyan-400" />
          </div>
          <p className="text-2xl font-bold text-slate-100 mt-2">{insights?.active_hypotheses_count || 3}</p>
          <p className="text-xs text-cyan-400 mt-1">Operational improvements proposed</p>
        </Card>

        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Discovered Processes</span>
            <TrendingUp className="w-4 h-4 text-emerald-400" />
          </div>
          <p className="text-2xl font-bold text-slate-100 mt-2">{insights?.discovered_processes_count || 4}</p>
          <p className="text-xs text-emerald-400 mt-1">Mined from runtime execution logs</p>
        </Card>

        <Card className="p-4 bg-slate-900/60 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Experience Memories Reused</span>
            <ShieldCheck className="w-4 h-4 text-amber-400" />
          </div>
          <p className="text-2xl font-bold text-slate-100 mt-2">{insights?.experience_memories_reused_count || 1420}</p>
          <p className="text-xs text-amber-400 mt-1">Zero-shot cross-agent transfers</p>
        </Card>
      </div>

      {/* Strategic Guidance & Optimization */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-indigo-400" />
            Top Strategic Recommendations
          </h2>
          <div className="space-y-3">
            {insights?.strategic_recommendations.map((rec) => (
              <div key={rec.id} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700/60 space-y-1">
                <div className="flex justify-between items-center">
                  <Badge variant="outline" className="text-indigo-400 border-indigo-500/30 text-[10px]">
                    {rec.category}
                  </Badge>
                  <Badge variant="warning">{rec.urgency} URGENCY</Badge>
                </div>
                <p className="text-sm font-semibold text-slate-200">{rec.title}</p>
                <p className="text-xs text-slate-400">{rec.description}</p>
                <p className="text-xs text-emerald-400 font-mono mt-1">Impact: {rec.projected_business_impact}</p>
              </div>
            ))}
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-slate-100 flex items-center gap-2">
            <Zap className="w-5 h-5 text-cyan-400" />
            Autonomous Optimization Opportunities
          </h2>
          <div className="space-y-3">
            {insights?.active_optimizations.map((opt) => (
              <div key={opt.id} className="p-3 bg-slate-800/50 rounded-lg border border-slate-700/60 space-y-2">
                <div className="flex justify-between items-center">
                  <Badge variant="info">{opt.subsystem}</Badge>
                  <span className="text-xs font-mono text-emerald-400">+${opt.projected_savings_monthly_usd}/mo</span>
                </div>
                <p className="text-sm font-medium text-slate-200">{opt.recommended_change}</p>
                <div className="flex justify-between items-center text-xs text-slate-400">
                  <span>Target: {opt.target_resource}</span>
                  <Button variant="intelligence" size="sm" onClick={() => cognitiveApiClient.applyOptimization(opt.id)}>
                    Apply Auto-Tune
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
