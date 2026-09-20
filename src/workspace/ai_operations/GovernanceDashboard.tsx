import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Lock,
  FileCheck,
  RefreshCw,
  Hash,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { GovernanceAuditRecord } from '../../types/aiOperations';

export const GovernanceDashboard: React.FC = () => {
  const [logs, setLogs] = useState<GovernanceAuditRecord[]>([]);
  const [selectedLog, setSelectedLog] = useState<GovernanceAuditRecord | null>(null);
  const [loading, setLoading] = useState(true);

  const loadLogs = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getGovernanceAuditLogs(50);
      setLogs(data);
      if (data.length > 0 && !selectedLog) {
        setSelectedLog(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load governance logs:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-emerald-500/10 rounded-xl border border-emerald-500/20">
            <ShieldCheck className="w-6 h-6 text-emerald-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">AI Governance & Compliance Center</h1>
            <p className="text-xs text-slate-400">Cryptographic audit trails, PII sanitizer logs, policy enforcement, and regulatory compliance</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadLogs} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* KPI Policy Highlights */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Policy Adherence</span>
            <FileCheck className="w-5 h-5 text-emerald-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">100%</span>
            <Badge variant="success">Strict</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">Zero active security violations</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">PII Redaction Guard</span>
            <Lock className="w-5 h-5 text-indigo-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">Active</span>
            <Badge variant="intelligence">Continuous</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">Auto-redacts API keys, emails, cards</p>
        </Card>

        <Card className="p-5 bg-slate-900/40 border-slate-800">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-slate-400">Audit Verifiability</span>
            <Hash className="w-5 h-5 text-cyan-400" />
          </div>
          <div className="mt-2 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">SHA-256</span>
            <Badge variant="sentinel">Immutable</Badge>
          </div>
          <p className="mt-1 text-xs text-slate-500">Cryptographically signed logs</p>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Audit Logs Table / List (5 cols) */}
        <div className="lg:col-span-5 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Governance Audit Trail</h2>
          <div className="space-y-2 max-h-[550px] overflow-y-auto pr-1">
            {logs.map((l) => (
              <Card
                key={l.audit_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedLog?.audit_id === l.audit_id
                    ? 'bg-emerald-950/30 border-emerald-500/50 shadow-md shadow-emerald-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedLog(l)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{l.event_type}</span>
                  <Badge variant={l.compliance_passed ? 'success' : 'error'}>
                    {l.compliance_passed ? 'Compliant' : 'Violation'}
                  </Badge>
                </div>
                <p className="text-xs text-slate-300 mt-1 line-clamp-1">{l.action_summary}</p>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2">
                  <span className="font-mono text-slate-500">{l.actor}</span>
                  <span>{new Date(l.timestamp).toLocaleTimeString()}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Log Details (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          {selectedLog ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">{selectedLog.event_type}</Badge>
                    <h2 className="text-base font-bold text-white">{selectedLog.actor}</h2>
                  </div>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">Audit ID: {selectedLog.audit_id}</p>
                </div>
                <Badge variant={selectedLog.compliance_passed ? 'success' : 'error'}>
                  {selectedLog.compliance_passed ? 'Passed Audit' : 'Flagged'}
                </Badge>
              </div>

              {/* Action Summary */}
              <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <FileCheck className="w-3.5 h-3.5 text-emerald-400" /> Action Summary
                </h4>
                <p className="text-sm text-slate-200 leading-relaxed">{selectedLog.action_summary}</p>
              </div>

              {/* Policy & PII Status */}
              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400">Enforced Policy</span>
                  <p className="text-xs font-bold text-white mt-1 font-mono">{selectedLog.policy_name || 'DEFAULT'}</p>
                </div>
                <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/60">
                  <span className="text-xs text-slate-400">PII Interception</span>
                  <p className="text-xs font-bold text-white mt-1">
                    {selectedLog.pii_detected ? (
                      <span className="text-amber-400">Redacted ({selectedLog.pii_types_redacted.join(', ')})</span>
                    ) : (
                      <span className="text-emerald-400">Clean Payload</span>
                    )}
                  </p>
                </div>
              </div>

              {/* Cryptographic Signature */}
              <div className="p-4 bg-slate-950/60 rounded-xl border border-slate-800/80">
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1.5">
                  <Hash className="w-3.5 h-3.5 text-cyan-400" /> Cryptographic Integrity Signature
                </h4>
                <p className="text-xs font-mono text-cyan-300 break-all">{selectedLog.signature_hash}</p>
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <ShieldCheck className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select an audit log to inspect compliance details and cryptographic hashes.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
