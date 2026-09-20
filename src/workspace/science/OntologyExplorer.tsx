import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Network,
  Plus,
  Binary,
  Layers,
  Search,
  CheckCircle2,
} from 'lucide-react';

interface ConceptNode {
  id: string;
  name: string;
  domain: string;
  definition: string;
  confidence: number;
}

interface RelationEdge {
  id: string;
  from: string;
  to: string;
  type: string;
  weight: number;
}

export const OntologyExplorer: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [expandNotice, setExpandNotice] = useState<string | null>(null);

  const concepts: ConceptNode[] = [
    {
      id: 'concept_agent_latency',
      name: 'Agent Latency',
      domain: 'performance',
      definition: 'Turnaround response time of agent reasoning cycles.',
      confidence: 1.0,
    },
    {
      id: 'concept_memory_footprint',
      name: 'Memory Footprint',
      domain: 'resource',
      definition: 'RAM and context memory consumed by agent swarms.',
      confidence: 1.0,
    },
    {
      id: 'concept_swarm_throughput',
      name: 'Swarm Throughput',
      domain: 'throughput',
      definition: 'Completed autonomous operations per unit time.',
      confidence: 1.0,
    },
    {
      id: 'concept_context_entropy',
      name: 'Context Entropy',
      domain: 'cognition',
      definition: 'Information disorder and token drift in cognitive memory.',
      confidence: 0.95,
    },
    {
      id: 'concept_speculative_cache',
      name: 'Speculative Tensor Cache',
      domain: 'caching',
      definition: 'GPU tensor cache pre-warming for recurring document schemas.',
      confidence: 0.98,
    },
  ];

  const relations: RelationEdge[] = [
    { id: 'rel_1', from: 'concept_speculative_cache', to: 'concept_agent_latency', type: 'optimizes', weight: 0.95 },
    { id: 'rel_2', from: 'concept_memory_footprint', to: 'concept_agent_latency', type: 'correlates_with', weight: 0.75 },
    { id: 'rel_3', from: 'concept_context_entropy', to: 'concept_speculative_cache', type: 'regulates', weight: 0.88 },
    { id: 'rel_4', from: 'concept_agent_latency', to: 'concept_swarm_throughput', type: 'causes', weight: 0.92 },
  ];

  const handleExpandOntology = () => {
    setExpandNotice('Ontology Engine expanded semantic graph: Discovered 1 new conceptual link [Speculative Cache -> Swarm Throughput] via transitive graph closure.');
    setTimeout(() => setExpandNotice(null), 4000);
  };

  const filteredConcepts = concepts.filter(c =>
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.domain.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.definition.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <Network className="w-6 h-6 text-indigo-500" />
            Dynamic Semantic Ontology Explorer
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Dynamically expands the platform's ontological taxonomy, conceptual relations, and causal pathways across discovered scientific laws.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm" onClick={handleExpandOntology}>
            <Plus className="w-3.5 h-3.5 mr-1.5" />
            Discover Semantic Relations
          </Button>
        </div>
      </div>

      {expandNotice && (
        <div className="p-4 bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-200 dark:border-indigo-800 rounded-lg text-sm text-indigo-800 dark:text-indigo-300 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>{expandNotice}</span>
        </div>
      )}

      {/* Search */}
      <div className="relative">
        <Search className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
        <input
          type="text"
          placeholder="Search ontology concepts or domains..."
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          className="w-full pl-9 pr-4 py-2 text-xs border rounded-lg dark:bg-gray-800 dark:border-gray-700 text-gray-900 dark:text-white"
        />
      </div>

      {/* Concept & Relation Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Concepts Column */}
        <div className="lg:col-span-2 space-y-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
            <Binary className="w-4 h-4 text-indigo-500" />
            Ontological Concepts ({filteredConcepts.length})
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {filteredConcepts.map(c => (
              <Card key={c.id} className="p-4 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-sm text-gray-900 dark:text-white">{c.name}</span>
                  <Badge variant="outline" size="sm">{c.domain}</Badge>
                </div>
                <p className="text-xs text-gray-600 dark:text-gray-300">{c.definition}</p>
                <div className="flex items-center justify-between text-[11px] text-gray-400 pt-1 border-t border-gray-100 dark:border-gray-800">
                  <span className="font-mono text-[10px]">{c.id}</span>
                  <span className="text-emerald-600">{(c.confidence * 100).toFixed(0)}% Conf</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Semantic Relations Column */}
        <div className="space-y-3">
          <h3 className="text-xs font-semibold text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-purple-500" />
            Semantic Relations ({relations.length})
          </h3>
          <div className="space-y-2">
            {relations.map(rel => (
              <Card key={rel.id} className="p-3 text-xs space-y-1">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-purple-600 dark:text-purple-400 uppercase text-[10px] tracking-wider">
                    {rel.type}
                  </span>
                  <Badge variant="outline" size="sm">Weight: {rel.weight}</Badge>
                </div>
                <div className="text-gray-800 dark:text-gray-200 font-mono text-[11px] flex items-center gap-1">
                  <span>{rel.from.replace('concept_', '')}</span>
                  <span className="text-purple-400">→</span>
                  <span>{rel.to.replace('concept_', '')}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
