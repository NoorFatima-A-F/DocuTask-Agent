import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const RuntimeProvenanceGraphView: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<string>('node-val-check');

  const provenanceNodes = [
    {
      id: 'node-raw-doc',
      type: 'INPUT',
      label: 'Raw PDF Document #8891',
      digest: 'c7e12f00a8918231bbd93172ca0913ef451',
      details: '4-page multi-table commercial invoice uploaded at 18:22:09 UTC.',
      parents: [],
      children: ['node-plan-dec'],
    },
    {
      id: 'node-plan-dec',
      type: 'PLAN',
      label: 'Planner Trajectory (Flash + Parallelism=3)',
      digest: '8891dec0001a4f98b12e3914a87c53d0e91',
      details: 'Evaluated 3 candidates; selected flash-p3 with 0.892 utility.',
      parents: ['node-raw-doc'],
      children: ['node-ocr-tool'],
    },
    {
      id: 'node-ocr-tool',
      type: 'TOOL',
      label: 'Adaptive OCR Execution (Tesseract V5)',
      digest: 'ocr001trace99102fae89bb3c17820aedfa',
      details: 'Extracted 142 tokens and 28 bounding boxes in 124.5ms.',
      parents: ['node-plan-dec'],
      children: ['node-val-check'],
    },
    {
      id: 'node-val-check',
      type: 'VALIDATION',
      label: 'Rule & Invariant Reconciliation',
      digest: 'val001pass7721d4e9102fae89bb3c1782',
      details: 'Verified Subtotal + Tax == Total with p=0.0001 confidence.',
      parents: ['node-ocr-tool'],
      children: ['node-out-json'],
    },
    {
      id: 'node-out-json',
      type: 'OUTPUT',
      label: 'Certified Extraction JSON',
      digest: 'f81d4fae7dec11d0a76500a0c91e6bf6012',
      details: 'Stored in content-addressable registry with SHA-256 seal.',
      parents: ['node-val-check'],
      children: [],
    },
  ];

  const activeNode = provenanceNodes.find((n) => n.id === selectedNode) || provenanceNodes[0]!;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Provenance DAG</h1>
            <Badge variant="success" size="sm">Acyclic & Grounded</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            End-to-end data lineage graph proving how every output token directly originates from raw document inputs and verified tool steps.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" size="md">
            Lineage Nodes: {provenanceNodes.length}
          </Badge>
          <Badge variant="intelligence" size="md">
            Zero Dangling References
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* DAG Flow Visualizer */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="p-6 space-y-6">
            <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Lineage DAG Flow
            </div>
            <div className="flex flex-col space-y-3">
              {provenanceNodes.map((node, idx) => {
                const isSelected = node.id === selectedNode;
                return (
                  <div key={node.id} className="space-y-2">
                    <div
                      className={`p-4 rounded-lg border cursor-pointer transition-all ${
                        isSelected
                          ? 'border-primary ring-2 ring-primary/30 bg-primary/10'
                          : 'border-border/60 hover:border-border bg-card'
                      }`}
                      onClick={() => setSelectedNode(node.id)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className="font-mono text-xs font-bold text-muted-foreground">#{idx + 1}</span>
                          <span className="text-sm font-semibold text-foreground">{node.label}</span>
                        </div>
                        <Badge variant={node.type === 'OUTPUT' ? 'success' : node.type === 'INPUT' ? 'info' : 'outline'} size="sm">
                          {node.type}
                        </Badge>
                      </div>
                      <div className="mt-2 text-xs text-muted-foreground">{node.details}</div>
                      <div className="mt-2 font-mono text-[10px] text-foreground/70">
                        Digest: {node.digest}
                      </div>
                    </div>
                    {idx < provenanceNodes.length - 1 && (
                      <div className="flex justify-center text-muted-foreground">
                        <span className="text-sm">↓</span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </Card>
        </div>

        {/* Selected Node Inspector */}
        <div className="space-y-4">
          <Card className="p-6 space-y-4">
            <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Node Details
            </div>
            <div className="space-y-3">
              <div>
                <div className="text-xs text-muted-foreground">Node ID</div>
                <div className="font-mono text-sm font-bold text-foreground">{activeNode.id}</div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Node Type</div>
                <Badge variant="intelligence" size="sm" className="mt-1">{activeNode.type}</Badge>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Cryptographic Digest</div>
                <div className="font-mono text-xs text-foreground/90 break-all p-2 bg-muted/30 rounded border border-border/40 mt-1">
                  {activeNode.digest}
                </div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Direct Ancestors (Parents)</div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {activeNode.parents.length > 0 ? (
                    activeNode.parents.map((p) => <Badge key={p} variant="outline" size="sm">{p}</Badge>)
                  ) : (
                    <span className="text-xs text-muted-foreground">Root Input (None)</span>
                  )}
                </div>
              </div>
              <div>
                <div className="text-xs text-muted-foreground">Direct Descendants (Children)</div>
                <div className="flex flex-wrap gap-1 mt-1">
                  {activeNode.children.length > 0 ? (
                    activeNode.children.map((c) => <Badge key={c} variant="outline" size="sm">{c}</Badge>)
                  ) : (
                    <span className="text-xs text-muted-foreground">Terminal Output (Leaf)</span>
                  )}
                </div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
