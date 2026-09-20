import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const PlatformDashboardView: React.FC = () => {
  const stats = {
    kernelVersion: 'AAPEROS-2026.1-LTS',
    activePluginsCount: 4,
    registeredCapabilities: 9,
    dynamicTools: 4,
    enforcedPolicies: 4,
    sandboxesActive: 4,
    marketplacePackages: 4,
    systemState: 'KERNEL_HEALTHY',
    memoryUsageMb: 84.5,
    totalDispatchedMissions: 1420,
    zeroHardcodingCompliance: '100.0%',
  };

  const installedPlugins = [
    { id: 'plugin.invoice.processing', name: 'Enterprise Invoice & Billing Agent', version: '1.4.0', status: 'ACTIVE', caps: 3, author: 'DocuTask Core' },
    { id: 'plugin.resume.screener', name: 'HR Resume & ATS Evaluation Agent', version: '1.2.0', status: 'ACTIVE', caps: 2, author: 'TalentAI Labs' },
    { id: 'plugin.medical.records', name: 'Clinical Health Record & HIPAA Agent', version: '2.0.1', status: 'ACTIVE', caps: 2, author: 'MedSecure' },
    { id: 'plugin.legal.contracts', name: 'Commercial Contract & Clause Reviewer', version: '1.1.5', status: 'ACTIVE', caps: 2, author: 'LexisCorp AI' },
  ];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Agent Platform OS Kernel</h1>
            <Badge variant="success" size="sm">AAPEROS 2026.1</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Generic autonomous execution operating system with zero domain hardcoding — every document type, capability, and tool is an installable plugin.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            Zero Hardcoding: 100%
          </Badge>
          <Badge variant="outline" size="md">
            RAM: {stats.memoryUsageMb} MB
          </Badge>
        </div>
      </div>

      {/* KPI Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card className="p-4 border-primary/20">
          <div className="text-xs text-muted-foreground">Installed Plugins</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{stats.activePluginsCount}</div>
          <div className="text-[11px] text-emerald-400 mt-1">100% Certified</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Dynamic Capabilities</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{stats.registeredCapabilities}</div>
          <div className="text-[11px] text-muted-foreground mt-1">Pareto Resolved</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Active Policy Rules</div>
          <div className="text-2xl font-bold font-mono text-foreground mt-1">{stats.enforcedPolicies}</div>
          <div className="text-[11px] text-emerald-400 mt-1">✓ SOC2/HIPAA/Cost</div>
        </Card>
        <Card className="p-4">
          <div className="text-xs text-muted-foreground">Sandbox Enclaves</div>
          <div className="text-2xl font-bold font-mono text-emerald-400 mt-1">{stats.sandboxesActive}</div>
          <div className="text-[11px] text-muted-foreground mt-1">Zero Breach</div>
        </Card>
      </div>

      {/* Active Plugins Matrix */}
      <Card className="p-6 space-y-4">
        <div className="flex items-center justify-between">
          <div className="text-sm font-bold text-foreground">
            Installed Domain Plugins (Dynamic Extensibility Engine)
          </div>
          <Badge variant="intelligence" size="sm">Hot-Reload Active</Badge>
        </div>

        <div className="border border-border/40 rounded-lg overflow-hidden">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-muted/50 border-b border-border/40 text-muted-foreground">
              <tr>
                <th className="p-3">Plugin ID</th>
                <th className="p-3">Display Name</th>
                <th className="p-3">Version</th>
                <th className="p-3">Author</th>
                <th className="p-3">Capabilities</th>
                <th className="p-3">Runtime Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/40">
              {installedPlugins.map((p) => (
                <tr key={p.id}>
                  <td className="p-3 text-foreground font-bold">{p.id}</td>
                  <td className="p-3 font-sans text-foreground">{p.name}</td>
                  <td className="p-3 text-muted-foreground">v{p.version}</td>
                  <td className="p-3 text-muted-foreground">{p.author}</td>
                  <td className="p-3 text-primary">{p.caps} Provided</td>
                  <td className="p-3">
                    <Badge variant="success" size="sm">
                      {p.status}
                    </Badge>
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
