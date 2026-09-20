import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Search,
  Code2,
  Sparkles,
  CheckCircle2,
} from 'lucide-react';

interface CapabilityItem {
  id: string;
  name: string;
  category: 'WORKFLOW_TEMPLATE' | 'TOOL_COMPOSITION' | 'AGENT_ROLE' | 'PLANNER_PATTERN';
  description: string;
  synthesizedFrom: string[];
  reusabilityScore: number;
  inputContract: string;
  outputContract: string;
  usageCount: number;
}

export const CapabilityDiscoveryDashboard: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [categoryFilter, setCategoryFilter] = useState<string>('ALL');

  const capabilities: CapabilityItem[] = [
    {
      id: 'cap-801',
      name: 'Parallel Multi-Table Layout Extractor',
      category: 'WORKFLOW_TEMPLATE',
      description: 'Autonomous sub-DAG template that concurrently isolates, unmerges, and verifies multi-column tabular data in financial balance sheets.',
      synthesizedFrom: ['tesseract_engine', 'vision_transformer', 'sha256_verifier'],
      reusabilityScore: 0.985,
      inputContract: '{ document_pages: array, bounding_boxes: array }',
      outputContract: '{ structured_tables: array, confidence: float }',
      usageCount: 342,
    },
    {
      id: 'cap-802',
      name: 'Cryptographic Invariant Validator Agent Role',
      category: 'AGENT_ROLE',
      description: 'Specialized agent profile tailored for zero-fabrication mathematical auditing and schema consensus verification.',
      synthesizedFrom: ['VALIDATOR', 'REVIEWER', 'SECURITY'],
      reusabilityScore: 0.992,
      inputContract: '{ target_data: object, schema_hash: string }',
      outputContract: '{ audit_proof: string, passed: boolean }',
      usageCount: 890,
    },
    {
      id: 'cap-803',
      name: 'Triadic Verification Planner Pattern',
      category: 'PLANNER_PATTERN',
      description: 'Pattern orchestrating three independent specialized agents (Extractor, Verifier, Auditor) for high-stakes regulatory documents.',
      synthesizedFrom: ['APDLE_SCHEDULER', 'CONSENSUS_ENGINE'],
      reusabilityScore: 0.978,
      inputContract: '{ mission_goal: string, compliance_tier: string }',
      outputContract: '{ verified_dossier: object, merkle_hash: string }',
      usageCount: 154,
    },
  ];

  const filteredCapabilities = capabilities.filter((cap) => {
    const matchesSearch =
      cap.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      cap.description.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesCategory = categoryFilter === 'ALL' || cap.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Capability Discovery Dashboard</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              SYNTHESIS ACTIVE
            </Badge>
            <Badge variant="outline" size="sm">
              AMRS-RSIP Phase 13.9
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Dynamic discovery of execution gaps, autonomous synthesis of composite tools, workflow templates, and specialized agent roles.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="intelligence" size="sm">
            <Sparkles className="w-3.5 h-3.5 mr-1.5" />
            Synthesize Novel Capability
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
          {(['ALL', 'WORKFLOW_TEMPLATE', 'AGENT_ROLE', 'PLANNER_PATTERN'] as const).map((cat) => (
            <Button
              key={cat}
              variant={categoryFilter === cat ? 'primary' : 'ghost'}
              size="sm"
              onClick={() => setCategoryFilter(cat)}
            >
              {cat.replace('_', ' ')}
            </Button>
          ))}
        </div>
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search capabilities..."
            className="w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary"
          />
        </div>
      </div>

      {/* Capability Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filteredCapabilities.map((cap) => (
          <Card key={cap.id} className="p-5 border-border/40 space-y-4 hover:border-purple-500/30 transition-colors flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <Badge variant="intelligence" size="sm">
                  {cap.category.replace('_', ' ')}
                </Badge>
                <span className="text-xs font-mono text-muted-foreground">{cap.usageCount} Executions</span>
              </div>

              <div>
                <h2 className="text-sm font-semibold text-foreground">{cap.name}</h2>
                <p className="text-xs text-muted-foreground mt-1 leading-relaxed">{cap.description}</p>
              </div>

              {/* Synthesized from badges */}
              <div className="space-y-1.5 pt-1">
                <span className="text-[11px] text-muted-foreground">Synthesized From Components:</span>
                <div className="flex flex-wrap gap-1.5">
                  {cap.synthesizedFrom.map((src, idx) => (
                    <span
                      key={idx}
                      className="text-[10px] font-mono px-2 py-0.5 rounded bg-secondary/60 text-secondary-foreground border border-border/40"
                    >
                      {src}
                    </span>
                  ))}
                </div>
              </div>

              {/* Contracts Preview */}
              <div className="p-2.5 rounded bg-secondary/20 border border-border/30 space-y-1 text-[11px] font-mono text-muted-foreground">
                <div className="flex items-center gap-1">
                  <Code2 className="w-3 h-3 text-purple-400" />
                  <span>Input: {cap.inputContract}</span>
                </div>
                <div className="flex items-center gap-1">
                  <Code2 className="w-3 h-3 text-emerald-400" />
                  <span>Output: {cap.outputContract}</span>
                </div>
              </div>
            </div>

            <div className="flex items-center justify-between text-xs pt-3 border-t border-border/30">
              <div className="flex items-center gap-1 text-emerald-400 font-mono">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Reusability: {(cap.reusabilityScore * 100).toFixed(1)}%</span>
              </div>
              <Button variant="outline" size="sm">
                Deploy Template
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
