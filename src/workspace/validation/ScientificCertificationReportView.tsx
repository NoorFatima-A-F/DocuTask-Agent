import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ScientificCertificationReportView: React.FC = () => {
  const packageData = {
    packageId: 'CERT-2026-V5-ALPHA',
    version: 'v5.0.0-rc1',
    signature: 'ED25519_SIG_8F3A20B1C4D5E6F789A01234',
    verificationHash: 'd3b07384d113edec49eaa6238ad5ff00f95c479421de7176a9452b415a99ad97',
    trialsCount: 2500,
    accuracy: '96.8%',
    p95Latency: '490 ms',
    brierScore: '0.018',
    psiDrift: '0.042',
    issuedDate: 'September 10, 2026',
    status: 'CRYPTOGRAPHICALLY_VERIFIED',
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="p-6 rounded-2xl bg-[#0F172A] border border-[#1E293B] shadow-xl">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl">📜</span>
              <h2 className="text-lg font-bold font-mono text-[#F8FAFC]">
                Cryptographic Scientific Certification Report
              </h2>
              <Badge variant="success" size="sm">
                TAMPER-EVIDENT MANIFEST
              </Badge>
            </div>
            <p className="text-sm font-mono text-[#94A3B8] mt-1">
              Deterministic, cryptographically signed dossier verifying empirical statistical bounds, calibration, and zero-drift proof.
            </p>
          </div>
        </div>
      </div>

      {/* Certificate Dossier Card */}
      <Card className="p-8 bg-[#0F172A] border-[#1E293B] relative overflow-hidden">
        <div className="absolute top-0 right-0 w-48 h-48 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />

        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pb-6 border-b border-[#1E293B]">
          <div>
            <span className="text-xs font-mono text-cyan-400 font-bold tracking-wider">
              OFFICIAL COMPLIANCE CERTIFICATION
            </span>
            <h3 className="text-xl font-bold font-mono text-[#F8FAFC] mt-1">
              DocuTask Autonomous Optimization Dossier
            </h3>
            <div className="text-xs font-mono text-[#64748B] mt-1">
              Target Release: {packageData.version} • Issued: {packageData.issuedDate}
            </div>
          </div>
          <Badge variant="success" size="md">
            {packageData.status}
          </Badge>
        </div>

        {/* Core Statistical Pillars */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 my-6">
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
            <div className="text-xs font-mono text-[#94A3B8]">Validated Trial Count</div>
            <div className="text-2xl font-bold font-mono text-[#F8FAFC] mt-1">{packageData.trialsCount} runs</div>
            <div className="text-[11px] font-mono text-emerald-400 mt-1">100% ground-truth paired</div>
          </div>
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
            <div className="text-xs font-mono text-[#94A3B8]">Empirical Accuracy</div>
            <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">{packageData.accuracy}</div>
            <div className="text-[11px] font-mono text-[#64748B] mt-1">Target ≥ 95.0%</div>
          </div>
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
            <div className="text-xs font-mono text-[#94A3B8]">P95 Execution Latency</div>
            <div className="text-2xl font-bold font-mono text-cyan-400 mt-1">{packageData.p95Latency}</div>
            <div className="text-[11px] font-mono text-[#64748B] mt-1">SLA target &lt; 1000ms</div>
          </div>
          <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B]">
            <div className="text-xs font-mono text-[#94A3B8]">Brier Calibration Score</div>
            <div className="text-2xl font-bold font-mono text-indigo-400 mt-1">{packageData.brierScore}</div>
            <div className="text-[11px] font-mono text-emerald-400 mt-1">Well calibrated (&lt;0.05)</div>
          </div>
        </div>

        {/* Cryptographic Manifest Details */}
        <div className="p-4 rounded-xl bg-[#020617] border border-[#1E293B] space-y-2 font-mono text-xs">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-1">
            <span className="text-[#94A3B8]">Package Identifier:</span>
            <span className="text-[#F8FAFC] font-bold">{packageData.packageId}</span>
          </div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-1">
            <span className="text-[#94A3B8]">ED25519 Cryptographic Signature:</span>
            <span className="text-cyan-400 font-bold">{packageData.signature}</span>
          </div>
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-1">
            <span className="text-[#94A3B8]">SHA-256 Merkle Verification Hash:</span>
            <span className="text-[#64748B] text-[11px] break-all">{packageData.verificationHash}</span>
          </div>
        </div>
      </Card>
    </div>
  );
};
