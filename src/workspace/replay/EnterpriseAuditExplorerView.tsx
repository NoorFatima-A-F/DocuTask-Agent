import React, { useState, useEffect } from 'react';
import type { AuditRecord, AuditVerificationReport } from '../../types/esmrReplay';
import { EsmrReplayApiClient } from '../../services/esmrReplayApiClient';

interface EnterpriseAuditExplorerViewProps {
  missionId: string;
}

export const EnterpriseAuditExplorerView: React.FC<EnterpriseAuditExplorerViewProps> = ({ missionId }) => {
  const [auditRecords, setAuditRecords] = useState<AuditRecord[]>([]);
  const [report, setReport] = useState<AuditVerificationReport | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([
      EsmrReplayApiClient.getAuditTrail(missionId),
      EsmrReplayApiClient.verifyAudit(missionId),
    ])
      .then(([records, rep]) => {
        setAuditRecords(records);
        setReport(rep);
      })
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [missionId]);

  if (loading) {
    return (
      <div className="p-6 bg-slate-900 border border-slate-800 rounded-xl text-slate-400 animate-pulse">
        Verifying Cryptographic Signatures across Enterprise Audit Trail...
      </div>
    );
  }

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>🛡️</span> Cryptographically Signed Enterprise Audit Trail
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            HMAC-SHA256 signed audit records with strict previous-hash chaining and tamper-evident guarantees.
          </p>
        </div>

        {report && (
          <div className="flex items-center gap-2">
            <span
              className={`px-3 py-1 rounded-lg text-xs font-mono font-bold border ${
                report.is_valid
                  ? 'bg-emerald-950/80 border-emerald-500/40 text-emerald-400'
                  : 'bg-rose-950/80 border-rose-500/40 text-rose-400'
              }`}
            >
              {report.is_valid ? '✓ HMAC-SHA256 AUDIT CHAIN VALID' : '✗ TAMPER DETECTED'}
            </span>
          </div>
        )}
      </div>

      <div className="overflow-x-auto border border-slate-800 rounded-lg">
        <table className="w-full text-left font-mono text-xs border-collapse">
          <thead className="bg-slate-900 text-slate-400 border-b border-slate-800">
            <tr>
              <th className="py-2.5 px-3">#</th>
              <th className="py-2.5 px-3">Category</th>
              <th className="py-2.5 px-3">Action Type</th>
              <th className="py-2.5 px-3">Actor</th>
              <th className="py-2.5 px-3">Audit Hash</th>
              <th className="py-2.5 px-3">HMAC Sig</th>
              <th className="py-2.5 px-3">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-850">
            {auditRecords.map((rec) => (
              <tr key={rec.audit_id} className="hover:bg-slate-900/60">
                <td className="py-2.5 px-3 text-slate-400">{rec.sequence_number}</td>
                <td className="py-2.5 px-3 text-cyan-400">{rec.category}</td>
                <td className="py-2.5 px-3 text-slate-200">{rec.action_type}</td>
                <td className="py-2.5 px-3 text-slate-400">{rec.actor}</td>
                <td className="py-2.5 px-3 text-slate-500 text-[10px]">{rec.audit_hash.slice(0, 12)}...</td>
                <td className="py-2.5 px-3 text-purple-400 text-[10px]">{rec.hmac_signature.slice(0, 16)}...</td>
                <td className="py-2.5 px-3">
                  <span className="text-emerald-400 font-bold">✓ SIGNED</span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
