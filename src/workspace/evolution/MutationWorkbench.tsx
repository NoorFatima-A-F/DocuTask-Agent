import React, { useState, useEffect } from 'react';
import {
  GitPullRequest,
  FileCode,
  ShieldCheck,
  PlusCircle,
  RefreshCw,
  Copy,
  Check,
  Lock,
} from 'lucide-react';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { EvolutionPlatformApiClient } from '../../services/evolutionPlatformApiClient';
import { ArchitectureMutationProposalPayload } from '../../types/evolutionPlatform';

export const MutationWorkbench: React.FC = () => {
  const [proposals, setProposals] = useState<ArchitectureMutationProposalPayload[]>([]);
  const [selectedProposal, setSelectedProposal] = useState<ArchitectureMutationProposalPayload | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [copied, setCopied] = useState<boolean>(false);
  const [showModal, setShowModal] = useState<boolean>(false);

  // Form
  const [title, setTitle] = useState<string>('');
  const [mutationType, setMutationType] = useState<string>('PLANNER_REDESIGN');
  const [targetComponent, setTargetComponent] = useState<string>('swarm_planner');
  const [diffSpec, setDiffSpec] = useState<string>('--- a/module.py\n+++ b/module.py\n-serial_call()\n+await parallel_task_group()');
  const [rationale, setRationale] = useState<string>('');

  useEffect(() => {
    loadProposals();
  }, []);

  const loadProposals = async () => {
    setLoading(true);
    try {
      const data = await EvolutionPlatformApiClient.listMutations();
      setProposals(data);
      if (data.length > 0 && data[0]) {
        setSelectedProposal(data[0]);
      }
    } catch (err) {
      console.error('Failed to load mutations:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePropose = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    try {
      const mut = await EvolutionPlatformApiClient.proposeMutation({
        title,
        mutation_type: mutationType,
        target_components: [targetComponent],
        code_diff_spec: diffSpec,
        rationale: rationale || 'Automated performance refactoring.',
      });
      setProposals((prev) => [mut, ...prev]);
      setSelectedProposal(mut);
      setShowModal(false);
      setTitle('');
      setRationale('');
    } catch (err) {
      console.error('Failed to propose mutation:', err);
    }
  };

  const copyHash = (hash: string) => {
    navigator.clipboard.writeText(hash);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 shadow-xl">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl">
            <GitPullRequest className="w-6 h-6 text-indigo-400" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl font-bold text-slate-100">Self-Modification & Mutation Workbench</h1>
              <Badge variant="intelligence" size="sm">AST Invariant Synthesis</Badge>
            </div>
            <p className="text-sm text-slate-400 mt-0.5">
              Inspect and synthesize non-destructive code mutations, AST rewrites, and cryptographic diff seals.
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            onClick={loadProposals}
            disabled={loading}
          >
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button
            variant="intelligence"
            onClick={() => setShowModal(true)}
          >
            <span className="flex items-center gap-2">
              <PlusCircle className="w-4 h-4" />
              Propose Mutation
            </span>
          </Button>
        </div>
      </div>

      {/* Grid: 2 Columns */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Proposals List */}
        <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm font-semibold text-slate-200">Active Mutation Proposals</span>
            <Badge variant="outline" size="sm">{proposals.length} Total</Badge>
          </div>

          <div className="space-y-3">
            {proposals.map((m) => (
              <div
                key={m.mutation_id}
                onClick={() => setSelectedProposal(m)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  selectedProposal?.mutation_id === m.mutation_id
                    ? 'bg-indigo-950/40 border-indigo-500/50 shadow-md'
                    : 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <span className="font-mono text-xs text-indigo-400 font-bold">{m.mutation_id}</span>
                  <Badge variant={m.status === 'APPROVED' ? 'success' : 'outline'} size="sm">
                    {m.status}
                  </Badge>
                </div>
                <h3 className="text-sm font-medium text-slate-200 leading-snug">{m.title}</h3>
                <div className="text-xs text-slate-400 mt-2 flex justify-between font-mono">
                  <span>{m.mutation_type}</span>
                  <span className="text-emerald-400 font-bold">{(m.confidence_score * 100).toFixed(0)}% Conf</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right 2 Cols: Code Diff & Safety Analysis */}
        {selectedProposal && (
          <div className="lg:col-span-2 space-y-4">
            <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-6 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-4 border-b border-slate-800">
                <div>
                  <div className="flex items-center gap-2">
                    <h2 className="text-lg font-bold text-slate-100">{selectedProposal.title}</h2>
                    <Badge variant="info" size="sm">{selectedProposal.mutation_type}</Badge>
                  </div>
                  <p className="text-xs text-slate-400 mt-1">{selectedProposal.rationale}</p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={() => copyHash(selectedProposal.sha256_hash)}
                    className="flex items-center gap-1.5 text-xs font-mono text-slate-400 hover:text-slate-200 bg-slate-950 border border-slate-800 px-3 py-1.5 rounded-lg"
                  >
                    <Lock className="w-3.5 h-3.5 text-purple-400" />
                    <span className="truncate max-w-[120px]">{selectedProposal.sha256_hash.substring(0, 16)}...</span>
                    {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                  </button>
                </div>
              </div>

              {/* Safety Assessment */}
              <div className="p-4 bg-purple-950/30 border border-purple-500/20 rounded-xl space-y-1.5">
                <div className="flex items-center gap-2 text-xs font-bold text-purple-300">
                  <ShieldCheck className="w-4 h-4 text-purple-400" />
                  <span>Automated AST Safety & Invariant Verification</span>
                </div>
                <p className="text-xs text-slate-300 font-mono">{selectedProposal.safety_analysis}</p>
              </div>

              {/* Code Diff Display */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-xs font-mono text-slate-400">
                  <FileCode className="w-4 h-4 text-slate-400" />
                  <span>Synthesized Unified Code Diff</span>
                </div>
                <pre className="bg-slate-950 border border-slate-800 rounded-xl p-4 text-xs font-mono text-slate-300 overflow-x-auto leading-relaxed">
                  {selectedProposal.code_diff_spec.split('\n').map((line, idx) => {
                    const isAdd = line.startsWith('+');
                    const isDel = line.startsWith('-');
                    const isHeader = line.startsWith('@@') || line.startsWith('---') || line.startsWith('+++');
                    return (
                      <div
                        key={idx}
                        className={
                          isAdd
                            ? 'text-emerald-400 bg-emerald-950/30 px-1 rounded'
                            : isDel
                            ? 'text-rose-400 bg-rose-950/30 px-1 rounded'
                            : isHeader
                            ? 'text-indigo-400 font-bold'
                            : 'text-slate-400'
                        }
                      >
                        {line}
                      </div>
                    );
                  })}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 max-w-lg w-full space-y-4 shadow-2xl">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-slate-100">Propose Architecture Mutation</h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-slate-400 hover:text-slate-200 text-sm font-semibold"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handlePropose} className="space-y-4">
              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Proposal Title</label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g. Async Concurrent Validator"
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                  required
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Mutation Type</label>
                  <select
                    value={mutationType}
                    onChange={(e) => setMutationType(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                  >
                    <option value="PLANNER_REDESIGN">PLANNER_REDESIGN</option>
                    <option value="ROUTING_REFACTOR">ROUTING_REFACTOR</option>
                    <option value="MODULE_REFACTORING">MODULE_REFACTORING</option>
                    <option value="CACHE_REDESIGN">CACHE_REDESIGN</option>
                  </select>
                </div>
                <div>
                  <label className="text-xs font-medium text-slate-300 block mb-1">Target Component</label>
                  <input
                    type="text"
                    value={targetComponent}
                    onChange={(e) => setTargetComponent(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500 font-mono"
                  />
                </div>
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Unified Diff Spec</label>
                <textarea
                  value={diffSpec}
                  onChange={(e) => setDiffSpec(e.target.value)}
                  rows={4}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg p-3 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div>
                <label className="text-xs font-medium text-slate-300 block mb-1">Rationale</label>
                <input
                  type="text"
                  value={rationale}
                  onChange={(e) => setRationale(e.target.value)}
                  placeholder="Why this refactor improves performance or safety..."
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="flex justify-end gap-3 pt-2">
                <Button variant="ghost" onClick={() => setShowModal(false)}>
                  Cancel
                </Button>
                <Button variant="intelligence" type="submit">
                  Submit Mutation
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
