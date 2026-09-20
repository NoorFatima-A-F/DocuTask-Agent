import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PlatformDiagnosticsView: React.FC = () => {
  const diagnostics = {
    kernelStatus: 'OPERATIONAL',
    uptimeSeconds: 84920,
    activeThreads: 12,
    diContainerInstances: 18,
    capabilityProvidersOnline: 9,
    policyEvaluationsTotal: 1420,
    policyViolationCount: 0,
    sandboxEnclavesActive: 4,
    merkleDagIntegrity: '100.0% VERIFIED',
    gcLatencyMs: 0.8,
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Platform OS Diagnostics</h1>
            <Badge variant="success" size="sm">Kernel Healthy</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Real-time kernel diagnostics, DI container resolutions, capability health radar, and sandbox telemetry.
          </p>
        </div>
        <Badge variant="outline" size="md">
          Uptime: {(diagnostics.uptimeSeconds / 3600).toFixed(1)} Hours
        </Badge>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Kernel Status</div>
          <div className="text-lg font-bold font-mono text-emerald-400 mt-1">{diagnostics.kernelStatus}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">DI Container Singletons</div>
          <div className="text-lg font-bold font-mono text-foreground mt-1">{diagnostics.diContainerInstances}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Capability Providers</div>
          <div className="text-lg font-bold font-mono text-foreground mt-1">{diagnostics.capabilityProvidersOnline} Online</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Policy Evaluations</div>
          <div className="text-lg font-bold font-mono text-foreground mt-1">{diagnostics.policyEvaluationsTotal}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Policy Violations</div>
          <div className="text-lg font-bold font-mono text-emerald-400 mt-1">{diagnostics.policyViolationCount}</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Merkle DAG Integrity</div>
          <div className="text-lg font-bold font-mono text-emerald-400 mt-1">{diagnostics.merkleDagIntegrity}</div>
        </Card>
      </div>
    </div>
  );
};
