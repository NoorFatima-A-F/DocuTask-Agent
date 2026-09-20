import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, Check, X, Clock, FileCheck } from 'lucide-react';

export const GovernanceApprovalWorkflow: React.FC = () => {
  const [reviews, setReviews] = useState([
    {
      id: 'rev-001',
      candidateId: 'cand_b5e79b7c',
      policyName: 'High-Throughput Wavefront Partitioning Policy (v1.1.0)',
      target: 'planner',
      projectedGain: '+14.2% Throughput',
      riskScore: 0.12,
      riskTier: 'LOW',
      confidence: 96.5,
      guardrailsPassed: true,
      decision: 'APPROVED',
      reviewer: 'Governance Gatekeeper Engine',
      comments: 'All 100 counterfactual replay simulations passed with zero invariant regressions.',
      timestamp: '2026-09-12 00:15 UTC',
    },
    {
      id: 'rev-002',
      candidateId: 'cand_c8f12a9e',
      policyName: 'Aggressive Concurrency Booster Policy (16 Workers)',
      target: 'worker',
      projectedGain: '+38.5% Throughput',
      riskScore: 0.38,
      riskTier: 'MEDIUM',
      confidence: 89.2,
      guardrailsPassed: true,
      decision: 'PENDING_REVIEW',
      reviewer: 'Pending Human Operator Review',
      comments: 'Requires confirmation of downstream rate limit quotas before live activation.',
      timestamp: '2026-09-12 00:28 UTC',
    },
  ]);

  const handleAction = (id: string, action: 'APPROVED' | 'REJECTED') => {
    setReviews((prev) =>
      prev.map((r) =>
        r.id === id
          ? {
              ...r,
              decision: action,
              reviewer: 'Admin User (Pair Programming Console)',
              comments: `Manually ${action.toLowerCase()} via governance workflow console.`,
            }
          : r
      )
    );
  };

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-teal-500/20 to-emerald-500/20 border border-teal-500/30 rounded-xl text-teal-400">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Governance & Safety Approval Workflow
              <Badge variant="intelligence" size="sm">Phase 13.5</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Enforce multi-tier governance gates, guardrail validation bounds, and human-in-the-loop policy promotions
            </p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">100% Guardrail Enforced</Badge>
        </div>
      </div>

      {/* Review Queue Cards */}
      <div className="space-y-4 font-mono">
        <h2 className="text-sm font-bold text-white flex items-center gap-2">
          <FileCheck className="w-4 h-4 text-indigo-400" />
          Candidate Policy Review Queue
        </h2>

        <div className="grid grid-cols-1 gap-4">
          {reviews.map((rev) => (
            <Card key={rev.id} className="p-5 rounded-2xl border border-[#1E293B] bg-[#0F172A] space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-3 border-b border-[#1E293B] pb-3">
                <div className="flex items-center gap-3">
                  <h3 className="text-sm font-bold text-white">{rev.policyName}</h3>
                  <Badge variant={rev.decision === 'APPROVED' ? 'success' : rev.decision === 'REJECTED' ? 'error' : 'warning'} size="sm">
                    {rev.decision}
                  </Badge>
                </div>

                <div className="text-xs text-[#94A3B8] flex items-center gap-3">
                  <span className="flex items-center gap-1"><Clock className="w-3.5 h-3.5" /> {rev.timestamp}</span>
                  <span>ID: {rev.candidateId}</span>
                </div>
              </div>

              {/* Metrics Breakdown */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
                  <span className="text-[10px] text-[#64748B] block">Projected Gain</span>
                  <span className="text-cyan-400 font-bold mt-0.5 block">{rev.projectedGain}</span>
                </div>
                <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
                  <span className="text-[10px] text-[#64748B] block">Risk Score</span>
                  <span className={`font-bold mt-0.5 block ${rev.riskScore < 0.2 ? 'text-emerald-400' : 'text-amber-400'}`}>
                    {rev.riskScore} ({rev.riskTier})
                  </span>
                </div>
                <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
                  <span className="text-[10px] text-[#64748B] block">Posterior Certainty</span>
                  <span className="text-indigo-400 font-bold mt-0.5 block">{rev.confidence}%</span>
                </div>
                <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl">
                  <span className="text-[10px] text-[#64748B] block">Safety Guardrails</span>
                  <span className="text-emerald-400 font-bold mt-0.5 block">Zero Violations</span>
                </div>
              </div>

              {/* Reviewer Note */}
              <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-xs space-y-1">
                <div className="flex justify-between text-[#64748B] text-[10px]">
                  <span>REVIEWER: {rev.reviewer}</span>
                </div>
                <p className="text-[#94A3B8]">{rev.comments}</p>
              </div>

              {/* Action Buttons if Pending */}
              {rev.decision === 'PENDING_REVIEW' && (
                <div className="flex items-center justify-end gap-3 pt-2">
                  <button
                    onClick={() => handleAction(rev.id, 'REJECTED')}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-300 border border-red-500/30 rounded-lg text-xs font-mono transition-colors"
                  >
                    <X className="w-3.5 h-3.5" /> Reject Policy
                  </button>
                  <button
                    onClick={() => handleAction(rev.id, 'APPROVED')}
                    className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-xs font-mono font-bold transition-colors"
                  >
                    <Check className="w-3.5 h-3.5" /> Approve & Promote
                  </button>
                </div>
              )}
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
