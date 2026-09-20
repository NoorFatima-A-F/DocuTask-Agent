import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { FileText, Download, ShieldCheck, CheckCircle2, Lock } from 'lucide-react';

export const AuditReportGenerator: React.FC = () => {
  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-cyan-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <FileText className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Audit Report & Certificate Generator
                <Badge variant="success" size="sm">ISO/IEC 42001 Ready</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Export compliance-ready audit bundles, Merkle evidence proofs, and cryptographic replay certificates.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <button className="px-4 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-bold rounded-lg flex items-center gap-2 transition-all font-mono text-xs">
            <Download className="w-4 h-4" /> Export Signed Audit Bundle
          </button>
        </div>
      </div>

      {/* Audit Package Metadata */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 font-mono text-xs">
        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-2">
          <div className="text-slate-400 flex items-center gap-2">
            <Lock className="w-4 h-4 text-amber-400" /> Digital Signature
          </div>
          <div className="text-sm font-bold text-white truncate">sig_9f018ca210b490...</div>
          <p className="text-[11px] text-slate-500">Cryptographically bound to replay Merkle root.</p>
        </Card>

        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-2">
          <div className="text-slate-400 flex items-center gap-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" /> Truth Ledger Root
          </div>
          <div className="text-sm font-bold text-emerald-400 truncate">sha256:7fa189c4de91...</div>
          <p className="text-[11px] text-slate-500">Matches immutable on-chain event partition.</p>
        </Card>

        <Card className="p-5 bg-[#0F172A] border-[#1E293B] space-y-2">
          <div className="text-slate-400 flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-cyan-400" /> Regulatory Status
          </div>
          <div className="text-sm font-bold text-cyan-300">EU AI Act & SOC2 Compliant</div>
          <p className="text-[11px] text-slate-500">Full audit logging & determinism verified.</p>
        </Card>
      </div>

      {/* Compliance Frameworks Table */}
      <Card className="p-5 bg-[#0F172A] border-[#1E293B] font-mono text-xs space-y-3">
        <div className="font-bold text-slate-200">Adherence to Governance Standards</div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-slate-300">
          <div className="p-3 bg-slate-900/60 rounded border border-slate-800 space-y-1">
            <div className="font-bold text-white">ISO/IEC 42001</div>
            <div className="text-emerald-400">Traceability: 100%</div>
            <div className="text-emerald-400">Human Oversight: Verified</div>
          </div>
          <div className="p-3 bg-slate-900/60 rounded border border-slate-800 space-y-1">
            <div className="font-bold text-white">EU AI Act (Art. 12)</div>
            <div className="text-emerald-400">Record-Keeping: Pass</div>
            <div className="text-emerald-400">Auditability: Deterministic</div>
          </div>
          <div className="p-3 bg-slate-900/60 rounded border border-slate-800 space-y-1">
            <div className="font-bold text-white">SOC 2 Type II</div>
            <div className="text-emerald-400">Audit Trails: Immutable</div>
            <div className="text-emerald-400">Integrity: Cryptographic</div>
          </div>
        </div>
      </Card>
    </div>
  );
};
