import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { LifecycleOverview, AgentApplication } from '../../types/aiLifecycle';
import {
  Layers,
  Cpu,
  DollarSign,
  Rocket,
  AlertCircle,
  RefreshCw,
  GitBranch,
} from 'lucide-react';

export const AIApplicationDashboard: React.FC = () => {
  const [overview, setOverview] = useState<LifecycleOverview | null>(null);
  const [agents, setAgents] = useState<AgentApplication[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    const [ov, agtList] = await Promise.all([
      AILifecycleApiClient.getOverview(),
      AILifecycleApiClient.listAgents(),
    ]);
    setOverview(ov);
    setAgents(agtList);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading || !overview) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mr-2" /> Loading AI Application Lifecycle Control Plane...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Layers className="w-7 h-7 text-indigo-400" />
            Autonomous AI Application Lifecycle Platform (AAILP)
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Enterprise agent development, testing, security review, multi-stage approval, and deployment control.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" className="px-3 py-1">
            Security Score: {overview.mean_security_score}/100
          </Badge>
          <Button variant="outline" onClick={loadData}>
            <span className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> Refresh Fleet
            </span>
          </Button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Managed AI Applications</span>
              <Cpu className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">{overview.total_managed_agents}</span>
              <span className="text-xs text-slate-400">Agents</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{overview.deployed_in_production} active in production</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Production Deployments</span>
              <Rocket className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-emerald-400">{overview.deployed_in_production}</span>
              <span className="text-xs text-slate-400">/ {overview.total_managed_agents}</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">Canary & Blue-Green verified</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">In Review / Testing</span>
              <AlertCircle className="w-5 h-5 text-amber-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-amber-400">{overview.in_review_or_testing}</span>
              <span className="text-xs text-slate-400">Pipelines</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">Awaiting security or owner signoff</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Enterprise Automation ROI</span>
              <DollarSign className="w-5 h-5 text-cyan-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-cyan-400">${overview.total_automation_roi_usd.toLocaleString()}</span>
              <Badge variant="intelligence" className="text-[10px]">VERIFIED</Badge>
            </div>
            <p className="text-xs text-slate-500 mt-1">Across managed enterprise fleet</p>
          </CardContent>
        </Card>
      </div>

      {/* Fleet Inventory Quick View */}
      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-indigo-400" /> Enterprise Agent Fleet Status
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {agents.map((agent) => (
            <div
              key={agent.agent_id}
              className="p-4 bg-slate-800/40 rounded-lg border border-slate-700/50 flex items-center justify-between"
            >
              <div>
                <div className="flex items-center gap-3">
                  <span className="text-base font-semibold text-white">{agent.name}</span>
                  <Badge variant={agent.lifecycle_state === 'DEPLOYED' ? 'success' : 'warning'}>
                    {agent.lifecycle_state}
                  </Badge>
                  <Badge variant="outline" className="text-xs font-mono">
                    v{agent.current_version}
                  </Badge>
                </div>
                <p className="text-xs text-slate-400 mt-1">{agent.description}</p>
              </div>
              <div className="flex items-center gap-3">
                <Badge variant="intelligence">{agent.category}</Badge>
                <span className="text-xs text-slate-500 font-mono">{agent.owner_email}</span>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
    </div>
  );
};
