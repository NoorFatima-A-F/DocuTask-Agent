import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Archive, ArrowRight, ShieldCheck } from 'lucide-react';

export const RetirementCenter: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Archive className="w-7 h-7 text-indigo-400" />
            AI Application Sunset & Retirement Center
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Controlled deprecation cycles, target migration guidance, and regulatory data retention.
          </p>
        </div>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" /> Deprecated Asset Migration Matrix
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          <div className="p-4 bg-slate-800/40 rounded border border-slate-700/50 space-y-2">
            <div className="flex items-center justify-between">
              <span className="text-sm font-semibold text-white">Legacy Invoice OCR v1</span>
              <Badge variant="warning">DEPRECATED</Badge>
            </div>
            <p className="text-xs text-slate-300">
              Scheduled sunset in 30 days. All workloads migrating to Autonomous Invoice Reconciler v1.2.
            </p>
            <div className="flex items-center gap-2 text-xs text-indigo-400 font-mono pt-2 border-t border-slate-700/40">
              <span>Target: agt_acme_invoice_reconciler</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
