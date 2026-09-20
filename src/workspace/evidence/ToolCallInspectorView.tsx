import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const ToolCallInspectorView: React.FC = () => {
  const [selectedCall, setSelectedCall] = useState<string>('tee-0001');

  const toolExecutions = [
    {
      id: 'tee-0001',
      callId: 'call-ocr-001',
      toolName: 'adaptive_document_ocr',
      timestamp: '2026-09-10T18:22:10.522Z',
      inputs: {
        doc_id: 'doc-invoice-8891',
        engine: 'tesseract_v5_enhanced',
        binarization: 'otsu_adaptive',
        deskew_enabled: true,
      },
      outputs: {
        status: 'SUCCESS',
        text_tokens: 142,
        bounding_boxes_count: 28,
        mean_confidence: 0.991,
      },
      trace: {
        latencyMs: 124.5,
        tokenCostUsd: 0.00042,
        energyJoules: 0.22,
        exitCode: 0,
        stdout: 'Processed 1 page in 124.5ms. Detected 28 word boxes with mean OCR confidence 99.1%.',
        stderr: '',
        sideEffects: ['document_ocr_cache_updated', 'memory_entity_seeded'],
        inputDigest: '8891a4e102f928bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7',
        outputDigest: '7721d4e9102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83',
      },
      previousHash: 'genesis_tool_block_00000000000000000000000000000000',
      entryHash: 'c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20',
    },
    {
      id: 'tee-0002',
      callId: 'call-table-002',
      toolName: 'tabular_grid_extractor',
      timestamp: '2026-09-10T18:22:10.610Z',
      inputs: {
        doc_id: 'doc-invoice-8891',
        table_bounding_box: [120, 340, 580, 720],
        column_alignment_mode: 'deterministic_hough_lines',
      },
      outputs: {
        status: 'SUCCESS',
        rows_extracted: 6,
        columns_extracted: 4,
        reconciled_sum: 4850.0,
      },
      trace: {
        latencyMs: 78.4,
        tokenCostUsd: 0.00028,
        energyJoules: 0.14,
        exitCode: 0,
        stdout: 'Table grid parsed: 6 rows, 4 columns. Line items sum = 4850.00.',
        stderr: '',
        sideEffects: ['table_schema_registered'],
        inputDigest: '102fae89bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c78891a4',
        outputDigest: 'f3b20c91e847ad3ef0192a83c77721d4e9102fae89bb3c17820aedfa9102bc45',
      },
      previousHash: 'c91e847ad3ef0192a83c7482910fae12089bb3c17820aedfa9102bc45a8f3b20',
      entryHash: 'e12089bb3c17820aedfa9102bc45a8f3b20c91e847ad3ef0192a83c7482910fa',
    },
  ];

  const activeCall = toolExecutions.find((t) => t.id === selectedCall) || toolExecutions[0]!;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Tool Execution Ledger</h1>
            <Badge variant="success" size="sm">Deterministic Traces</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Granular trace inspector for tool invocations, parameter hashes, execution durations, token costs, and Joules.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" size="md">
            Total Spend: $0.00070
          </Badge>
          <Badge variant="intelligence" size="md">
            Energy: 0.36 J
          </Badge>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Tool Calls List */}
        <div className="space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Tool Executions ({toolExecutions.length})
          </div>
          {toolExecutions.map((item) => {
            const isSelected = item.id === selectedCall;
            return (
              <Card
                key={item.id}
                className={`p-4 cursor-pointer transition-all ${
                  isSelected ? 'border-primary ring-1 ring-primary/40 bg-primary/5' : 'hover:border-border/80'
                }`}
                onClick={() => setSelectedCall(item.id)}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs font-bold text-foreground">{item.callId}</span>
                    <div className="text-xs font-medium text-foreground mt-0.5">{item.toolName}</div>
                  </div>
                  <Badge variant="success" size="sm">0 Exit</Badge>
                </div>
                <div className="mt-3 flex items-center justify-between text-[11px] font-mono text-muted-foreground">
                  <span>{item.trace.latencyMs} ms</span>
                  <span>${item.trace.tokenCostUsd.toFixed(5)}</span>
                  <span>{item.trace.energyJoules} J</span>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Selected Tool Trace */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6 space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-border/40 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-lg font-bold">{activeCall.toolName}</h2>
                  <Badge variant="intelligence" size="sm">{activeCall.callId}</Badge>
                </div>
                <div className="text-xs text-muted-foreground mt-0.5">
                  Executed at: <span className="font-mono text-foreground">{activeCall.timestamp}</span>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Badge variant="outline" size="md">{activeCall.trace.latencyMs} ms</Badge>
                <Badge variant="success" size="md">${activeCall.trace.tokenCostUsd.toFixed(5)}</Badge>
              </div>
            </div>

            {/* Inputs & Outputs */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Parameters ({activeCall.trace.inputDigest.slice(0, 8)}...)
                </div>
                <pre className="p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto">
                  {JSON.stringify(activeCall.inputs, null, 2)}
                </pre>
              </div>
              <div className="space-y-2">
                <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                  Output Results ({activeCall.trace.outputDigest.slice(0, 8)}...)
                </div>
                <pre className="p-3 bg-muted/40 rounded border border-border/40 font-mono text-xs overflow-x-auto">
                  {JSON.stringify(activeCall.outputs, null, 2)}
                </pre>
              </div>
            </div>

            {/* Stdout Logs */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Execution stdout
              </div>
              <div className="p-3 bg-black/80 rounded border border-border/40 font-mono text-xs text-emerald-400">
                {activeCall.trace.stdout}
              </div>
            </div>

            {/* Side effects and Hash */}
            <div className="space-y-2">
              <div className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
                Verified Side-Effects & Hash Block
              </div>
              <div className="flex flex-wrap gap-2">
                {activeCall.trace.sideEffects.map((eff) => (
                  <Badge key={eff} variant="outline" size="sm">{eff}</Badge>
                ))}
              </div>
              <div className="p-3 bg-card border border-border/40 rounded font-mono text-[11px] text-muted-foreground mt-2 space-y-1">
                <div><span className="text-foreground">Prev Hash: </span>{activeCall.previousHash}</div>
                <div><span className="text-foreground">Block Hash: </span><span className="text-emerald-400 font-bold">{activeCall.entryHash}</span></div>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
