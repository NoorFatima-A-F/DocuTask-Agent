import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { ShieldCheck, CheckCircle2, Lock, FileCode, Check } from 'lucide-react';

interface GovernanceRule {
  id: string;
  rule: string;
  category: 'BOUNDS' | 'MONOTONICITY' | 'APPROVAL' | 'IMMUTABILITY';
  status: 'PASSED' | 'WARNING' | 'FAILED';
  enforcement: 'STRICT_BLOCK' | 'AUDIT_LOG';
  details: string;
}

const rules: GovernanceRule[] = [
  {
    id: 'GOV-001',
    rule: 'Monotonic Feature Response',
    category: 'MONOTONICITY',
    status: 'PASSED',
    enforcement: 'STRICT_BLOCK',
    details: 'Positive feature increments must never decrease resulting confidence score.',
  },
  {
    id: 'GOV-002',
    rule: 'Output Bounds Compliance [0, 1]',
    category: 'BOUNDS',
    status: 'PASSED',
    enforcement: 'STRICT_BLOCK',
    details: 'Calculated confidence and uncertainty must stay strictly within [0.0, 1.0].',
  },
  {
    id: 'GOV-003',
    rule: 'Dual Approval on Formula Promotion',
    category: 'APPROVAL',
    status: 'PASSED',
    enforcement: 'STRICT_BLOCK',
    details: 'Formula migration from v1.2.0 to v1.3.0 approved by Governance Committee & Chief Architect.',
  },
  {
    id: 'GOV-004',
    rule: 'Cryptographic Event Hash Lineage',
    category: 'IMMUTABILITY',
    status: 'PASSED',
    enforcement: 'STRICT_BLOCK',
    details: 'All feature inputs must resolve to immutable Event Store entries with valid hashes.',
  },
];

export const FormulaGovernanceInspector: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <ShieldCheck className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Formula Governance & Policy Inspector
                <Badge variant="success" size="sm">Governance Certified</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Enforcing mathematical validity, monotonicity, bounds safety, and dual-authorization on formulas.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="outline" size="sm">Active Formula: WeightedEnsemble (v1.3.0)</Badge>
        </div>
      </div>

      {/* Governance Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono">
        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs text-slate-400">Monotonic Invariance</div>
          <div className="text-lg font-bold text-emerald-400 mt-1 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4" /> 100% Enforced
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Zero anti-monotonic regressions</p>
        </Card>

        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs text-slate-400">Formula Immutability</div>
          <div className="text-lg font-bold text-cyan-400 mt-1 flex items-center gap-2">
            <Lock className="w-4 h-4" /> Locked & Signed
          </div>
          <p className="text-[11px] text-slate-500 mt-1">SHA256: 9e01fb3401...</p>
        </Card>

        <Card className="p-4 bg-[#0F172A] border-[#1E293B]">
          <div className="text-xs text-slate-400">Audit Compliance</div>
          <div className="text-lg font-bold text-indigo-400 mt-1 flex items-center gap-2">
            <FileCode className="w-4 h-4" /> ISO/IEC 42001
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Enterprise AI Governance Ready</p>
        </Card>
      </div>

      {/* Rules Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B]">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-sm font-bold font-mono text-slate-200">Enforced Governance Policies</h2>
          <Badge variant="success" size="sm">4 Policies Active</Badge>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]">
              <tr>
                <th className="p-3">Rule ID</th>
                <th className="p-3">Policy Name</th>
                <th className="p-3">Category</th>
                <th className="p-3">Enforcement Mode</th>
                <th className="p-3">Status</th>
                <th className="p-3">Verification Details</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/40">
              {rules.map((r) => (
                <tr key={r.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="p-3 font-semibold text-emerald-400">{r.id}</td>
                  <td className="p-3 text-slate-100 font-bold">{r.rule}</td>
                  <td className="p-3">
                    <Badge variant="outline" size="sm">{r.category}</Badge>
                  </td>
                  <td className="p-3 text-slate-300">{r.enforcement}</td>
                  <td className="p-3">
                    <Badge variant="success" size="sm" className="flex items-center gap-1">
                      <Check className="w-3 h-3" />
                      {r.status}
                    </Badge>
                  </td>
                  <td className="p-3 text-slate-400">{r.details}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
