import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Database, Search, ShieldCheck, Tag, CheckCircle2 } from 'lucide-react';

export const KnowledgeRegistryView: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('ALL');

  const records = [
    {
      id: 'kn_8ae86cf4',
      title: 'Parallel Wavefront Sharding for Large Document Sets',
      category: 'EXECUTION_RULE',
      version: '1.0.0',
      status: 'VERIFIED',
      confidence: 96.5,
      hash: 'sha256:4a9c1e7f',
      missionId: 'mission-001',
      tags: ['ocr', 'sharding', 'performance', 'wavefront'],
      content: { shard_size: 4, parallelism: 6, speedup_pct: 34.2 },
    },
    {
      id: 'kn_7b9d3e12',
      title: 'Dynamic SMT Verification on Ambiguous Entity Extractions',
      category: 'VALIDATION_STRATEGY',
      version: '1.0.0',
      status: 'VERIFIED',
      confidence: 94.2,
      hash: 'sha256:2d8f9a0c',
      missionId: 'mission-001',
      tags: ['smt', 'verification', 'confidence', 'truth'],
      content: { confidence_floor: 0.88, smt_timeout_ms: 120 },
    },
    {
      id: 'kn_3c8a91f5',
      title: 'Exponential Jitter Backoff on OCR Throttling',
      category: 'RESILIENCE_STRATEGY',
      version: '1.0.0',
      status: 'VERIFIED',
      confidence: 97.8,
      hash: 'sha256:8e1a3b5c',
      missionId: 'mission-001',
      tags: ['resilience', 'retry', 'throttling'],
      content: { base_delay_ms: 250, max_retries: 3, jitter: true },
    },
    {
      id: 'kn_1e9f4a6b',
      title: 'Dynamic DAG Wavefront Partitioning Heuristic',
      category: 'PLANNER_POLICY',
      version: '2.1.0',
      status: 'VERIFIED',
      confidence: 98.2,
      hash: 'sha256:9c2b4e8a',
      missionId: 'mission-002',
      tags: ['planner', 'dag', 'heuristics'],
      content: { max_fanout: 8, replan_threshold: 0.85 },
    },
  ];

  const filteredRecords = records.filter((r) => {
    const matchesCat = selectedCategory === 'ALL' || r.category === selectedCategory;
    const matchesSearch = r.title.toLowerCase().includes(searchTerm.toLowerCase()) || r.tags.some((t) => t.toLowerCase().includes(searchTerm.toLowerCase()));
    return matchesCat && matchesSearch;
  });

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
            <Database className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
              Institutional Knowledge Registry
              <Badge variant="intelligence" size="sm">Version Controlled</Badge>
            </h1>
            <p className="text-xs text-[#94A3B8] font-mono">
              Authoritative catalog of immutable, cryptographically sealed rules, strategies, and empirical knowledge records
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="relative">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#64748B]" />
            <input
              type="text"
              placeholder="Search knowledge records..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="bg-[#0F172A] border border-[#334155] rounded-lg pl-9 pr-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-emerald-500"
            />
          </div>
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="bg-[#0F172A] border border-[#334155] rounded-lg px-3 py-1.5 text-xs font-mono text-white focus:outline-none focus:border-emerald-500"
          >
            <option value="ALL">All Categories</option>
            <option value="EXECUTION_RULE">Execution Rules</option>
            <option value="VALIDATION_STRATEGY">Validation Strategies</option>
            <option value="RESILIENCE_STRATEGY">Resilience Strategies</option>
            <option value="PLANNER_POLICY">Planner Policies</option>
          </select>
        </div>
      </div>

      {/* Knowledge Records Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono">
        {filteredRecords.map((rec) => (
          <Card key={rec.id} className="p-5 rounded-xl border border-[#1E293B] bg-[#0F172A] space-y-4 flex flex-col justify-between">
            <div className="space-y-3">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <Badge variant="intelligence" size="sm">{rec.category}</Badge>
                  <Badge variant="outline" size="sm">v{rec.version}</Badge>
                </div>
                <div className="flex items-center gap-1.5 text-emerald-400 text-xs font-bold">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  {rec.confidence}% Conf
                </div>
              </div>

              <div>
                <h3 className="text-sm font-bold text-white">{rec.title}</h3>
                <div className="flex items-center gap-3 text-[11px] text-[#64748B] mt-1">
                  <span>Source: {rec.missionId}</span>
                  <span>Hash: {rec.hash}</span>
                </div>
              </div>

              {/* JSON Parameters Box */}
              <div className="p-3 bg-[#0B1120] border border-[#1E293B] rounded-xl text-[11px] space-y-1 font-mono">
                <span className="text-[#64748B] block text-[10px]">RECORD PAYLOAD:</span>
                <pre className="text-cyan-300 overflow-x-auto">{JSON.stringify(rec.content, null, 2)}</pre>
              </div>

              {/* Tags */}
              <div className="flex flex-wrap gap-1.5 pt-1">
                {rec.tags.map((t, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-[#1E293B] text-[#94A3B8] rounded text-[10px] flex items-center gap-1">
                    <Tag className="w-2.5 h-2.5 text-[#64748B]" />
                    {t}
                  </span>
                ))}
              </div>
            </div>

            <div className="pt-3 border-t border-[#1E293B] flex items-center justify-between text-xs">
              <span className="text-emerald-400 font-bold flex items-center gap-1">
                <CheckCircle2 className="w-3.5 h-3.5" />
                {rec.status}
              </span>
              <span className="text-[11px] text-[#64748B]">ID: {rec.id}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
