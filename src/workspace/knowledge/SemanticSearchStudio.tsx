import React, { useState } from 'react';
import { Search, Sparkles, Sliders } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { RetrievedSnippet } from '../../types/knowledge';

export const SemanticSearchStudio: React.FC = () => {
  const [query, setQuery] = useState('procurement approval threshold for vendor contracts');
  const [results, setResults] = useState<RetrievedSnippet[]>([]);
  const [loading, setLoading] = useState(false);
  const [clearance, setClearance] = useState<'PUBLIC' | 'INTERNAL' | 'CONFIDENTIAL' | 'RESTRICTED'>('CONFIDENTIAL');

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await knowledgeApiClient.search(query, 5);
      setResults(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
          <Search className="w-7 h-7 text-indigo-400" />
          Semantic Search & Hybrid Retrieval Studio
        </h1>
        <p className="text-slate-400 text-sm mt-1">
          Perform multi-modal vector similarity, keyword BM25 matching, and security-governed enterprise retrieval.
        </p>
      </div>

      {/* Query Bar */}
      <Card className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
        <div className="flex gap-3">
          <div className="relative flex-1">
            <Search className="w-5 h-5 text-slate-400 absolute left-3 top-3" />
            <input
              value={query}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setQuery(e.target.value)}
              placeholder="Ask questions or enter search query across all organizational data..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500"
              onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => e.key === 'Enter' && handleSearch()}
            />
          </div>
          <Button variant="intelligence" onClick={handleSearch} disabled={loading}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {loading ? 'Searching...' : 'Hybrid Search'}
            </span>
          </Button>
        </div>

        <div className="flex flex-wrap items-center justify-between pt-2 border-t border-slate-800 text-xs text-slate-400">
          <div className="flex items-center gap-3">
            <Sliders className="w-4 h-4 text-slate-400" />
            <span>Security Clearance:</span>
            {(['PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'RESTRICTED'] as const).map((lvl) => (
              <Button
                key={lvl}
                variant={clearance === lvl ? 'primary' : 'outline'}
                size="sm"
                onClick={() => setClearance(lvl)}
              >
                {lvl}
              </Button>
            ))}
          </div>
          <span>Algorithm: Cosine Similarity (0.7) + BM25 Keyword Overlap (0.3)</span>
        </div>
      </Card>

      {/* Search Results */}
      <div className="space-y-3">
        <h2 className="text-lg font-semibold text-slate-200">
          Retrieved Grounded Snippets ({results.length})
        </h2>
        {results.map((res, idx) => (
          <Card key={idx} className="p-4 bg-slate-900/60 border-slate-800 hover:border-indigo-500/40 transition-colors">
            <div className="flex justify-between items-start mb-2">
              <div className="flex items-center gap-2">
                <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                  {res.matched_via}
                </Badge>
                <Badge variant="info">{res.source_type}</Badge>
                <Badge variant={res.security_classification === 'CONFIDENTIAL' ? 'warning' : 'outline'}>
                  {res.security_classification}
                </Badge>
              </div>
              <span className="text-xs font-mono text-emerald-400">
                Score: {(res.score * 100).toFixed(1)}%
              </span>
            </div>
            <h3 className="text-base font-semibold text-slate-200 mb-1">{res.title}</h3>
            <p className="text-sm text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50">
              {res.content}
            </p>
          </Card>
        ))}
      </div>
    </div>
  );
};
