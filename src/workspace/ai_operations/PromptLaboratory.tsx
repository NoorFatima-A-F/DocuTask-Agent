import React, { useState, useEffect } from 'react';
import {
  FlaskConical,
  Sparkles,
  RefreshCw,
  FileCode,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { AIOperationsApiClient } from '../../services/aiOperationsApiClient';
import { PromptVersion } from '../../types/aiOperations';

export const PromptLaboratory: React.FC = () => {
  const [prompts, setPrompts] = useState<PromptVersion[]>([]);
  const [selectedPrompt, setSelectedPrompt] = useState<PromptVersion | null>(null);
  const [loading, setLoading] = useState(true);

  const loadPrompts = async () => {
    try {
      setLoading(true);
      const data = await AIOperationsApiClient.getPrompts();
      setPrompts(data);
      if (data.length > 0 && !selectedPrompt) {
        setSelectedPrompt(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load prompts:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPrompts();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between bg-slate-900/60 p-5 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-500/10 rounded-xl border border-purple-500/20">
            <FlaskConical className="w-6 h-6 text-purple-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white">Prompt Laboratory & Evolution</h1>
            <p className="text-xs text-slate-400">Version control, automated mutations, few-shot tuning, and evaluation benchmarks</p>
          </div>
        </div>
        <Button variant="outline" onClick={loadPrompts} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Prompts list (4 cols) */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-slate-400 uppercase tracking-wider px-1">Prompt Versions</h2>
          <div className="space-y-2 max-h-[600px] overflow-y-auto pr-1">
            {prompts.map((p) => (
              <Card
                key={p.prompt_id}
                className={`p-3.5 cursor-pointer transition-all border ${
                  selectedPrompt?.prompt_id === p.prompt_id
                    ? 'bg-purple-950/30 border-purple-500/50 shadow-md shadow-purple-950/20'
                    : 'bg-slate-900/40 border-slate-800/80 hover:bg-slate-800/40'
                }`}
                onClick={() => setSelectedPrompt(p)}
              >
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-white text-xs">{p.version}</span>
                  <Badge variant={p.active ? 'success' : 'outline'}>{p.active ? 'Active' : 'Candidate'}</Badge>
                </div>
                <p className="text-xs text-slate-400 mt-1 font-mono">{p.agent_id}</p>
                <div className="flex items-center justify-between mt-2.5 text-[11px] text-slate-400 border-t border-slate-800/60 pt-2">
                  <span>Score: {(p.average_score * 100).toFixed(0)}%</span>
                  <span className="text-slate-500">{new Date(p.created_at).toLocaleDateString()}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Prompt Details (8 cols) */}
        <div className="lg:col-span-8 space-y-4">
          {selectedPrompt ? (
            <Card className="p-6 bg-slate-900/50 border-slate-800 space-y-5">
              <div className="flex items-start justify-between border-b border-slate-800 pb-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-lg font-bold text-white">{selectedPrompt.version}</h2>
                    <Badge variant={selectedPrompt.active ? 'success' : 'outline'}>
                      {selectedPrompt.active ? 'Production Active' : 'Offline Version'}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-400 font-mono mt-0.5">
                    Target: {selectedPrompt.agent_id} • ID: {selectedPrompt.prompt_id}
                  </p>
                </div>
                <div className="text-right">
                  <span className="text-2xl font-bold text-purple-400">
                    {(selectedPrompt.average_score * 100).toFixed(1)}%
                  </span>
                  <p className="text-[11px] text-slate-400">Benchmark Rating</p>
                </div>
              </div>

              {/* System Instruction */}
              <div>
                <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <FileCode className="w-3.5 h-3.5 text-purple-400" /> System Instruction
                </h4>
                <div className="p-4 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs text-slate-300 whitespace-pre-wrap leading-relaxed">
                  {selectedPrompt.system_instruction}
                </div>
              </div>

              {/* Mutation Notes */}
              {selectedPrompt.mutation_notes && (
                <div className="p-4 bg-purple-950/20 border border-purple-500/20 rounded-xl">
                  <h4 className="text-xs font-semibold text-purple-300 mb-1 flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5 text-purple-400" /> Optimization & Mutation Rationale
                  </h4>
                  <p className="text-xs text-slate-300">{selectedPrompt.mutation_notes}</p>
                </div>
              )}
            </Card>
          ) : (
            <Card className="p-8 text-center text-slate-400 bg-slate-900/40 border-slate-800">
              <FlaskConical className="w-8 h-8 text-slate-600 mx-auto mb-2" />
              <p>Select a prompt version to inspect and refine system instructions.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
