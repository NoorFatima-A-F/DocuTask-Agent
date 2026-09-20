import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Compass,
  Plus,
  CheckCircle2,
  HelpCircle,
  Filter,
} from 'lucide-react';


interface HypothesisItem {
  id: string;
  title: string;
  statement: string;
  domain: string;
  rationale: string;
  prior: number;
  eig: number;
  status: 'PROPOSED' | 'EXPERIMENTING' | 'CONFIRMED' | 'FALSIFIED';
  variables: string[];
  ageDays: number;
}

export const HypothesisGenerationCenter: React.FC = () => {
  const [selectedDomain, setSelectedDomain] = useState<string>('all');
  const [notice, setNotice] = useState<string | null>(null);

  const hypotheses: HypothesisItem[] = [
    {
      id: 'hyp-spec-tensor-01',
      title: 'Speculative Layout Cache Invariant',
      statement: 'Retaining speculative tensor embeddings for corporate invoice headers with >=5 hits/hr reduces P95 extraction latency by >=25%.',
      domain: 'performance',
      rationale: 'Analysis of 50,000 corporate invoices indicates 85% header spatial layout redundancy.',
      prior: 0.82,
      eig: 0.915,
      status: 'EXPERIMENTING',
      variables: ['tensor_cache_ttl', 'header_entropy', 'vram_allocation_mb'],
      ageDays: 1,
    },
    {
      id: 'hyp-triadic-coalition-02',
      title: 'Triadic Specialization Scaling Invariant',
      statement: 'Grouping agents into 3-member specialist triadic teams (Parser, Segmenter, Validator) eliminates 90% of auction negotiation jitter.',
      domain: 'swarm_dynamics',
      rationale: 'Auction bidding protocols experience 42ms scheduling overhead under high concurrency.',
      prior: 0.78,
      eig: 0.860,
      status: 'PROPOSED',
      variables: ['cluster_size', 'auction_round_count', 'task_throughput'],
      ageDays: 3,
    },
    {
      id: 'hyp-lockfree-ring-03',
      title: 'Lock-Free Ring Buffer Telemetry Invariant',
      statement: 'Migrating memory telemetry from mutex locks to atomic circular buffers reduces state synchronization stalls to zero across 64 concurrent workers.',
      domain: 'resilience',
      rationale: 'Mutex contention caused 180ms stalls in historical stress runs.',
      prior: 0.95,
      eig: 0.940,
      status: 'CONFIRMED',
      variables: ['buffer_lock_type', 'worker_concurrency', 'commit_latency'],
      ageDays: 7,
    },
    {
      id: 'hyp-quant-memory-04',
      title: 'Int8 Vector Quantization Recall Invariant',
      statement: 'Quantizing scratchpad vector representations from FP32 to Int8 retains >=99% semantic accuracy while reducing memory bandwidth by 50%.',
      domain: 'memory',
      rationale: 'High-dimensional embeddings exhibit significant sparsity in intermediate layers.',
      prior: 0.88,
      eig: 0.890,
      status: 'CONFIRMED',
      variables: ['quantization_bits', 'semantic_recall_pct', 'memory_bandwidth'],
      ageDays: 5,
    },
  ];

  const filteredHypotheses = selectedDomain === 'all'
    ? hypotheses
    : hypotheses.filter(h => h.domain === selectedDomain);

  const handleFormulateHypothesis = () => {
    setNotice('Autonomous Knowledge Gap Scanner formulated 1 new hypothesis for Memory Caching with EIG = 0.892.');
    setTimeout(() => setNotice(null), 4000);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Compass className="w-6 h-6 text-indigo-500" />
            Hypothesis Generation & Knowledge Gap Studio
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Formulates testable scientific propositions driven by Expected Information Gain (EIG), Bayesian priors, and causal assumption mining.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleFormulateHypothesis}>
            <Plus className="w-3.5 h-3.5 mr-1.5" />
            Mine Knowledge Gaps & Formulate
          </Button>
        </div>
      </div>

      {notice && (
        <div className="p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{notice}</span>
        </div>
      )}

      {/* Filters & Summary Row */}
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-400" />
          <span className="text-xs text-gray-500">Domain Filter:</span>
          {['all', 'performance', 'swarm_dynamics', 'resilience', 'memory'].map(d => (
            <button
              key={d}
              onClick={() => setSelectedDomain(d)}
              className={`px-2.5 py-1 text-xs rounded-full border transition-colors ${
                selectedDomain === d
                  ? 'bg-indigo-600 text-white border-indigo-600'
                  : 'bg-white dark:bg-gray-800 text-gray-600 dark:text-gray-300 border-gray-200 dark:border-gray-700 hover:bg-gray-50'
              }`}
            >
              {d.replace('_', ' ').toUpperCase()}
            </button>
          ))}
        </div>
        <div className="flex items-center gap-3 text-xs text-gray-500">
          <span>Active Hypotheses: <strong className="text-gray-900 dark:text-white">{filteredHypotheses.length}</strong></span>
          <span>Mean Prior: <strong className="text-emerald-600">85.7%</strong></span>
          <span>Mean EIG: <strong className="text-indigo-600">0.901</strong></span>
        </div>
      </div>

      {/* Hypotheses Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredHypotheses.map(hypo => (
          <Card key={hypo.id} className="p-5 space-y-3">
            <div className="flex items-start justify-between gap-2">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-indigo-500">{hypo.id}</span>
                  <Badge
                    variant={
                      hypo.status === 'CONFIRMED' ? 'success' :
                      hypo.status === 'EXPERIMENTING' ? 'warning' : 'info'
                    }
                    size="sm"
                  >
                    {hypo.status}
                  </Badge>
                </div>
                <h3 className="font-semibold text-gray-900 dark:text-white mt-1">{hypo.title}</h3>
              </div>
              <Badge variant="outline" size="sm">
                EIG: {hypo.eig.toFixed(3)}
              </Badge>
            </div>

            <p className="text-xs text-gray-600 dark:text-gray-300 bg-gray-50 dark:bg-gray-800/50 p-2.5 rounded border border-gray-100 dark:border-gray-700/60">
              "{hypo.statement}"
            </p>

            <div className="text-xs text-gray-500 dark:text-gray-400">
              <strong className="text-gray-700 dark:text-gray-300">Empirical Premise:</strong> {hypo.rationale}
            </div>

            <div className="flex flex-wrap items-center gap-1.5 pt-1">
              <span className="text-[10px] text-gray-400">Variables:</span>
              {hypo.variables.map(v => (
                <span key={v} className="text-[10px] font-mono px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded">
                  {v}
                </span>
              ))}
            </div>

            <div className="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800 text-xs">
              <div className="flex items-center gap-2">
                <span className="text-gray-400">Prior:</span>
                <span className="font-medium text-emerald-600 dark:text-emerald-400">{(hypo.prior * 100).toFixed(0)}%</span>
              </div>
              <span className="text-gray-400">Age: {hypo.ageDays}d</span>
            </div>
          </Card>
        ))}
      </div>

      {/* Knowledge Gap Detection Engine */}
      <Card className="p-5 space-y-4">
        <h3 className="font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <HelpCircle className="w-4 h-4 text-amber-500" />
          Detected Knowledge Gaps & Uncharacterized Regimes
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div className="p-3 bg-amber-50/50 dark:bg-amber-950/20 rounded border border-amber-200 dark:border-amber-800/40">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-amber-900 dark:text-amber-300">Layout Embedding Cache Pre-Warming</span>
              <Badge variant="warning" size="sm">Severity: High</Badge>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              Optimal pre-warming batch size across multi-vendor accounting documents remains uncharacterized.
            </p>
          </div>

          <div className="p-3 bg-sky-50/50 dark:bg-sky-950/20 rounded border border-sky-200 dark:border-sky-800/40">
            <div className="flex items-center justify-between">
              <span className="text-xs font-semibold text-sky-900 dark:text-sky-300">Inter-Agent Comm Burst Latency</span>
              <Badge variant="info" size="sm">Severity: Medium</Badge>
            </div>
            <p className="text-xs text-gray-600 dark:text-gray-400 mt-1">
              Inter-agent shared scratchpad communication latency under &gt;1000 doc/sec bursts.
            </p>
          </div>
        </div>
      </Card>
    </div>
  );
};
