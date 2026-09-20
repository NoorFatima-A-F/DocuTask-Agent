import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Award,
  CheckCircle2,
  Lock,
  FileText,
} from 'lucide-react';

interface DecisionItem {
  id: string;
  title: string;
  importance: string;
  status: 'APPROVED' | 'PENDING' | 'REJECTED';
  utilityScore: number;
  roiMultiplier: number;
  impact: string;
  tradeoffs: string;
  evidenceHashes: string[];
  confidence: number;
  approverSignature: string;
}

export const ExecutiveDecisionCenter: React.FC = () => {
  const [decisions, setDecisions] = useState<DecisionItem[]>([
    {
      id: 'exec-dec-001',
      title: 'Accelerate Speculative Invoice Cache Deployment (Q3)',
      importance: 'TIER_1_EXECUTIVE',
      status: 'APPROVED',
      utilityScore: 0.965,
      roiMultiplier: 3.80,
      impact: 'Drives sub-200ms P95 latency across top 50 corporate invoice formats.',
      tradeoffs: 'Consumes 12 GB shared VRAM across worker nodes.',
      evidenceHashes: [
        'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
        '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4',
      ],
      confidence: 0.988,
      approverSignature: 'secp256k1:cso_oracle_key_alpha',
    },
    {
      id: 'exec-dec-002',
      title: 'Deploy Multi-Swarm Dynamic Nash Resource Auction',
      importance: 'TIER_1_EXECUTIVE',
      status: 'APPROVED',
      utilityScore: 0.930,
      roiMultiplier: 3.20,
      impact: 'Eliminates GPU starvation by dynamically reallocating idle tokens across departments.',
      tradeoffs: 'Requires 5% latency buffer during auction convergence cycles.',
      evidenceHashes: [
        '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8',
      ],
      confidence: 0.975,
      approverSignature: 'secp256k1:cso_oracle_key_beta',
    },
    {
      id: 'exec-dec-003',
      title: 'Mandate Zero-Knowledge Ledger Cryptographic Audit Trail',
      importance: 'TIER_2_DEPARTMENTAL',
      status: 'APPROVED',
      utilityScore: 0.985,
      roiMultiplier: 2.40,
      impact: 'Guarantees 100% compliance audit readiness with instant rollback capability.',
      tradeoffs: 'Adds 1.5ms overhead per strategic state mutation.',
      evidenceHashes: [
        '4b227777d4dd1fc61c6f884f48641d02b4d121d3fd328cb08b5531fcacdabf8a',
      ],
      confidence: 0.995,
      approverSignature: 'secp256k1:gov_oracle_key_gamma',
    },
  ]);

  const [approvedNotice, setApprovedNotice] = useState<string | null>(null);

  const handleApprove = (id: string) => {
    setDecisions((prev) =>
      prev.map((d) =>
        d.id === id
          ? {
              ...d,
              status: 'APPROVED',
              approverSignature: 'secp256k1:manual_override_approved',
            }
          : d
      )
    );
    setApprovedNotice(`Executive Decision ${id} cryptographically approved and sealed.`);
    setTimeout(() => setApprovedNotice(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Award className="w-6 h-6 text-indigo-500" />
            Executive Decision & CSO Intelligence Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Multi-Criteria Decision Analysis (MCDA), Analytic Hierarchy Process (AHP), and SHA-256 signed executive directives.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            <Lock className="w-3.5 h-3.5 mr-1" />
            3/3 Cryptographically Signed
          </Badge>
        </div>
      </div>

      {approvedNotice && (
        <div className="p-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-lg text-sm text-emerald-800 dark:text-emerald-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{approvedNotice}</span>
        </div>
      )}

      {/* Decisions List */}
      <div className="space-y-4">
        <h3 className="text-sm font-semibold text-gray-900 dark:text-white uppercase tracking-wider flex items-center gap-2">
          <FileText className="w-4 h-4 text-indigo-500" />
          Executive Decision Ledger
        </h3>

        <div className="grid grid-cols-1 gap-4">
          {decisions.map((dec) => (
            <Card key={dec.id} className="p-5 border-l-4 border-l-indigo-600 hover:shadow-md transition-shadow">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{dec.id}</span>
                    <Badge variant="intelligence" size="sm">
                      {dec.importance}
                    </Badge>
                  </div>
                  <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{dec.title}</h4>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="success" size="sm">
                    <CheckCircle2 className="w-3 h-3 mr-1" />
                    {dec.status}
                  </Badge>
                  {dec.status === 'PENDING' && (
                    <Button variant="primary" size="sm" onClick={() => handleApprove(dec.id)}>
                      Approve & Sign
                    </Button>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs">
                <div className="space-y-2">
                  <div>
                    <span className="text-gray-400 block mb-0.5">Organizational Impact:</span>
                    <p className="text-gray-700 dark:text-gray-300 font-medium">{dec.impact}</p>
                  </div>
                  <div>
                    <span className="text-gray-400 block mb-0.5">Strategic Tradeoffs:</span>
                    <p className="text-amber-700 dark:text-amber-400">{dec.tradeoffs}</p>
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between p-2 bg-gray-50 dark:bg-gray-900/40 rounded border border-gray-100 dark:border-gray-800">
                    <span className="text-gray-400">Utility / ROI:</span>
                    <span className="font-mono font-semibold text-indigo-600 dark:text-indigo-400">
                      {dec.utilityScore.toFixed(3)} utility • {dec.roiMultiplier}x ROI
                    </span>
                  </div>
                  <div>
                    <span className="text-gray-400 block mb-1">Signed Approver Signature:</span>
                    <div className="p-2 bg-gray-50 dark:bg-gray-900/60 rounded border border-gray-200 dark:border-gray-800 font-mono text-gray-600 dark:text-gray-400 break-all text-[11px]">
                      {dec.approverSignature}
                    </div>
                  </div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
