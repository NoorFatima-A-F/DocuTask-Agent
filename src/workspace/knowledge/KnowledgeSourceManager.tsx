import React, { useState, useEffect } from 'react';
import { Database, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { knowledgeApiClient } from '../../services/knowledgeApiClient';
import { KnowledgeSource } from '../../types/knowledge';

export const KnowledgeSourceManager: React.FC = () => {
  const [sources, setSources] = useState<KnowledgeSource[]>([]);
  const [syncingId, setSyncingId] = useState<string | null>(null);

  const loadSources = async () => {
    const data = await knowledgeApiClient.listSources();
    setSources(data);
  };

  useEffect(() => {
    loadSources();
  }, []);

  const handleSync = async (srcId: string) => {
    setSyncingId(srcId);
    try {
      await fetch(`/api/v1/knowledge/sources/${srcId}/sync?tenant_id=default-tenant`, { method: 'POST' });
      await loadSources();
    } finally {
      setSyncingId(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-7 h-7 text-indigo-400" />
            Enterprise Data Source & Connector Manager
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Manage real-time sync connectors for Google Drive, Confluence, SharePoint, Slack, Jira, and Salesforce.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {sources.map((src) => (
          <Card key={src.id} className="p-5 bg-slate-900/60 border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start mb-2">
                <Badge variant="outline" className="text-indigo-400 border-indigo-500/30 font-mono">
                  {src.source_type}
                </Badge>
                <Badge variant={src.health_status === 'HEALTHY' ? 'success' : 'warning'}>
                  {src.health_status}
                </Badge>
              </div>
              <h3 className="text-lg font-semibold text-slate-200 mb-1">{src.name}</h3>
              <p className="text-xs text-slate-400 mb-4 font-mono">
                Sync Cron: {src.sync_schedule} | Synced Assets: {src.total_assets_synced}
              </p>
            </div>

            <div className="pt-3 border-t border-slate-800 flex justify-between items-center">
              <span className="text-xs text-slate-400">
                Status: {src.is_active ? 'Active Auto-Sync' : 'Paused'}
              </span>
              <Button
                variant="intelligence"
                size="sm"
                onClick={() => handleSync(src.id)}
                disabled={syncingId === src.id}
              >
                <span className="flex items-center gap-2">
                  <RefreshCw className={`w-3.5 h-3.5 ${syncingId === src.id ? 'animate-spin' : ''}`} />
                  {syncingId === src.id ? 'Syncing...' : 'Trigger Sync'}
                </span>
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
