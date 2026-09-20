import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const SandboxInspectorView: React.FC = () => {
  const quotas = {
    maxCpuMs: '3000 ms',
    maxMemoryMb: '256 MB',
    maxTokenSpendUsd: '$0.0500',
    networkEgress: 'BLOCKED (Air-Gapped)',
    filesystemAccess: 'ISOLATED_TMP_ONLY',
    violationsDetected: 0,
  };

  const activeEnclaves = [
    { pluginId: 'plugin.invoice.processing', pid: 'sb-9921', ramUsed: '48.2 MB', cpuP95: '124 ms', scopes: ['ocr:read', 'storage:write', 'evidence:seal'], status: 'ISOLATED' },
    { pluginId: 'plugin.medical.records', pid: 'sb-9922', ramUsed: '36.8 MB', cpuP95: '65 ms', scopes: ['ocr:read', 'phi:anonymize'], status: 'ISOLATED' },
    { pluginId: 'plugin.resume.screener', pid: 'sb-9923', ramUsed: '52.1 MB', cpuP95: '190 ms', scopes: ['ocr:read'], status: 'ISOLATED' },
    { pluginId: 'plugin.legal.contracts', pid: 'sb-9924', ramUsed: '44.0 MB', cpuP95: '140 ms', scopes: ['ocr:read', 'storage:write'], status: 'ISOLATED' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Sandbox Isolation Inspector</h1>
            <Badge variant="success" size="sm">Hard Boundary Active</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time memory, CPU, network, and secret boundaries enforced on all untrusted third-party plugins.
          </p>
        </div>
        <Badge variant="outline" size="md">
          Air-Gapped Enclaves: 4
        </Badge>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Max CPU Quota</div>
          <div className="text-lg font-bold font-mono text-foreground mt-1">{quotas.maxCpuMs}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Max Memory Quota</div>
          <div className="text-lg font-bold font-mono text-foreground mt-1">{quotas.maxMemoryMb}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Network Egress</div>
          <div className="text-sm font-bold font-mono text-emerald-400 mt-1">{quotas.networkEgress}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Security Breaches</div>
          <div className="text-lg font-bold font-mono text-emerald-400 mt-1">{quotas.violationsDetected}</div>
        </Card>
      </div>

      <Card className="p-6 space-y-4">
        <div className="text-sm font-bold text-foreground">
          Active Plugin Sandbox Enclaves
        </div>
        <div className="border border-border/40 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-muted/40 text-muted-foreground">
              <tr>
                <th className="p-3">Enclave ID</th>
                <th className="p-3">Plugin ID</th>
                <th className="p-3">RAM Usage</th>
                <th className="p-3">P95 CPU</th>
                <th className="p-3">Granted Permission Scopes</th>
                <th className="p-3">Isolation Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {activeEnclaves.map((e) => (
                <tr key={e.pid}>
                  <td className="p-3 font-bold text-foreground">{e.pid}</td>
                  <td className="p-3 text-primary">{e.pluginId}</td>
                  <td className="p-3">{e.ramUsed}</td>
                  <td className="p-3">{e.cpuP95}</td>
                  <td className="p-3">
                    <div className="flex flex-wrap gap-1">
                      {e.scopes.map((s) => (
                        <Badge key={s} variant="outline" size="sm">{s}</Badge>
                      ))}
                    </div>
                  </td>
                  <td className="p-3">
                    <Badge variant="success" size="sm">{e.status}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
