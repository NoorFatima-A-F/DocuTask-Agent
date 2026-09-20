import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { OrganizationOverviewReport, WorkforcePerformanceMetric, ExecutiveCouncilProposition } from '../../types/workforce';
import { Users, Building, ShieldCheck, TrendingUp, Sparkles, Scale, RefreshCw } from 'lucide-react';

export const ExecutiveOrganizationDashboard: React.FC = () => {
  const [overview, setOverview] = useState<OrganizationOverviewReport | null>(null);
  const [perf, setPerf] = useState<WorkforcePerformanceMetric | null>(null);
  const [props, setProps] = useState<ExecutiveCouncilProposition[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ov, pf, cp] = await Promise.all([
        workforceApiClient.getOverview(),
        workforceApiClient.getPerformance(),
        workforceApiClient.getCouncilPropositions()
      ]);
      setOverview(ov);
      setPerf(pf);
      setProps(cp);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="p-2 bg-indigo-500/20 text-indigo-400 rounded-xl">🏢</span>
            Executive Organization Dashboard
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Autonomous Digital Workforce Leadership & High-Level Operational Governance
          </p>
        </div>
        <Button variant="outline" onClick={loadData} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Intelligence
          </span>
        </Button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="p-5 bg-slate-900/50 border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-xs font-semibold uppercase">Total Digital Employees</span>
            <Users className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="text-3xl font-bold text-white mt-2">{overview?.total_employees ?? 0}</div>
          <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <span>●</span> 100% Autonomous Coverage
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-xs font-semibold uppercase">Workforce Readiness</span>
            <Sparkles className="w-5 h-5 text-purple-400" />
          </div>
          <div className="text-3xl font-bold text-purple-400 mt-2">
            {Math.round((overview?.workforce_readiness_index ?? 0.96) * 100)}%
          </div>
          <div className="text-xs text-slate-400 mt-1">Operational Fleet Health</div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-xs font-semibold uppercase">Average Trust Rating</span>
            <ShieldCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="text-3xl font-bold text-emerald-400 mt-2">
            {overview?.average_trust_score ?? 0.98}
          </div>
          <div className="text-xs text-slate-400 mt-1">Zero-Fabrication Baseline</div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800/80">
          <div className="flex items-center justify-between">
            <span className="text-slate-400 text-xs font-semibold uppercase">Monthly Salary Burn</span>
            <TrendingUp className="w-5 h-5 text-amber-400" />
          </div>
          <div className="text-3xl font-bold text-amber-400 mt-2">
            ${(perf?.monthly_salary_burn_usd ?? 12450).toLocaleString()}
          </div>
          <div className="text-xs text-slate-400 mt-1">Cost vs. 92% ROI Multiplier</div>
        </Card>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Building className="w-5 h-5 text-indigo-400" />
            Active Organization Structure
          </h3>
          <div className="space-y-3">
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 flex justify-between items-center">
              <div>
                <div className="text-sm font-semibold text-white">Autonomous Engineering</div>
                <div className="text-xs text-slate-400">Lead: Nexus Engineering (VP)</div>
              </div>
              <Badge variant="default">3 Employees</Badge>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 flex justify-between items-center">
              <div>
                <div className="text-sm font-semibold text-white">Security & Governance</div>
                <div className="text-xs text-slate-400">Lead: Aegis Sentinel (Director)</div>
              </div>
              <Badge variant="default">2 Employees</Badge>
            </div>
            <div className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/50 flex justify-between items-center">
              <div>
                <div className="text-sm font-semibold text-white">Autonomous Operations</div>
                <div className="text-xs text-slate-400">Lead: HyperDoc Synthesizer</div>
              </div>
              <Badge variant="default">2 Employees</Badge>
            </div>
          </div>
        </Card>

        <Card className="p-5 bg-slate-900/50 border-slate-800">
          <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
            <Scale className="w-5 h-5 text-amber-400" />
            Executive AI Council Quorum
          </h3>
          <div className="space-y-3">
            {props.map((p) => (
              <div key={p.id} className="p-4 bg-slate-800/40 rounded-xl border border-slate-700/50">
                <div className="flex justify-between items-start mb-2">
                  <div className="text-sm font-bold text-white">{p.title}</div>
                  <Badge variant={p.enacted ? "default" : "outline"}>
                    {p.enacted ? "ENACTED" : "VOTING"}
                  </Badge>
                </div>
                <p className="text-xs text-slate-400 mb-3">{p.summary}</p>
                <div className="flex gap-2">
                  {Object.entries(p.council_votes).map(([role, vote]) => (
                    <span key={role} className="text-[10px] px-2 py-1 bg-slate-900 rounded border border-slate-700 text-slate-300">
                      {role}: <strong className="text-emerald-400">{vote}</strong>
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
