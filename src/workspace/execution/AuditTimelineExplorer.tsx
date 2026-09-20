import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  ShieldCheck,
  RotateCw,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { AuditEntry } from '../../types/executionPlatform';

export const AuditTimelineExplorer: React.FC = () => {
  const [entries, setEntries] = useState<AuditEntry[]>([]);
  const [ledgerValid, setLedgerValid] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [eRes, vRes] = await Promise.all([
        executionPlatformApiClient.listAuditEntries({ limit: 100 }),
        executionPlatformApiClient.verifyAuditLedger(),
      ]);
      setEntries(eRes.entries || []);
      setLedgerValid(vRes.ledger_valid);
    } catch (err) {
      console.error('Failed to load audit ledger:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <ShieldCheck className="w-5 h-5 text-cyan-400" />
            Cryptographic Audit Timeline & Compliance Ledger
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Tamper-evident SHA-256 block chain verification, SOC2/HIPAA evidence trails & provenance records
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant={ledgerValid ? 'success' : 'error'} className="py-1 px-3 text-xs">
            {ledgerValid ? 'Ledger Chain 100% Cryptographically Valid' : 'Ledger Inconsistency Detected'}
          </Badge>
          <Button variant="outline" onClick={loadData}>
            <span className="flex items-center gap-2">
              <RotateCw className="w-4 h-4" />
              Re-Verify
            </span>
          </Button>
        </div>
      </div>

      {loading && entries.length === 0 && (
        <p className="text-xs text-slate-500 py-4 text-center">Loading audit ledger...</p>
      )}

      {/* Audit Entries List */}
      <Card className="bg-slate-900/60 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white">Chained Block Entries ({entries.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {entries.map((e, idx) => (
              <div
                key={e.entry_id}
                className="p-4 bg-slate-950 border border-slate-800 rounded-xl space-y-2 text-xs"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-5 h-5 rounded-full bg-cyan-950 border border-cyan-500 flex items-center justify-center font-mono font-bold text-[10px] text-cyan-200">
                      {idx + 1}
                    </span>
                    <span className="font-semibold text-white uppercase tracking-wider">{e.action_type}</span>
                    <span className="text-slate-400">by {e.actor}</span>
                  </div>
                  <Badge variant="outline">{e.risk_level} risk</Badge>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] font-mono pt-1">
                  <div className="text-slate-400 truncate">
                    <span className="text-slate-600 block text-[9px]">PREV HASH</span>
                    {e.prev_hash}
                  </div>
                  <div className="text-cyan-400 truncate">
                    <span className="text-slate-600 block text-[9px]">BLOCK SIGNATURE SHA-256</span>
                    {e.hash_signature}
                  </div>
                </div>

                {e.payload_summary && Object.keys(e.payload_summary).length > 0 && (
                  <pre className="p-2 bg-slate-900 rounded text-slate-300 text-[10px] overflow-x-auto">
                    {JSON.stringify(e.payload_summary, null, 2)}
                  </pre>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};
