import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  BookOpen,
  Share2,
  CheckCircle2,
  Layers,
  Sparkles,
  Search,
} from 'lucide-react';

interface ScientificLawItem {
  id: string;
  name: string;
  statement: string;
  equation: string;
  supportingFactsCount: number;
  falsificationBoundary: string;
  version: string;
}

interface ScientificFactItem {
  id: string;
  statement: string;
  confidence: string;
  sourceExperiment: string;
}

export const KnowledgeGraphExplorer: React.FC = () => {
  const [selectedLawId, setSelectedLawId] = useState<string>('law-01');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const laws: ScientificLawItem[] = [
    {
      id: 'law-01',
      name: 'Law of Speculative Invariance in Structured Documents',
      statement: 'Spatial layout redundancy in recurring document schemas bounded by entropy H <= 1.2 permits O(1) speculative cache retrieval with sub-50ms latency overhead.',
      equation: 'Latency_P95(H, C) = T_base * (1 - C_rate * (1 - H/H_max))',
      supportingFactsCount: 4,
      falsificationBoundary: 'Invalidated if document token entropy exceeds H > 2.8 bits/token.',
      version: '1.0.0',
    },
    {
      id: 'law-02',
      name: 'Principle of Swarm Convergence Latency',
      statement: 'Coordination latency across distributed agent teams scales with the 0.42 power of agent count when using triadic specialist clusters.',
      equation: 'T_convergence = alpha * (N_agents^0.42) / bandwidth',
      supportingFactsCount: 3,
      falsificationBoundary: 'Invalidated if inter-agent network packet loss exceeds 5%.',
      version: '1.1.0',
    },
    {
      id: 'law-03',
      name: 'Universal Ring Buffer Contention Limit',
      statement: 'Lock-free atomic ring buffers provide strictly zero lock stalls for worker thread counts up to hardware concurrency limit.',
      equation: 'Stall_Time(W) = 0, for all W <= Hardware_Cores',
      supportingFactsCount: 2,
      falsificationBoundary: 'Invalidated on non-cache-coherent NUMA nodes.',
      version: '1.0.0',
    },
  ];

  const facts: ScientificFactItem[] = [
    {
      id: 'fact-01',
      statement: 'Speculative layout tensor caching yields 30.27% extraction latency reduction on corporate invoices.',
      confidence: 'ESTABLISHED_LAW',
      sourceExperiment: 'exp-cache-ab-01',
    },
    {
      id: 'fact-02',
      statement: 'Header spatial layout entropy across 50,000 corporate invoices is bounded at H <= 1.14 bits/token.',
      confidence: 'ESTABLISHED_LAW',
      sourceExperiment: 'exp-cache-ab-01',
    },
    {
      id: 'fact-03',
      statement: 'Triadic agent specialization reduces auction round count from 4.2 to 1.1 during bursts.',
      confidence: 'SOLID_THEORY',
      sourceExperiment: 'exp-triadic-auction-03',
    },
  ];

  const selectedLaw: ScientificLawItem = laws.find(l => l.id === selectedLawId) ?? laws[0]!;

  const filteredLaws = laws.filter(l =>
    l.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    l.statement.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-emerald-500" />
            Scientific Knowledge Base & Empirical Laws
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Permanent, versioned knowledge repository containing ratified empirical laws, governing equations, verified facts, and falsification boundaries.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            <Sparkles className="w-3.5 h-3.5 mr-1" />
            3 Governing Laws Ratified
          </Badge>
        </div>
      </div>

      {/* Search Filter */}
      <div className="relative">
        <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
        <input
          type="text"
          placeholder="Search laws, equations, or scientific statements..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full pl-9 pr-4 py-2 text-xs border rounded-lg dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white"
        />
      </div>

      {/* Grid: Laws list & Law Detail Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Laws list */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider">Ratified Laws</h3>
          {filteredLaws.map(law => (
            <Card
              key={law.id}
              className={`p-4 cursor-pointer transition-all border-l-4 ${
                selectedLawId === law.id
                  ? 'border-l-emerald-500 shadow-md bg-emerald-50/20 dark:bg-emerald-950/20'
                  : 'border-l-transparent hover:bg-gray-50 dark:hover:bg-gray-800/40'
              }`}
              onClick={() => setSelectedLawId(law.id)}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-xs text-emerald-600 font-semibold">{law.id}</span>
                <Badge variant="outline" size="sm">v{law.version}</Badge>
              </div>
              <h4 className="font-semibold text-sm text-gray-900 dark:text-white mt-1">{law.name}</h4>
              <p className="text-xs text-gray-500 dark:text-gray-400 line-clamp-2 mt-1">
                {law.statement}
              </p>
            </Card>
          ))}
        </div>

        {/* Middle & Right: Law Detail Inspector */}
        <div className="lg:col-span-2 space-y-4">
          <Card className="p-6 space-y-5">
            <div className="flex items-start justify-between">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-emerald-600 font-bold">{selectedLaw.id}</span>
                  <Badge variant="success" size="sm">Ratified Scientific Law</Badge>
                  <Badge variant="outline" size="sm">Version {selectedLaw.version}</Badge>
                </div>
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mt-1">{selectedLaw.name}</h3>
              </div>
              <Share2 className="w-5 h-5 text-gray-400 hover:text-emerald-500 cursor-pointer" />
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Formal Statement</span>
              <p className="text-sm text-gray-800 dark:text-gray-200 mt-1 bg-gray-50 dark:bg-gray-800/60 p-3 rounded border border-gray-100 dark:border-gray-700">
                "{selectedLaw.statement}"
              </p>
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Governing Equation</span>
              <div className="mt-1 font-mono text-sm text-emerald-700 dark:text-emerald-400 bg-emerald-50/60 dark:bg-emerald-950/40 p-3 rounded border border-emerald-200 dark:border-emerald-800">
                {selectedLaw.equation}
              </div>
            </div>

            <div>
              <span className="text-xs font-semibold text-gray-500 uppercase">Falsification Boundary</span>
              <div className="mt-1 text-xs text-amber-700 dark:text-amber-400 bg-amber-50/60 dark:bg-amber-950/40 p-2.5 rounded border border-amber-200 dark:border-amber-800">
                {selectedLaw.falsificationBoundary}
              </div>
            </div>

            <div className="pt-2 border-t border-gray-100 dark:border-gray-800">
              <span className="text-xs font-semibold text-gray-500 uppercase flex items-center gap-1 mb-2">
                <Layers className="w-3.5 h-3.5 text-emerald-500" />
                Supporting Empirical Facts ({facts.length})
              </span>
              <div className="space-y-2">
                {facts.map(fact => (
                  <div key={fact.id} className="p-2.5 bg-gray-50 dark:bg-gray-800/40 rounded text-xs flex items-start justify-between gap-2 border border-gray-100 dark:border-gray-700">
                    <div className="flex items-start gap-2">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500 flex-shrink-0 mt-0.5" />
                      <div>
                        <p className="text-gray-800 dark:text-gray-200">{fact.statement}</p>
                        <span className="text-[10px] text-gray-400">Source Exp: {fact.sourceExperiment}</span>
                      </div>
                    </div>
                    <Badge variant="success" size="sm">{fact.confidence}</Badge>
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
