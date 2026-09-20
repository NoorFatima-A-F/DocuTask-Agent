import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { UsageRecord } from '../../types/saasPlatform';
import { BarChart3, Zap, FileText, DollarSign, Clock, RefreshCw } from 'lucide-react';

export const UsageAnalyticsDashboard: React.FC = () => {
  const [records, setRecords] = useState<UsageRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const data = await SaaSApiClient.listUsageRecords('tenant_acme_corp');
      setRecords(data);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <BarChart3 className="w-7 h-7 text-indigo-400" />
            Metered Usage & Quota Intelligence
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Real-time consumption telemetry for LLM tokens, OCR page volume, compute runtime, and API calls.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-indigo-950/60 text-indigo-400 rounded-lg">
              <Zap className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">LLM Token Burn Rate</span>
              <span className="text-xl font-bold text-white">12.45M Tokens</span>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-emerald-950/60 text-emerald-400 rounded-lg">
              <FileText className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">Document Pages Processed</span>
              <span className="text-xl font-bold text-white">4,800 Pages</span>
            </div>
          </CardContent>
        </Card>
        <Card className="bg-slate-900/80 border-slate-800">
          <CardContent className="p-4 flex items-center gap-4">
            <div className="p-3 bg-cyan-950/60 text-cyan-400 rounded-lg">
              <DollarSign className="w-6 h-6" />
            </div>
            <div>
              <span className="text-xs text-slate-400 block">Estimated Metered Spend</span>
              <span className="text-xl font-bold text-cyan-400">$96.90 USD</span>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Clock className="w-4 h-4 text-indigo-400" /> Usage Record Feed
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <div className="p-8 text-center text-slate-400">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading usage records...
            </div>
          ) : (
            records.map((r) => (
              <div
                key={r.record_id}
                className="p-3 bg-slate-800/40 rounded border border-slate-700/50 flex items-center justify-between"
              >
                <div>
                  <span className="text-sm font-semibold text-white block">{r.metric_name}</span>
                  <span className="text-xs text-slate-400">
                    Workspace: {r.workspace_id} • Unit Cost: ${r.unit_cost_usd}
                  </span>
                </div>
                <div className="flex items-center gap-4">
                  <span className="text-sm font-bold text-white">
                    {r.quantity.toLocaleString()} {r.unit}
                  </span>
                  <Badge variant="intelligence">${r.total_cost_usd.toFixed(2)}</Badge>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
