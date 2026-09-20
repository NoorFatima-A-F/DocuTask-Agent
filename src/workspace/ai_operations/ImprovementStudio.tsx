import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  CheckCircle,
  XCircle,
  ShieldAlert,
  GitPullRequest,
  RefreshCw,
  TrendingUp,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { ImprovementProposal } from '../../types/aiOperations';

export const ImprovementStudio: React.FC = () => {
  const [proposals, setProposals] = useState<ImprovementProposal[]>([]);
  const [selectedProposal, setSelectedProposal] = useState<ImprovementProposal | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionInProgress, setActionInProgress] = useState(false);

  const loadProposals = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getProposals();
      setProposals(data);
      if (data.length > 0 && !selectedProposal) {
        setSelectedProposal(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load improvement proposals:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProposals();
  }, []);

  const handleApprove = async (propId: string) => {
    try {
      setActionInProgress(true);
      const updated = await AIOperationsApiClient.approveProposal(propId);
      setSelectedProposal(updated);
      await loadProposals();
    } catch (err) {
      console.error('Failed to approve proposal:', err);
    } finally {
      setActionInProgress(false);
    }
  };

  const handleReject = async (propId: string) => {
    try {
      setActionInProgress(true);
      const updated = await AIOperationsApiClient.rejectProposal(propId);
      setSelectedProposal(updated);
      await loadProposals();
    } catch (err) {
      console.error('Failed to reject proposal:', err);
    } finally {
      setActionInProgress(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 rounded-xl border border-indigo-500/20">
            <Sparkles className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Controlled Self-Improvement Studio</h1>
            <p className="text-xs text-slate-400">AI proposes optimizations • Canary validates • Human approval gates production deployment</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadProposals} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Proposals List (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Improvement Proposals</h2>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {proposals.map((p) => (
              <Card
                key={p.proposal_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedProposal?.proposal_id === p.proposal_id
                    ? 'bg-indigo-950/30 border-indigo-500/50 shadow-md shadow-indigo-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedProposal(p)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{p.target_agent_id}</span>
                  <Badge
                    variant={
                      p.status === 'APPROVED' || p.status === 'DEPLOYED'
                        ? 'success'
                        : p.status === 'REJECTED'
                        ? 'error'
                        : 'warning'
                    }
                  >
                    {p.status}
                  </Badge>
                </div>
                <h3 className="font-medium text-slate-200 text-xs mt-1.5 line-clamp-2">{p.title}</h3>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2">
                  <span className="text-emerald-400 font-semibold">+{(p.expected_quality_delta * 100).toFixed(0)}% Quality</span>
                  <span className="text-slate-500">{new Date(p.created_at).toLocaleDateString()}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Proposal Details (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedProposal ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">{selectedProposal.proposal_type}</Badge>
                    <h2 className="text-lg font-bold text-white">{selectedProposal.title}</h2>
                  </div>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Target: {selectedProposal.target_agent_id} • Proposal ID: {selectedProposal.proposal_id}
                  </p>
                </div>
                <Badge
                  variant={
                    selectedProposal.status === 'APPROVED' || selectedProposal.status === 'DEPLOYED'
                      ? 'success'
                      : selectedProposal.status === 'REJECTED'
                      ? 'error'
                      : 'warning'
                  }
                >
                  {selectedProposal.status}
                </Badge>
              </div>

              {/* Description */}
              <p className="text-sm text-slate-300 leading-relaxed">{selectedProposal.description}</p>

              {/* Projected Impact Metrics */}
              <div className="grid grid-cols-3 gap-3">
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5 text-emerald-400" /> Quality Delta</span>
                  <p className="text-lg font-bold text-emerald-400 mt-1">+{(selectedProposal.expected_quality_delta * 100).toFixed(1)}%</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5 text-cyan-400" /> Latency Delta</span>
                  <p className="text-lg font-bold text-cyan-300 mt-1">{selectedProposal.expected_latency_delta_ms} ms</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5 text-indigo-400" /> Cost Delta</span>
                  <p className="text-lg font-bold text-indigo-300 mt-1">{selectedProposal.expected_cost_delta_pct}%</p>
                </div>
              </div>

              {/* Diff View */}
              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <GitPullRequest className="w-3.5 h-3.5 text-indigo-400" /> Change Diff Summary
                </h4>
                <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-emerald-400 whitespace-pre-wrap leading-relaxed">
                  {selectedProposal.diff_summary}
                </div>
              </div>

              {/* HITL Approval Gate Controls */}
              {selectedProposal.status === 'PENDING_HITL_APPROVAL' && (
                <div className="p-4 bg-amber-950/20 border border-amber-500/30 rounded-xl space-y-3">
                  <div className="flex items-center gap-2 text-amber-300 text-xs font-semibold">
                    <ShieldAlert className="w-4 h-4" /> Human-in-the-Loop Governance Gate Required
                  </div>
                  <p className="text-xs text-slate-300">
                    This modification has passed canary validation ($p &lt; 0.05$). Confirm deployment to production fleet.
                  </p>
                  <div className="flex items-center gap-3 pt-1">
                    <Button
                      variant="intelligence"
                      onClick={() => handleApprove(selectedProposal.proposal_id)}
                      disabled={actionInProgress}
                    >
                      <span className="flex items-center gap-2">
                        <CheckCircle className="w-4 h-4" />
                        Approve & Deploy
                      </span>
                    </Button>
                    <Button
                      variant="danger"
                      onClick={() => handleReject(selectedProposal.proposal_id)}
                      disabled={actionInProgress}
                    >
                      <span className="flex items-center gap-2">
                        <XCircle className="w-4 h-4" />
                        Reject Proposal
                      </span>
                    </Button>
                  </div>
                </div>
              )}
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <Sparkles className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select an improvement proposal to review diffs and execute human approval decisions.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
