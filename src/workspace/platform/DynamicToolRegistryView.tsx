import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const DynamicToolRegistryView: React.FC = () => {
  const tools = [
    {
      id: 'tool.llm.gemini_2_5_flash',
      name: 'Google Gemini 2.5 Flash API',
      category: 'LLM_INTELLIGENCE',
      description: 'High-speed multi-modal reasoning and structured JSON entity extraction.',
      costPerCall: '$0.00018',
      p95Latency: '180 ms',
      rateLimit: '1000 RPM',
      permissions: ['ai:generate'],
      status: 'ONLINE',
    },
    {
      id: 'tool.ocr.tesseract_v5',
      name: 'Tesseract V5 Enhanced OCR Engine',
      category: 'OPTICAL_PERCEPTION',
      description: 'Local OpenCV-accelerated binary segmentation and token bounding-box generator.',
      costPerCall: '$0.00004',
      p95Latency: '120 ms',
      rateLimit: '5000 RPM',
      permissions: ['ocr:read'],
      status: 'ONLINE',
    },
    {
      id: 'tool.storage.gdrive',
      name: 'Google Drive Enterprise Sync',
      category: 'STORAGE',
      description: 'Secure automated cloud document ingestion and PDF export destination.',
      costPerCall: '$0.00001',
      p95Latency: '220 ms',
      rateLimit: '300 RPM',
      permissions: ['drive:rw'],
      status: 'ONLINE',
    },
    {
      id: 'tool.notification.slack',
      name: 'Slack Incident & Handoff Webhook',
      category: 'COMMUNICATION',
      description: 'Broadcasts human-in-the-loop review alerts and executive status summaries.',
      costPerCall: '$0.00000',
      p95Latency: '95 ms',
      rateLimit: '60 RPM',
      permissions: ['slack:write'],
      status: 'ONLINE',
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Dynamic Tool Registry</h1>
            <Badge variant="success" size="sm">Declarative Integrations</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Pluggable external and local tools. Each tool advertises cost models, permission scopes, rate limits, and latency percentiles.
          </p>
        </div>
        <Badge variant="outline" size="md">
          {tools.length} Dynamic Tools Registered
        </Badge>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {tools.map((t) => (
          <Card key={t.id} className="p-5 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <Badge variant="outline" size="sm" className="mb-1">{t.category}</Badge>
                <div className="font-bold text-sm text-foreground">{t.name}</div>
                <div className="font-mono text-[11px] text-muted-foreground mt-0.5">{t.id}</div>
              </div>
              <Badge variant="success" size="sm">{t.status}</Badge>
            </div>

            <p className="text-xs text-muted-foreground">{t.description}</p>

            <div className="grid grid-cols-3 gap-2 pt-2 border-t border-border/40 text-xs font-mono">
              <div>
                <span className="text-muted-foreground">Cost: </span>
                <span className="text-foreground">{t.costPerCall}</span>
              </div>
              <div>
                <span className="text-muted-foreground">P95: </span>
                <span className="text-foreground">{t.p95Latency}</span>
              </div>
              <div>
                <span className="text-muted-foreground">Limit: </span>
                <span className="text-foreground">{t.rateLimit}</span>
              </div>
            </div>

            <div className="flex items-center gap-1 text-[11px] font-mono text-muted-foreground">
              <span>Required Scope:</span>
              {t.permissions.map((p) => (
                <Badge key={p} variant="intelligence" size="sm">{p}</Badge>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
