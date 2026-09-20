import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import {
  BookOpen,
  Search,
} from 'lucide-react';

interface KnowledgeItem {
  id: string;
  category: 'PLAYBOOK' | 'LESSON_LEARNED' | 'ANTI_PATTERN' | 'FAILURE_POSTMORTEM' | 'SUCCESS_STRATEGY';
  title: string;
  description: string;
  tags: string[];
  confidence: number;
  usageCount: number;
  successRate: number;
}

export const OrganizationalMemoryExplorer: React.FC = () => {
  const [selectedCategory, setSelectedCategory] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const knowledgeEntries: KnowledgeItem[] = [
    {
      id: 'playbook-triadic-01',
      category: 'PLAYBOOK',
      title: 'Triadic Coalition Strategy for Complex Tables',
      description: 'Use a 3-agent team (Header Parser, Grid Segmenter, Data Validator) with shared scratchpad to bypass auction renegotiation.',
      tags: ['playbook', 'tables', 'coalition', 'throughput'],
      confidence: 0.992,
      usageCount: 380,
      successRate: 0.996,
    },
    {
      id: 'lesson-cache-warm-02',
      category: 'LESSON_LEARNED',
      title: 'Recurrent Corporate Invoice Header Redundancy',
      description: '85% of corporate invoices share identical token sequences in the upper 20% bounding region, yielding 28% latency reduction via caching.',
      tags: ['caching', 'invoices', 'latency', 'gpu'],
      confidence: 0.988,
      usageCount: 520,
      successRate: 0.991,
    },
    {
      id: 'antipattern-bidding-03',
      category: 'ANTI_PATTERN',
      title: 'Unbounded Inter-Agent Bidding in High-Concurrency Batches',
      description: 'Real-time multi-agent bidding during >500 doc/sec surges increases scheduling jitter by 42ms. Use pre-allocated task coalitions instead.',
      tags: ['bidding', 'swarm', 'latency', 'anti_pattern'],
      confidence: 0.975,
      usageCount: 95,
      successRate: 0.980,
    },
    {
      id: 'postmortem-lock-04',
      category: 'FAILURE_POSTMORTEM',
      title: 'State Lock Contention on Global Memory Stream',
      description: 'Simultaneous 32-worker telemetry commits locked memory table for 180ms. Resolved by migrating to lock-free ring buffers.',
      tags: ['resilience', 'locks', 'ring_buffer', 'postmortem'],
      confidence: 0.995,
      usageCount: 45,
      successRate: 1.0,
    },
    {
      id: 'strategy-zk-verify-05',
      category: 'SUCCESS_STRATEGY',
      title: 'Continuous SHA-256 Checkpoint Verification',
      description: 'Cryptographic hashing of state snapshots prior to destructive interventions enables zero-downtime micro-rollbacks.',
      tags: ['security', 'cryptography', 'governance', 'rollback'],
      confidence: 0.999,
      usageCount: 1240,
      successRate: 0.999,
    },
  ];

  const filteredEntries = knowledgeEntries.filter((k) => {
    const matchCategory = selectedCategory === 'ALL' || k.category === selectedCategory;
    const matchSearch =
      searchQuery === '' ||
      k.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      k.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      k.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()));
    return matchCategory && matchSearch;
  });

  const getCategoryBadgeVariant = (category: string): 'intelligence' | 'success' | 'warning' | 'error' | 'default' => {
    switch (category) {
      case 'PLAYBOOK':
        return 'intelligence';
      case 'SUCCESS_STRATEGY':
        return 'success';
      case 'LESSON_LEARNED':
        return 'default';
      case 'ANTI_PATTERN':
        return 'warning';
      case 'FAILURE_POSTMORTEM':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
            <BookOpen className="w-6 h-6 text-indigo-500" />
            Organizational Memory & Institutional Knowledge Center
          </h2>
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Phase 13.11 — Collective knowledge repository preserving playbooks, empirical lessons, anti-patterns, and postmortems.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="intelligence" size="md">
            {knowledgeEntries.length} Verified Playbooks & Insights
          </Badge>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-gray-400" />
          <input
            type="text"
            placeholder="Search playbooks, lessons, anti-patterns, tags..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        <div className="flex gap-1.5 flex-wrap">
          {['ALL', 'PLAYBOOK', 'LESSON_LEARNED', 'ANTI_PATTERN', 'FAILURE_POSTMORTEM', 'SUCCESS_STRATEGY'].map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-3 py-1.5 text-xs font-semibold rounded-md transition-colors ${
                selectedCategory === cat
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 hover:text-indigo-600'
              }`}
            >
              {cat.replace('_', ' ')}
            </button>
          ))}
        </div>
      </div>

      {/* Knowledge Cards */}
      <div className="grid grid-cols-1 gap-4">
        {filteredEntries.map((k) => (
          <Card key={k.id} className="p-5 hover:shadow-md transition-shadow">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 pb-3 border-b border-gray-100 dark:border-gray-800">
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-xs text-indigo-600 dark:text-indigo-400 font-semibold">{k.id}</span>
                  <Badge variant={getCategoryBadgeVariant(k.category)} size="sm">
                    {k.category.replace('_', ' ')}
                  </Badge>
                </div>
                <h4 className="font-semibold text-gray-900 dark:text-white text-base mt-1">{k.title}</h4>
              </div>
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <span className="text-xs text-gray-400 block">Usage Replays</span>
                  <span className="text-base font-bold text-gray-900 dark:text-white font-mono">
                    {k.usageCount} times
                  </span>
                </div>
              </div>
            </div>

            <p className="text-xs text-gray-600 dark:text-gray-300 mt-3">{k.description}</p>

            <div className="mt-4 flex flex-col md:flex-row md:items-center justify-between gap-2 pt-3 border-t border-gray-100 dark:border-gray-800 text-xs">
              <div className="flex items-center gap-1.5 flex-wrap">
                {k.tags.map((t, idx) => (
                  <span key={idx} className="px-2 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 rounded-full font-mono text-[10px]">
                    #{t}
                  </span>
                ))}
              </div>
              <div className="flex items-center gap-4 text-gray-400">
                <span>Confidence: <strong className="text-purple-600 dark:text-purple-400">{(k.confidence * 100).toFixed(1)}%</strong></span>
                <span>•</span>
                <span>Success Rate: <strong className="text-emerald-600 dark:text-emerald-400">{(k.successRate * 100).toFixed(1)}%</strong></span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
