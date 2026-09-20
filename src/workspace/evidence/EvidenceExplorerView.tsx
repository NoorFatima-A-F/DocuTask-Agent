import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const EvidenceExplorerView: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<string>('ev-node-001');

  const evidenceNodes = [
    {
      id: 'ev-node-001',
      type: 'PLANNER_DECISION',
      agent: 'docutask-chief-planner',
      timestamp: '2026-09-10T18:22:10.142Z',
      hash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
      parentHash: 'genesis_root_00000000000000000000000000000000000000000000000000000000',
      status: 'VERIFIED',
      inputs: { document_id: 'doc-inv-8891', pages: 4, sla_bound_ms: 1500, quality_target: 0.98 },
      outputs: { selected_model: 'gemini-2.5-flash', parallelism: 3, strategy: 'two_phase_ocr_extract' },
      metrics: { predicted_latency_ms: 380.0, predicted_cost_usd: 0.0018, confidence: 0.985 },
      proof: {
        algorithm: 'SHA-256+Ed25519-Sim',
        signature: 'sig_a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa',
        publicKey: 'pub_docutask_root_key_2026_a8f3',
        nonce: 819204,
      },
    },
    {
      id: 'ev-node-002',
      type: 'TOOL_EXECUTION',
      agent: 'docutask-ocr-worker-01',
      timestamp: '2026-09-10T18:22:10.522Z',
      hash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
      parentHash: 'a8f3b20c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45',
      status: 'VERIFIED',
      inputs: { region: 'header_block_bbox', binarization: 'otsu_adaptive', engine: 'tesseract_v5_enhanced' },
      outputs: { tokens_extracted: 142, skew_angle_deg: 0.4, raw_text: 'INVOICE #INV-2026-9921 TOTAL: $4,850.00' },
      metrics: { ocr_latency_ms: 124.5, token_cost_usd: 0.00042, energy_joules: 0.22 },
      proof: {
        algorithm: 'SHA-256+Ed25519-Sim',
        signature: 'sig_d4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a',
        publicKey: 'pub_docutask_root_key_2026_d4e9',
        nonce: 492011,
      },
    },
    {
      id: 'ev-node-003',
      type: 'VALIDATION_CHECK',
      agent: 'docutask-qa-department',
      timestamp: '2026-09-10T18:22:10.680Z',
      hash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
      parentHash: 'd4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c748',
      status: 'VERIFIED',
      inputs: { line_items_sum: 4850.0, extracted_total: 4850.0, tolerance_usd: 0.01 },
      outputs: { invariant_reconciled: true, p_value: 0.0001, status: 'RECONCILED' },
      metrics: { check_latency_ms: 18.2, accuracy_score: 1.0 },
      proof: {
        algorithm: 'SHA-256+Ed25519-Sim',
        signature: 'sig_7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102f',
        publicKey: 'pub_docutask_root_key_2026_7c3f',
        nonce: 192837,
      },
    },
    {
      id: 'ev-node-004',
      type: 'REFLECTION_MUTATION',
      agent: 'docutask-governance-council',
      timestamp: '2026-09-10T18:22:11.050Z',
      hash: '3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120bc45a8f',
      parentHash: '7c3f810dae99120bc45a8f3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c',
      status: 'VERIFIED',
      inputs: { policy: 'ocr_deskew_threshold', observed_drift: '0.4 deg angle on rotated invoice headers' },
      outputs: { action: 'ADAPT_PREFILTER_POLICY', new_threshold_deg: 0.25, governance_vote: 'UNANIMOUS_APPROVED' },
      metrics: { expected_accuracy_lift: 0.038, policy_entropy_delta: -0.12 },
      proof: {
        algorithm: 'SHA-256+Ed25519-Sim',
        signature: 'sig_3b20c91e847ad3ef0192a83c748d4e9102fae89bb3c7c3f810dae99120b',
        publicKey: 'pub_docutask_root_key_2026_3b20',
        nonce: 663910,
      },
    },
  ];

  const activeNode = evidenceNodes.find((n) => n.id === selectedNode) || evidenceNodes[0]!;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Execution Evidence Explorer</h1>
            <Badge variant="success" size="sm">Merkle Root Attested</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Immutable cryptographic hash chains and Merkle DAG linking every planner decision, tool call, validation step, and policy mutation.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" size="md">
            SHA-256 + Ed25519
          </Badge>
          <Badge variant="intelligence" size="md">
            DAG Depth: 4 Layers
          </Badge>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Node List */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Evidence Chain ({evidenceNodes.length} Nodes)
          </div>
          {evidenceNodes.map((node) => {
            const isSelected = node.id === selectedNode;
            return (
              <Card
                key={node.id}
                className={`p-4 cursor-pointer transition-all ${
                  isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'
                }`}
                onClick={() => setSelectedNode(node.id)}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-xs font-bold text-foreground">{node.id}</span>
                      <Badge variant={node.status === 'VERIFIED' ? 'success' : 'warning'} size="sm">
                        {node.status}
                      </Badge>
                    </div>
                    <div className="text-xs font-medium text-muted-foreground mt-1">{node.type}</div>
                  </div>
                  <span className="text-[10px] font-mono text-muted-foreground">
                    {node.timestamp.split('T')[1]?.replace('Z', '')}
                  </span>
                </div>
                <div className="mt-3 font-mono text-[11px] text-muted-foreground truncate">
                  <span className="text-foreground/70">Hash: </span>
                  {node.hash.slice(0, 16)}...{node.hash.slice(-8)}
                </div>
              </Card>
            );
          })}
        </div>

        {/* Right: Selected Node Detail */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-lg font-bold">{activeNode.id}</h2>
                  <Badge variant="intelligence" size="sm">{activeNode.type}</Badge>
                </div>
                <div className="text-xs text-muted-foreground mt-1">Source Agent: <span className="font-mono text-foreground">{activeNode.agent}</span></div>
              </div>
              <div className="text-right">
                <div className="text-xs text-muted-foreground">Timestamp (UTC)</div>
                <div className="font-mono text-xs text-foreground">{activeNode.timestamp}</div>
              </div>
            </div>

            {/* Cryptographic Proof Details */}
            <div className="bg-muted/30 rounded-lg p-4 border border-border/40 space-y-2">
              <div className="text-xs font-semibold text-foreground flex items-center justify-between">
                <span>Cryptographic Proof & Signature</span>
                <span className="text-emerald-400 font-mono text-[11px]">✓ Nonce & Signature Verified</span>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono">
                <div>
                  <span className="text-muted-foreground">Digest: </span>
                  <span className="text-foreground/90 break-all">{activeNode.hash}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Parent Hash: </span>
                  <span className="text-foreground/90 break-all">{activeNode.parentHash.slice(0, 24)}...</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Signature: </span>
                  <span className="text-foreground/90 break-all">{activeNode.proof.signature}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Public Key: </span>
                  <span className="text-foreground/90">{activeNode.proof.publicKey}</span>
                </div>
              </div>
            </div>

            {/* Inputs & Outputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Verified Inputs
                </div>
                <pre className="p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto">
                  {JSON.stringify(activeNode.inputs, null, 2)}
                </pre>
              </div>
              <div className="space-y-2">
                <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                  Verified Outputs
                </div>
                <pre className="p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto">
                  {JSON.stringify(activeNode.outputs, null, 2)}
                </pre>
              </div>
            </div>

            {/* Telemetry Metrics */}
            <div className="space-y-2">
              <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                Runtime Telemetry Metrics
              </div>
              <div className="grid grid-cols-3 gap-3">
                {Object.entries(activeNode.metrics).map(([key, val]) => (
                  <div key={key} className="p-3 bg-card border border-border/40 rounded">
                    <div className="text-[11px] text-muted-foreground capitalize">{key.replace(/_/g, ' ')}</div>
                    <div className="text-sm font-bold font-mono text-foreground mt-1">
                      {typeof val === 'number' ? (val < 1 && val > 0 ? val.toFixed(4) : val.toLocaleString()) : String(val)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
