import React from 'react';

interface EnterpriseExportCenterViewProps {
  missionId: string;
}

export const EnterpriseExportCenterView: React.FC<EnterpriseExportCenterViewProps> = ({ missionId }) => {
  const handleDownload = (format: 'json' | 'csv' | 'compliance') => {
    window.open(`/api/v1/replay/missions/${encodeURIComponent(missionId)}/export?format=${format}`, '_blank');
  };

  return (
    <div className="bg-slate-950 border border-slate-800 rounded-xl p-6 shadow-2xl space-y-6 text-slate-100">
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <h3 className="text-lg font-bold text-white flex items-center gap-2">
            <span>📦</span> Enterprise Forensic Export Center
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Export complete tamper-evident audit packages, event logs, and decision DAGs for external compliance audits (SOC2 / ISO 27001).
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
          <div className="text-sm font-bold text-cyan-400 font-mono">Canonical JSON Bundle</div>
          <p className="text-xs text-slate-400">
            Complete replay state, decision DAG, and raw event log formatted with cryptographic signatures.
          </p>
          <button
            onClick={() => handleDownload('json')}
            className="w-full py-2 bg-cyan-600 hover:bg-cyan-500 text-white font-mono text-xs font-semibold rounded-lg transition-colors"
          >
            Download JSON Package
          </button>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
          <div className="text-sm font-bold text-emerald-400 font-mono">Tabular CSV Audit Log</div>
          <p className="text-xs text-slate-400">
            Tabular chronological audit record dump suitable for spreadsheet analysis and SIEM ingestion.
          </p>
          <button
            onClick={() => handleDownload('csv')}
            className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-mono text-xs font-semibold rounded-lg transition-colors"
          >
            Download CSV Log
          </button>
        </div>

        <div className="bg-slate-900 border border-slate-800 p-5 rounded-xl space-y-3">
          <div className="text-sm font-bold text-purple-400 font-mono">SOC2 Compliance Bundle</div>
          <p className="text-xs text-slate-400">
            Forensic package including HMAC-SHA256 signature chain verification reports and root hashes.
          </p>
          <button
            onClick={() => handleDownload('compliance')}
            className="w-full py-2 bg-purple-600 hover:bg-purple-500 text-white font-mono text-xs font-semibold rounded-lg transition-colors"
          >
            Export Compliance Report
          </button>
        </div>
      </div>
    </div>
  );
};
