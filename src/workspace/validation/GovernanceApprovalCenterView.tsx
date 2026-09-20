import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const GovernanceApprovalCenterView: React.FC = () => {
  const approvalStages = [
    {
      stage: 'STAGE 1: Automated Test & Invariant Verification',
      status: 'PASSED',
      approver: 'CI/CD Automated Daemon',
      timestamp: '2 hours ago',
      details: '10/10 test suites passed. Residual errors within ±5% bounds.',
      isDone: true,
    },
    {
      stage: 'STAGE 2: Principal AI Engineer Peer Review',
      status: 'APPROVED',
      approver: 'lead-architect@enterprise.internal',
      timestamp: '1 hour ago',
      details: 'Verified Pearl SCM backdoor adjustment and Bayesian regret bounds.',
      isDone: true,
    },
    {
      stage: 'STAGE 3: Enterprise Compliance & Model Safety Signoff',
      status: 'APPROVED',
      approver: 'compliance-officer@enterprise.internal',
      timestamp: '30 mins ago',
      details: 'Audited deterministic audit logs and zero-data-loss rollback plans.',
      isDone: true,
    },
    {
      stage: 'STAGE 4: Production Rollout Authorization',
      status: 'READY_TO_DEPLOY',
      approver: 'Release Gatekeeper',
      timestamp: 'Pending Final Trigger',
      details: 'Canary staging health check optimal; ready for 100% production traffic promotion.',
      isDone: false,
    },
  ];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">🛡️</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Governance Approval Center & Multi-Stage Gatekeeper
              </h2>
              <Badge variant="success" size="sm">
                3/4 GATES APPROVED
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Multi-stakeholder compliance verification before promoting evolved model weights and policies to production.
            </p>
          </div>
          <button className="px-4 py-2 rounded-xl text-xs font-mono font-bold bg-emerald-600 text-white hover:bg-emerald-500 transition-all shadow-lg shadow-emerald-600/20">
            ✓ AUTHORIZE FINAL PRODUCTION PROMOTION
          </button>
        </div>
      </div>

      {/* Stage Flow */}
      <div className="space-y-4">
        {approvalStages.map((st, idx) => (
          <Card
            key={idx}
            className={`p-6 border ${
              st.isDone
                ? 'bg-[#0F172A] border-[#1E293B]'
                : 'bg-blue-950/20 border-blue-500/50 shadow-lg shadow-blue-500/10'
            }`}
          >
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-bold font-mono text-[#F8FAFC]">{st.stage}</span>
                </div>
                <div className="text-xs font-mono text-[#64748B] mt-1">
                  Signed by: <span className="text-[#94A3B8] font-bold">{st.approver}</span> • {st.timestamp}
                </div>
                <p className="text-xs font-mono text-[#E2E8F0] mt-3">{st.details}</p>
              </div>
              <Badge variant={st.isDone ? 'success' : 'info'} size="sm">
                {st.status}
              </Badge>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
