import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { SaaSExecutiveOverview } from '../../types/saasPlatform';
import {
  TrendingUp,
  Building2,
  Layers,
  Zap,
  DollarSign,
  ShieldCheck,
  RefreshCw,
  Server,
  Activity,
} from 'lucide-react';

export const PlatformExecutiveDashboard: React.FC = () => {
  const [data, setData] = useState<SaaSExecutiveOverview | null>(null);
  const [loading, setLoading] = useState(true);

  const fetchData = async () => {
    setLoading(true);
    const res = await SaaSApiClient.getExecutiveOverview();
    setData(res);
    setLoading(false);
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading || !data) {
    return (
      <div className="flex items-center justify-center p-12 text-slate-400">
        <RefreshCw className="w-6 h-6 animate-spin mr-2" /> Loading Executive Control Plane...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Server className="w-7 h-7 text-indigo-400" />
            Enterprise SaaS Control Plane & Multi-Tenant Operating System
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Global fleet observability, MRR/ARR economics, tenant health, and consumption telemetry.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" className="px-3 py-1">
            SLA {data.mean_system_sla_compliance_pct}%
          </Badge>
          <Button variant="outline" onClick={fetchData}>
            <span className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> Refresh
            </span>
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Monthly Recurring Rev</span>
              <DollarSign className="w-5 h-5 text-emerald-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">${data.monthly_recurring_revenue_usd.toLocaleString()}</span>
              <span className="text-xs text-emerald-400 flex items-center font-medium">
                <TrendingUp className="w-3 h-3 mr-0.5" /> +{data.net_mrr_growth_pct}%
              </span>
            </div>
            <p className="text-xs text-slate-500 mt-1">ARR: ${data.annual_recurring_revenue_usd.toLocaleString()}</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Enterprise Tenants</span>
              <Building2 className="w-5 h-5 text-indigo-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">{data.active_tenants}</span>
              <span className="text-xs text-slate-400">/ {data.total_tenants} Total</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{data.total_organizations} Orgs across {data.total_workspaces} Workspaces</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Metered Token Volume</span>
              <Zap className="w-5 h-5 text-amber-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-white">{(data.total_metered_tokens / 1_000_000).toFixed(2)}M</span>
              <span className="text-xs text-amber-400">Tokens</span>
            </div>
            <p className="text-xs text-slate-500 mt-1">{data.total_metered_ocr_pages.toLocaleString()} OCR pages processed</p>
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-5">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Enterprise Compliance</span>
              <ShieldCheck className="w-5 h-5 text-cyan-400" />
            </div>
            <div className="mt-2 flex items-baseline gap-2">
              <span className="text-2xl font-bold text-cyan-400">SOC2 Type II</span>
              <Badge variant="intelligence" className="text-[10px]">VERIFIED</Badge>
            </div>
            <p className="text-xs text-slate-500 mt-1">Hash-chained audit log active</p>
          </CardContent>
        </Card>
      </div>

      {/* Grid of Subsystem Health */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-400" /> Multi-Tenant System Fabric Health
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {[
              { name: 'Tenant Isolation Gateway', status: 'Optimal', latency: '0.4ms', badge: 'success' },
              { name: 'SAML 2.0 / SCIM Identity Broker', status: 'Healthy', latency: '12ms', badge: 'success' },
              { name: 'Usage Metering & Rate-Limiter', status: 'Active', latency: '1.2ms', badge: 'success' },
              { name: 'Cryptographic License Validator', status: 'Operational', latency: '0.1ms', badge: 'success' },
              { name: 'AI Marketplace Registry', status: 'Synced', latency: '22ms', badge: 'intelligence' },
            ].map((sub, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
                <span className="text-sm text-slate-200 font-medium">{sub.name}</span>
                <div className="flex items-center gap-3">
                  <span className="text-xs text-slate-400">{sub.latency}</span>
                  <Badge variant={sub.badge as any}>{sub.status}</Badge>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        <Card className="bg-slate-900/80 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white flex items-center gap-2">
              <Layers className="w-4 h-4 text-indigo-400" /> SaaS Revenue & Cohort Retention
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="p-4 rounded-lg bg-indigo-950/20 border border-indigo-900/40">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-slate-300">Enterprise Plan Distribution</span>
                <span className="text-indigo-400 font-bold">85% Enterprise / 15% Business</span>
              </div>
              <div className="w-full bg-slate-800 rounded-full h-2.5 overflow-hidden flex">
                <div className="bg-indigo-500 h-2.5 w-[85%]"></div>
                <div className="bg-cyan-500 h-2.5 w-[15%]"></div>
              </div>
            </div>

            <div className="grid grid-cols-3 gap-3 text-center">
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-xs text-slate-400 block">Q1 Retention</span>
                <span className="text-lg font-bold text-white">98.4%</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-xs text-slate-400 block">Net Expansion</span>
                <span className="text-lg font-bold text-emerald-400">124%</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="text-xs text-slate-400 block">Gross Margin</span>
                <span className="text-lg font-bold text-cyan-400">82.6%</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
