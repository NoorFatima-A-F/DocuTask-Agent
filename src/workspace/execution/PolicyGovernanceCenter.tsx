import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  ShieldAlert,
  RotateCw,
  CheckCircle,
  XCircle,
  AlertTriangle,
  Lock,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { PolicyRule, ApprovalRequest } from '../../types/executionPlatform';

export const PolicyGovernanceCenter: React.FC = () => {
  const [rules, setRules] = useState<PolicyRule[]>([]);
  const [approvals, setApprovals] = useState<ApprovalRequest[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [rList, aList] = await Promise.all([
        executionPlatformApiClient.listPolicyRules(),
        executionPlatformApiClient.listApprovals(),
      ]);
      setRules(rList.rules || []);
      setApprovals(aList.approvals || []);
    } catch (err) {
      console.error('Failed to load governance rules:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleResolveApproval = async (approvalId: string, approved: boolean) => {
    try {
      await executionPlatformApiClient.resolveApproval(approvalId, approved, 'Executive Governance Officer');
      await loadData();
    } catch (err) {
      console.error('Error resolving approval:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-amber-400" />
            Execution Policy, Governance & HITL Sign-off Gates
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            RBAC/ABAC rule evaluation, spending cap thresholds, destructive mutation guards & human escalation
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      {loading && rules.length === 0 && (
        <p className="text-xs text-slate-500 py-4 text-center">Loading governance rules...</p>
      )}

      {/* HITL Pending Approvals */}
      <Card className="bg-slate-900/80 border-amber-800/40">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Human-In-The-Loop Approval Requests ({approvals.filter((a) => a.status === 'pending').length} Pending)
          </CardTitle>
        </CardHeader>
        <CardContent>
          {approvals.filter((a) => a.status === 'pending').length === 0 ? (
            <div className="py-6 text-center text-xs text-slate-500">
              No pending execution escalations. All operational thresholds clear.
            </div>
          ) : (
            <div className="space-y-3">
              {approvals
                .filter((a) => a.status === 'pending')
                .map((req) => (
                  <div
                    key={req.approval_id}
                    className="p-4 bg-slate-950 border border-amber-800/60 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-4"
                  >
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-semibold text-white">{req.reason}</span>
                        <Badge variant="error">{req.risk_level} risk</Badge>
                      </div>
                      <p className="text-xs text-slate-400 mt-1 font-mono">
                        Tool: {req.tool_id} • Mission: {req.mission_id} • Requester: {req.requester}
                      </p>
                    </div>
                    <div className="flex items-center gap-2">
                      <Button
                        variant="secondary"
                        onClick={() => handleResolveApproval(req.approval_id, true)}
                      >
                        <span className="flex items-center gap-1.5 text-xs text-emerald-400">
                          <CheckCircle className="w-4 h-4" /> Approve
                        </span>
                      </Button>
                      <Button
                        variant="outline"
                        onClick={() => handleResolveApproval(req.approval_id, false)}
                      >
                        <span className="flex items-center gap-1.5 text-xs text-rose-400">
                          <XCircle className="w-4 h-4" /> Deny
                        </span>
                      </Button>
                    </div>
                  </div>
                ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Active Rules Specifications Table */}
      <Card className="bg-slate-900/60 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <Lock className="w-4 h-4 text-purple-400" />
            Active Governance Policy Rules ({rules.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="border border-slate-800 rounded-xl overflow-hidden">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950 text-slate-400 font-mono">
                <tr>
                  <th className="p-3">Rule Name</th>
                  <th className="p-3">Target Scope</th>
                  <th className="p-3">Policy Decision</th>
                  <th className="p-3">Condition Expression</th>
                  <th className="p-3">Simulation Mandatory</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800 text-slate-300">
                {rules.map((r) => (
                  <tr key={r.rule_id} className="hover:bg-slate-800/30">
                    <td className="p-3 font-semibold text-white">
                      {r.name}
                      <p className="text-[11px] text-slate-400 font-normal mt-0.5">{r.description}</p>
                    </td>
                    <td className="p-3 font-mono text-purple-300">{r.target_tools.join(', ')}</td>
                    <td className="p-3">
                      <Badge
                        variant={
                          r.decision === 'allow'
                            ? 'success'
                            : r.decision === 'deny'
                            ? 'error'
                            : 'warning'
                        }
                      >
                        {r.decision}
                      </Badge>
                    </td>
                    <td className="p-3 font-mono text-slate-400">{r.condition_expression}</td>
                    <td className="p-3">
                      {r.requires_simulation ? (
                        <Badge variant="intelligence">Required</Badge>
                      ) : (
                        <span className="text-slate-500">Optional</span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
