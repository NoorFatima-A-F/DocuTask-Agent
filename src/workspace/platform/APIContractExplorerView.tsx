import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const APIContractExplorerView: React.FC = () => {
  const [selectedFormat, setSelectedFormat] = useState<'OPENAPI' | 'JSON_SCHEMA' | 'PYTHON_SDK'>('OPENAPI');

  const openApiSpec = {
    openapi: '3.1.0',
    info: { title: 'DocuTask Agent Platform OS API', version: '2026.1' },
    paths: {
      '/api/v1/platform/plugins': { get: { summary: 'List active domain plugins' } },
      '/api/v1/platform/capabilities': { get: { summary: 'Query dynamic capability registry' } },
      '/api/v1/agents/plugin.invoice.processing/execute': { post: { summary: 'Execute Invoice Agent' } },
      '/api/v1/agents/plugin.medical.records/execute': { post: { summary: 'Execute HIPAA Clinical Agent' } },
    },
  };

  const pythonSdkStub = `# Auto-Generated DocuTask Platform Client (Python 3.8+)
from docutask import PlatformClient

client = PlatformClient(base_url="https://api.docutask.internal")

# Execute Invoice Agent via dynamic capability
result = client.execute_capability(
    capability="extraction.invoice",
    payload={"doc_url": "s3://invoices/inv-8891.pdf"}
)
print("Reconciled Total:", result.data.total_usd)`;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">API Contract Explorer</h1>
            <Badge variant="success" size="sm">Auto-Generated Schemas</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Zero handwritten documentation — OpenAPI 3.1, JSON Schema, and Python/TypeScript client stubs generated dynamically.
          </p>
        </div>
        <div className="flex items-center gap-2">
          {(['OPENAPI', 'JSON_SCHEMA', 'PYTHON_SDK'] as const).map((fmt) => (
            <button
              key={fmt}
              onClick={() => setSelectedFormat(fmt)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold font-mono transition-all cursor-pointer ${
                selectedFormat === fmt
                  ? 'bg-primary text-primary-foreground'
                  : 'bg-muted/40 text-muted-foreground hover:bg-muted/80'
              }`}
            >
              {fmt}
            </button>
          ))}
        </div>
      </div>

      <Card className="p-6 space-y-4">
        <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          {selectedFormat === 'OPENAPI' ? 'OpenAPI 3.1 Specification' : selectedFormat === 'JSON_SCHEMA' ? 'JSON Schemas' : 'Python Client SDK'}
        </div>
        <pre className="p-4 bg-black/90 rounded-lg border border-border/40 font-mono text-xs text-emerald-400 overflow-x-auto leading-relaxed">
          {selectedFormat === 'OPENAPI'
            ? JSON.stringify(openApiSpec, null, 2)
            : selectedFormat === 'JSON_SCHEMA'
            ? JSON.stringify({ PluginManifest: { type: 'object' }, CapabilityProvider: { type: 'object' } }, null, 2)
            : pythonSdkStub}
        </pre>
      </Card>
    </div>
  );
};
