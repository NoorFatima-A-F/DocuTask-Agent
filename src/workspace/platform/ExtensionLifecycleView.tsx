import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ExtensionLifecycleView: React.FC = () => {
  const lifecycleActions = [
    { action: 'UPGRADE', pluginId: 'plugin.invoice.processing', details: 'Upgraded v1.3.2 -> v1.4.0 (Mod11 speedup)', time: '18:10:04 UTC', status: 'SUCCESS' },
    { action: 'ENABLE', pluginId: 'plugin.medical.records', details: 'Activated HIPAA de-identification sandbox', time: '18:12:20 UTC', status: 'SUCCESS' },
    { action: 'HOT_RELOAD', pluginId: 'plugin.resume.screener', details: 'Dynamic AST re-compiled in 14ms', time: '18:15:30 UTC', status: 'SUCCESS' },
    { action: 'LOCK_VERSION', pluginId: 'plugin.legal.contracts', details: 'Pinned to v1.1.5 (SHA-256 attested)', time: '18:18:10 UTC', status: 'SUCCESS' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Extension Lifecycle & Versioning</h1>
            <Badge variant="success" size="sm">Hot-Reload & Rollback Safe</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Zero-downtime hot reloading, automated rollback history, SemVer dependency locking, and dynamic lifecycle events.
          </p>
        </div>
        <Badge variant="outline" size="md">
          Zero Restart Required
        </Badge>
      </div>

      <div className="space-y-3">
        <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Recent Lifecycle Operations ({lifecycleActions.length})
        </div>
        {lifecycleActions.map((item, idx) => (
          <Card key={idx} className="p-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Badge variant="intelligence" size="sm">{item.action}</Badge>
              <div>
                <div className="font-mono text-xs font-bold text-foreground">{item.pluginId}</div>
                <div className="text-xs text-muted-foreground mt-0.5">{item.details}</div>
              </div>
            </div>
            <div className="text-right font-mono">
              <span className="text-xs text-muted-foreground">{item.time}</span>
              <div className="text-emerald-400 text-xs font-bold mt-0.5">✓ {item.status}</div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
