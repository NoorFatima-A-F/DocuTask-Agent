import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  CheckCircle,
  XCircle,
  Lock,
  RefreshCw,
  Database,
  FileCheck,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { EvolutionGovernanceReviewPayload, RollbackSnapshotPayload } from '../../types/evolutionPlatform';

export const GovernanceApprovalCenter: React.FC = () => {
  const [reviews, setReviews] = useState<EvolutionGovernanceReviewPayload[]>([]);
  const [snapshots, setSnapshots] = useState<RollbackSnapshotPayload[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [revData, snapData] = await Promise.all([
        EvolutionPlatformApiClient.listGovernanceReviews(),
        EvolutionPlatformApiClient.listRollbackSnapshots(),
      ]);
      setReviews(revData);
      setSnapshots(snapData);
    } catch (err) {
      console.error('Failed to load governance data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (reviewId: string) => {
    setActionLoading(reviewId);
    try {
      const updated = await EvolutionPlatformApiClient.approveReview(reviewId);
      setReviews((prev) => prev.map((r) => (r.review_id === reviewId ? updated : r)));
    } catch (err) {
      console.error('Approval failed:', err);
    } finally {
      setActionLoading(null);
    }
  };

  const handleReject = async (reviewId: string) => {
    setActionLoading(reviewId);
    try {
      const updated = await EvolutionPlatformApiClient.rejectReview(reviewId, 'Rejected by operator');
      setReviews((prev) => prev.map((r) => (r.review_id === reviewId ? updated : r)));
    } catch (err) {
      console.error('Rejection failed:', err);
    } finally {
      setActionLoading(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 border border-purple-500/20 rounded-xl">
            <ShieldCheck className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Cryptographic Governance & Rollback Center</h1>
              <Badge variant="sentinel" size="sm">Zero-Risk Gatekeeper</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Enforces multi-stage verification gates, cryptographic SHA-256 rollback snapshots, and policy compliance.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadData}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      {/* Grid: Reviews & Snapshots */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Governance Reviews */}
        <div className="lg:col-span-2 bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <FileCheck className="w-5 h-5 text-purple-400" />
              <h2 className="text-base font-semibold text-slate-100">Governance Review Gates</h2>
            </div>
            <Badge variant="outline" size="sm">{reviews.length} Active Reviews</Badge>
          </div>

          <div className="space-y-4">
            {reviews.map((r) => (
              <div
                key={r.review_id}
                className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-5 space-y-4 hover:border-slate-700 transition-all"
              >
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 pb-3 border-b border-slate-800/80">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm font-bold text-purple-400">{r.review_id}</span>
                      <Badge
                        variant={
                          r.approval_status === 'APPROVED'
                            ? 'success'
                            : r.approval_status === 'REJECTED'
                            ? 'error'
                            : 'warning'
                        }
                        size="sm"
                      >
                        {r.approval_status}
                      </Badge>
                    </div>
                    <span className="text-xs text-slate-400 font-mono mt-0.5 block">
                      Target Mutation: <span className="text-slate-200">{r.mutation_id}</span> • Reviewer: {r.reviewer_agent_id}
                    </span>
                  </div>

                  {r.approval_status === 'PENDING' && (
                    <div className="flex items-center gap-2">
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleReject(r.review_id)}
                        disabled={actionLoading === r.review_id}
                      >
                        <span className="flex items-center gap-1.5">
                          <XCircle className="w-3.5 h-3.5" />
                          Reject
                        </span>
                      </Button>
                      <Button
                        variant="intelligence"
                        size="sm"
                        onClick={() => handleApprove(r.review_id)}
                        disabled={actionLoading === r.review_id}
                      >
                        <span className="flex items-center gap-1.5">
                          <CheckCircle className="w-3.5 h-3.5" />
                          Approve & Seal
                        </span>
                      </Button>
                    </div>
                  )}
                </div>

                {/* Gates Status */}
                <div className="grid grid-cols-3 gap-3 text-xs font-mono">
                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    <div>
                      <div className="text-slate-400 text-[10px]">FORMAL VERIFICATION</div>
                      <div className="text-slate-200 font-semibold">{r.formal_verification_passed ? 'PASSED' : 'FAILED'}</div>
                    </div>
                  </div>

                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    <div>
                      <div className="text-slate-400 text-[10px]">SHADOW SIMULATION</div>
                      <div className="text-slate-200 font-semibold">{r.simulation_verified ? 'VERIFIED' : 'PENDING'}</div>
                    </div>
                  </div>

                  <div className="p-2.5 bg-slate-900 border border-slate-800 rounded-lg flex items-center gap-2">
                    <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                    <div>
                      <div className="text-slate-400 text-[10px]">BENCHMARK PROOF</div>
                      <div className="text-slate-200 font-semibold">{r.benchmark_verified ? 'SUPERIOR' : 'PENDING'}</div>
                    </div>
                  </div>
                </div>

                {r.cryptographic_signature && (
                  <div className="p-2.5 bg-slate-900/90 border border-purple-500/20 rounded-lg text-xs font-mono text-slate-400 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <Lock className="w-3.5 h-3.5 text-purple-400" />
                      <span>Signature:</span>
                    </div>
                    <span className="text-purple-300 font-semibold truncate max-w-[320px]">{r.cryptographic_signature}</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Right 1 Col: Rollback Snapshots */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Database className="w-5 h-5 text-indigo-400" />
              <h2 className="text-base font-semibold text-slate-100">Rollback Snapshots</h2>
            </div>
            <Badge variant="sentinel" size="sm">Immutable</Badge>
          </div>

          <div className="space-y-3">
            {snapshots.map((s) => (
              <div
                key={s.snapshot_id}
                className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-2 text-xs font-mono"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-200">{s.snapshot_id}</span>
                  <Badge variant="outline" size="sm">{s.platform_version}</Badge>
                </div>
                <div className="text-slate-400 text-[11px] truncate">
                  <span className="text-purple-400 font-semibold">SHA256: </span>
                  {s.sha256_seal}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
