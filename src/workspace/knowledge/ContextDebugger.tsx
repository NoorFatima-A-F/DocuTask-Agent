import React, { useState } from 'react';
import { Cpu, Sparkles, Code } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { ContextRetrievalResponse } from '../../types/knowledge';

export const ContextDebugger: React.FC = () => {
  const [goal, setGoal] = useState('Reconcile invoice #INV-99014 exceeding $50k purchase order threshold');
  const [contextData, setContextData] = useState<ContextRetrievalResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleRetrieveContext = async () => {
    setLoading(true);
    try {
      const res = await knowledgeApiClient.retrieveContext(goal);
      setContextData(res);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Cpu className="w-7 h-7 text-indigo-400" />
          Agent Context Engineering & Budget Debugger
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Inspect the complete retrieval &rarr; rerank &rarr; compression &rarr; prompt injection pipeline.
        </p>
      </div>

      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <div className="flex gap-3">
          <input
            value={goal}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setGoal(e.target.value)}
            placeholder="Agent goal or execution prompt..."
            className="flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500"
          />
          <Button variant="intelligence" onClick={handleRetrieveContext} disabled={loading}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {loading ? 'Assembling...' : 'Assemble Context'}
            </span>
          </Button>
        </div>
      </Card>

      {contextData && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
            <div className="flex justify-between items-center">
              <h2 className="text-base font-semibold text-slate-200">Assembled Context Metrics</h2>
              <Badge variant="success">Compression: {contextData.compression_ratio}x</Badge>
            </div>

            <div className="space-y-2 text-xs text-slate-300">
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700 flex justify-between">
                <span>Estimated Prompt Tokens:</span>
                <span className="font-mono text-cyan-400">{contextData.total_tokens_estimated} tokens</span>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700 flex justify-between">
                <span>Retrieval Latency:</span>
                <span className="font-mono text-emerald-400">{contextData.retrieval_latency_ms} ms</span>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-2">Graph Ontology Injected</h3>
              {contextData.graph_context.map((g, i) => (
                <p key={i} className="text-xs bg-slate-800/60 p-2 rounded text-cyan-300 font-mono mb-1">{g}</p>
              ))}
            </div>

            <div>
              <h3 className="text-sm font-semibold text-slate-300 mb-2">Procedural Memories Injected</h3>
              {contextData.memory_context.map((m, i) => (
                <p key={i} className="text-xs bg-slate-800/60 p-2 rounded text-indigo-300 font-mono mb-1">{m}</p>
              ))}
            </div>
          </Card>

          <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
            <h2 className="text-base font-semibold text-slate-200 flex items-center gap-2">
              <Code className="w-4 h-4 text-emerald-400" />
              Final Prompt Injected into Autonomous Agent
            </h2>
            <pre className="text-xs font-mono text-slate-300 bg-slate-950 p-4 rounded-lg border border-slate-800 overflow-x-auto whitespace-pre-wrap max-h-[460px]">
              {contextData.optimized_context_prompt}
            </pre>
          </Card>
        </div>
      )}
    </div>
  );
};
