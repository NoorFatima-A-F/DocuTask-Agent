import React, { useState, useEffect } from 'react';
import { Filter, Search, FileText, Shield, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { KnowledgeAsset } from '../../types/knowledge';

export const KnowledgeExplorer: React.FC = () => {
  const [assets, setAssets] = useState<KnowledgeAsset[]>([]);
  const [search, setSearch] = useState('');
  const [filterType, setFilterType] = useState<string>('ALL');
  const [loading, setLoading] = useState(false);

  const loadAssets = async () => {
    setLoading(true);
    try {
      const data = await knowledgeApiClient.listAssets();
      setAssets(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAssets();
  }, []);

  const filtered = assets.filter(a => {
    const matchSearch = a.name.toLowerCase().includes(search.toLowerCase()) ||
      a.raw_content.toLowerCase().includes(search.toLowerCase());
    const matchType = filterType === 'ALL' || a.source_type === filterType;
    return matchSearch && matchType;
  });

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <FileText className="w-7 h-7 text-indigo-400" />
            Enterprise Knowledge Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Browse, search, and inspect ingested organizational documents, datasets, policies, and metadata.
          </p>
        </div>
        <Button variant="outline" onClick={loadAssets}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Filters */}
      <Card className="p-4 bg-slate-900/60 border-slate-800 flex flex-wrap gap-4 items-center justify-between">
        <div className="flex items-center gap-3 flex-1 min-w-[280px]">
          <Search className="w-4 h-4 text-slate-400" />
          <input
            placeholder="Search documents, policies, or topics..."
            value={search}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearch(e.target.value)}
            className="flex-1 px-3 py-2 bg-slate-800/80 border border-slate-700 rounded-lg text-slate-200 text-sm focus:outline-none focus:border-indigo-500"
          />
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-slate-400" />
          <span className="text-xs text-slate-400">Source:</span>
          {['ALL', 'LOCAL_DOCUMENT', 'GOOGLE_DRIVE', 'CONFLUENCE'].map((type) => (
            <Button
              key={type}
              variant={filterType === type ? 'primary' : 'outline'}
              size="sm"
              onClick={() => setFilterType(type)}
            >
              {type.replace('_', ' ')}
            </Button>
          ))}
        </div>
      </Card>

      {/* Assets Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((asset) => (
          <Card key={asset.id} className="p-5 bg-slate-900/60 border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start mb-2">
                <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                  {asset.source_type}
                </Badge>
                <Badge variant={asset.security_classification === 'CONFIDENTIAL' ? 'warning' : 'info'}>
                  {asset.security_classification}
                </Badge>
              </div>
              <h3 className="text-base font-semibold text-slate-200 mb-1">{asset.name}</h3>
              <p className="text-xs text-slate-400 line-clamp-3 mb-3">
                {asset.processed_content || asset.raw_content}
              </p>
            </div>

            <div className="pt-3 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center">
              <span>Tokens: {asset.metadata.token_count || 320}</span>
              <div className="flex items-center gap-1 text-emerald-400">
                <Shield className="w-3.5 h-3.5" />
                <span>Reliability: {((asset.reliability_score || 0.95) * 100).toFixed(0)}%</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
