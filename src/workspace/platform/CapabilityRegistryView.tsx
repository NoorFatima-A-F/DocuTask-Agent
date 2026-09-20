import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const CapabilityRegistryView: React.FC = () => {
  const capabilities = [
    {
      name: 'perception.ocr',
      category: 'Perception',
      description: 'Document image binarization, de-skewing, token segmentation, and bounding box coordinates.',
      providers: [
        { name: 'Tesseract V5 Enhanced', plugin: 'plugin.invoice.processing', latency: '120 ms', cost: '$0.00010', quality: '98.0%', status: 'OPTIMAL' },
        { name: 'Cloud Vision API', plugin: 'plugin.cloud_ocr', latency: '450 ms', cost: '$0.00250', quality: '99.5%', status: 'BACKUP' },
      ],
    },
    {
      name: 'extraction.invoice',
      category: 'Extraction',
      description: 'Structured financial extraction including vendor name, tax ID, line items, and totals.',
      providers: [
        { name: 'InvoicePro Structured Extractor', plugin: 'plugin.invoice.processing', latency: '280 ms', cost: '$0.00180', quality: '99.1%', status: 'OPTIMAL' },
      ],
    },
    {
      name: 'validation.reconciliation',
      category: 'Validation',
      description: 'Invariant mathematical proof: subtotal + taxes == invoice total, Mod11 checksum.',
      providers: [
        { name: 'Mod11 Invariant Validator', plugin: 'plugin.invoice.processing', latency: '18 ms', cost: '$0.00000', quality: '100.0%', status: 'OPTIMAL' },
      ],
    },
    {
      name: 'privacy.deidentify',
      category: 'Privacy & Security',
      description: 'Zero-knowledge PHI redaction and HIPAA compliance boundary enforcement.',
      providers: [
        { name: 'HIPAA Shield Enclave', plugin: 'plugin.medical.records', latency: '65 ms', cost: '$0.00020', quality: '99.8%', status: 'OPTIMAL' },
      ],
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Dynamic Capability Registry</h1>
            <Badge variant="success" size="sm">Pareto Resolver Active</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Abstract capabilities registered by plugins. The planner dynamically binds to the optimal provider based on real-time cost, latency, and quality.
          </p>
        </div>
        <Badge variant="intelligence" size="md">
          {capabilities.length} Abstract Capabilities
        </Badge>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {capabilities.map((cap) => (
          <Card key={cap.name} className="p-5 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="font-mono text-sm font-bold text-foreground">{cap.name}</span>
                <Badge variant="outline" size="sm">{cap.category}</Badge>
              </div>
              <span className="text-xs text-muted-foreground font-mono">{cap.providers.length} Provider(s)</span>
            </div>
            <p className="text-xs text-muted-foreground">{cap.description}</p>

            <div className="border border-border/40 rounded-lg overflow-hidden mt-2">
              <table className="w-full text-left text-xs font-mono">
                <thead className="bg-muted/40 text-muted-foreground">
                  <tr>
                    <th className="p-2.5">Provider Implementation</th>
                    <th className="p-2.5">Plugin Source</th>
                    <th className="p-2.5">P95 Latency</th>
                    <th className="p-2.5">Cost / Call</th>
                    <th className="p-2.5">Quality</th>
                    <th className="p-2.5">Planner Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border/40">
                  {cap.providers.map((prov) => (
                    <tr key={prov.name}>
                      <td className="p-2.5 font-bold text-foreground">{prov.name}</td>
                      <td className="p-2.5 text-muted-foreground">{prov.plugin}</td>
                      <td className="p-2.5">{prov.latency}</td>
                      <td className="p-2.5">{prov.cost}</td>
                      <td className="p-2.5 text-emerald-400 font-bold">{prov.quality}</td>
                      <td className="p-2.5">
                        <Badge variant={prov.status === 'OPTIMAL' ? 'success' : 'outline'} size="sm">
                          {prov.status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
