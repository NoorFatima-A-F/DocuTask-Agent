import React from 'react';
import { Badge } from '../../components/ui/Badge';

export const TrustCenter: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">SECURITY &amp; COMPLIANCE PORTAL</Badge>
          <h1 className="text-2xl font-black text-white mt-1">Enterprise AI Trust Center</h1>
          <p className="text-sm text-[#94A3B8]">
            Cryptographic tenant isolation, zero training data retention, and immutable audit ledgers.
          </p>
        </div>
        <Badge variant="success" size="md">100 / 100 Trust Score</Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Compliance Certifications */}
        <div className="p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-4">
          <h2 className="text-base font-bold text-white">Regulatory Frameworks</h2>
          <div className="space-y-3">
            {[
              { name: 'SOC 2 Type II Certified', desc: 'Continuous security & availability controls', badge: 'Certified' },
              { name: 'HIPAA Security Rule', desc: 'Encrypted ePHI with BAA guarantees', badge: 'Compliant' },
              { name: 'GDPR Article 28 (DPA)', desc: 'Right to erasure & EU regional tenancy', badge: 'Compliant' },
              { name: 'ISO/IEC 27001', desc: 'Information security management system', badge: 'Aligned' },
            ].map((comp, idx) => (
              <div key={idx} className="p-3.5 rounded-xl bg-[#0A0F1D] border border-[#1E293B] flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-white block">{comp.name}</span>
                  <span className="text-[11px] text-[#94A3B8]">{comp.desc}</span>
                </div>
                <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-800/40">
                  {comp.badge}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Model Governance & Security Architecture */}
        <div className="lg:col-span-2 p-6 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-5">
          <h2 className="text-base font-bold text-white">AI Model Governance &amp; Guardrails</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
              <span className="text-xs font-bold text-cyan-400">Zero Data Retention (ZTR)</span>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                Enterprise API contracts guarantee that customer documents and prompts are never used for model training or retained on third-party servers.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
              <span className="text-xs font-bold text-emerald-400">Cryptographic Partitioning</span>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                Each enterprise tenant uses isolated KMS encryption keys (AES-256-GCM) with strict Row-Level Security across all vector indices and databases.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
              <span className="text-xs font-bold text-purple-400">Prompt Injection Defenses</span>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                100% defense against indirect prompt injections and jailbreaks through automated AST input sanitization and dual-stage guardrail agents.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#0A0F1D] border border-[#1E293B] space-y-2">
              <span className="text-xs font-bold text-amber-400">Immutable Audit Ledger</span>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                Every agent step, tool invocation, and human review decision is cryptographically signed and logged with SHA-256 tamper-evident checksums.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
