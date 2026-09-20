import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentApproval } from '../../types/aiLifecycle';
import { CheckSquare, UserCheck, RefreshCw } from 'lucide-react';

export const ApprovalWorkflowCenter: React.FC = () => {
  const [approvals, setApprovals] = useState<AgentApproval[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await AILifecycleApiClient.listApprovals('agt_acme_invoice_reconciler');
      setApprovals(list);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <CheckSquare className="w-7 h-7 text-indigo-400" />
            Enterprise Approval Workflow Engine
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Multi-stage review gates: Developer Submission → Security Gate → Business Signoff → Compliance Release.
          </p>
        </div>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-emerald-400" /> Governance Signoff History
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <div className="p-8 text-center text-slate-400">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Approvals...
            </div>
          ) : (
            approvals.map((appr) => (
              <div
                key={appr.approval_id}
                className="p-4 bg-slate-800/40 rounded border border-slate-700/50 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <span className="text-sm font-semibold text-white">{appr.stage}</span>
                  <Badge variant={appr.decision === 'APPROVED' ? 'success' : 'warning'}>
                    {appr.decision}
                  </Badge>
                </div>
                <p className="text-xs text-slate-300">{appr.comments}</p>
                <div className="text-[10px] text-slate-400 flex justify-between pt-2 border-t border-slate-700/40 font-mono">
                  <span>Approver: {appr.approver_email || 'System Governor'}</span>
                  <span>{new Date(appr.timestamp).toLocaleString()}</span>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
