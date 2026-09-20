import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { AuditEvent } from '../../types/saasPlatform';
import { ShieldAlert, CheckCircle2, RefreshCw, FileCheck } from 'lucide-react';

export const EnterpriseAuditExplorer: React.FC = () => {
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [integrity, setIntegrity] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    setLoading(true);
    const [evList, integ] = await Promise.all([
      SaaSApiClient.listAuditEvents('tenant_acme_corp'),
      SaaSApiClient.verifyAuditIntegrity('tenant_acme_corp'),
    ]);
    setEvents(evList);
    setIntegrity(integ);
    setLoading(false);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <ShieldAlert className="w-7 h-7 text-indigo-400" />
            Immutable Enterprise Audit Ledger & SOC2 Proof
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Cryptographic SHA-256 hash-chained tamper-evident audit trail for enterprise governance.
          </p>
        </div>
        <div className="flex items-center gap-3">
          {integrity && integrity.valid ? (
            <Badge variant="success" className="px-3 py-1 flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4" /> Hash Chain Verified
            </Badge>
          ) : (
            <Badge variant="error" className="px-3 py-1">Integrity Compromised</Badge>
          )}
          <Button variant="outline" onClick={loadData}>
            <span className="flex items-center gap-2">
              <RefreshCw className="w-4 h-4" /> Re-Verify Chain
            </span>
          </Button>
        </div>
      </div>

      <Card className="bg-slate-900/80 border-slate-800">
        <CardHeader>
          <CardTitle className="text-base text-white flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-emerald-400" /> Cryptographic Event Trail ({events.length})
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {loading ? (
            <div className="p-8 text-center text-slate-400">Loading audit ledger...</div>
          ) : (
            events.map((ev) => (
              <div
                key={ev.audit_id}
                className="p-4 bg-slate-800/40 rounded border border-slate-700/50 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Badge variant="intelligence">{ev.action}</Badge>
                    <span className="text-sm font-semibold text-white">{ev.actor_email}</span>
                  </div>
                  <span className="text-xs text-slate-400">{new Date(ev.timestamp).toLocaleString()}</span>
                </div>
                <div className="text-xs text-slate-400 grid grid-cols-2 gap-2">
                  <div>Resource: <span className="text-slate-200 font-mono">{ev.resource_type}:{ev.resource_id}</span></div>
                  <div>IP Address: <span className="text-slate-200 font-mono">{ev.ip_address}</span></div>
                </div>
                <div className="pt-2 border-t border-slate-700/40 text-[10px] text-slate-500 font-mono truncate">
                  SHA-256 Hash: <span className="text-cyan-400">{ev.event_hash}</span>
                </div>
              </div>
            ))
          )}
        </CardContent>
      </Card>
    </div>
  );
};
