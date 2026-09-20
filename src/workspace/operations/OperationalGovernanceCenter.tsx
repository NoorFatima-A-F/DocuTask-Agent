import React, { useState } from 'react';
import {
  ShieldAlert,
  CheckCircle2,
  RefreshCw,
  Lock,
  Award
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface OperationalGovernanceCenterProps {
  missionId?: string;
}

export const OperationalGovernanceCenter: React.FC<OperationalGovernanceCenterProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [policies] = useState([
    {
      id: 'POL-OP-001',
      name: 'Automated Sub-Second Self-Healing',
      rule: 'Execute automated restarts on single worker thread failure without human blocking',
      isHardGuardrail: true,
      enforced: true,
      violations: 0,
    },
    {
      id: 'POL-OP-002',
      name: 'Zero Data Loss Checkpoint Guarantee',
      rule: 'Rollback only to verified cryptographic SHA-256 snapshots from Phase 13.4',
      isHardGuardrail: true,
      enforced: true,
      violations: 0,
    },
    {
      id: 'POL-OP-003',
      name: 'SLA Latency Circuit Breaker',
      rule: 'Engage quantized fallback models when P99 latency exceeds 3000ms for 3 consecutive minutes',
      isHardGuardrail: false,
      enforced: true,
      violations: 0,
    },
  ]);

  const [compliance] = useState({
    soc2Pct: 100.0,
    iso27001Pct: 100.0,
    iso42001Pct: 98.5,
    nistAiRmfPct: 99.0,
    merkleRoot: '0x8f1a029cb384ef7a91c55d015a3bf4f1b2b0b822cd15d6c15b0f00a08',
    auditedEvents: 1420,
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <ShieldAlert className="w-5 h-5 text-emerald-400" />
            Operational Governance & SRE Compliance Center
          </h2>
          <p className="text-sm text-slate-400">
            Automated safety boundaries, multi-standard compliance scoring (SOC2, ISO 27001, ISO 42001, NIST AI RMF), and append-only cryptographic audits for: <code className="text-emerald-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Governance Status: 100% COMPLIANT
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Audit Merkle Root
          </button>
        </div>
      </div>

      {/* Compliance Scorecards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 font-mono">
        <Card className="p-4 bg-slate-900 border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 block">SOC 2 Type II</span>
          <span className="text-2xl font-bold text-emerald-400">{compliance.soc2Pct}%</span>
          <span className="text-[10px] text-slate-500 block">Security & Availability</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 block">ISO / IEC 27001</span>
          <span className="text-2xl font-bold text-cyan-400">{compliance.iso27001Pct}%</span>
          <span className="text-[10px] text-slate-500 block">Information Security</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 block">ISO / IEC 42001</span>
          <span className="text-2xl font-bold text-purple-400">{compliance.iso42001Pct}%</span>
          <span className="text-[10px] text-slate-500 block">AI Governance System</span>
        </Card>

        <Card className="p-4 bg-slate-900 border-slate-800 space-y-1">
          <span className="text-xs text-slate-400 block">NIST AI RMF 1.0</span>
          <span className="text-2xl font-bold text-indigo-400">{compliance.nistAiRmfPct}%</span>
          <span className="text-[10px] text-slate-500 block">AI Risk Management</span>
        </Card>
      </div>

      {/* Merkle Root Provenance Banner */}
      <Card className="p-4 bg-slate-900 border-slate-800 flex items-center justify-between font-mono">
        <div className="flex items-center gap-3">
          <div className="p-2 rounded-lg bg-indigo-950/60 border border-indigo-500/30 text-indigo-400">
            <Lock className="w-5 h-5" />
          </div>
          <div>
            <span className="text-xs text-slate-400 block">Append-Only Merkle Audit Root</span>
            <code className="text-xs font-bold text-slate-200">{compliance.merkleRoot}</code>
          </div>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 block">Audited Operations</span>
          <span className="text-xs font-bold text-emerald-400">{compliance.auditedEvents} Events Logged</span>
        </div>
      </Card>

      {/* Active Operational Policies */}
      <div className="space-y-3 font-mono">
        <h3 className="text-sm font-semibold text-slate-200 flex items-center gap-2">
          <Award className="w-4 h-4 text-emerald-400" />
          Enforced Operational SRE Policies & Guardrails
        </h3>

        {policies.map((pol) => (
          <Card key={pol.id} className="p-4 bg-slate-900 border-slate-800 flex items-center justify-between">
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-indigo-400">{pol.id}</span>
                <span className="text-xs font-bold text-slate-200">{pol.name}</span>
                {pol.isHardGuardrail && <Badge variant="error" size="sm">Hard Guardrail</Badge>}
              </div>
              <p className="text-xs text-slate-400">{pol.rule}</p>
            </div>

            <div className="text-right space-y-1">
              <Badge variant="success" size="sm">
                <CheckCircle2 className="w-3 h-3 mr-1" />
                ENFORCED
              </Badge>
              <span className="text-[10px] text-slate-500 block">{pol.violations} Violations</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
