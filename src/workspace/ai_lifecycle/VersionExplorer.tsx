import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { AILifecycleApiClient } from '../../services/aiLifecycleApiClient';
import type { AgentVersion } from '../../types/aiLifecycle';
import { GitCommit, RotateCcw, Check, Sparkles, RefreshCw } from 'lucide-react';

export const VersionExplorer: React.FC = () => {
  const [versions, setVersions] = useState<AgentVersion[]>([]);
  const [activeVersion, setActiveVersion] = useState<AgentVersion | null>(null);
  const [loading, setLoading] = useState(true);
  const [rollbackSuccess, setRollbackSuccess] = useState(false);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await AILifecycleApiClient.listVersions('agt_acme_invoice_reconciler');
      setVersions(list);
      if (list.length > 0 && list[0]) setActiveVersion(list[0]);
      setLoading(false);
    };
    load();
  }, []);

  const handleRollback = async (tag: string) => {
    await AILifecycleApiClient.rollbackVersion('agt_acme_invoice_reconciler', tag);
    setRollbackSuccess(true);
    setTimeout(() => setRollbackSuccess(false), 3000);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <GitCommit className="w-7 h-7 text-indigo-400" />
            Agent Version Control System (AVCS)
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Git-like immutable version history, prompt diffs, accuracy metrics, and instant rollback.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Version History...
        </div>
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Version Commit Tree */}
          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-1">
            <CardHeader>
              <CardTitle className="text-base text-white">Semantic Releases ({versions.length})</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              {versions.map((v) => (
                <div
                  key={v.version_id}
                  onClick={() => setActiveVersion(v)}
                  className={`p-3 rounded-lg border cursor-pointer transition ${
                    activeVersion?.version_id === v.version_id
                      ? 'bg-indigo-950/40 border-indigo-500'
                      : 'bg-slate-800/50 border-slate-700/60 hover:border-slate-600'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <span className="text-sm font-bold text-white font-mono">v{v.version_tag}</span>
                    <Badge variant="success">{(v.accuracy_score * 100).toFixed(0)}% Acc</Badge>
                  </div>
                  <p className="text-xs text-slate-400 mt-1 truncate">{v.changelog}</p>
                  <span className="text-[10px] text-slate-500 mt-2 block font-mono">{v.model_family}</span>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Version Inspector */}
          <Card className="bg-slate-900/80 border-slate-800 lg:col-span-2">
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-base text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-indigo-400" /> Version v{activeVersion?.version_tag} Configuration
                </CardTitle>
                <Button
                  variant="outline"
                  onClick={() => activeVersion && handleRollback(activeVersion.version_tag)}
                >
                  <span className="flex items-center gap-1.5 text-xs">
                    {rollbackSuccess ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <RotateCcw className="w-3.5 h-3.5" />}
                    Rollback to v{activeVersion?.version_tag}
                  </span>
                </Button>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <label className="text-xs text-slate-400 font-semibold block mb-1">System Prompt Directive</label>
                <div className="p-3 bg-slate-950 rounded border border-slate-800 text-xs font-mono text-slate-200">
                  {activeVersion?.system_prompt}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50 text-xs">
                  <span className="text-slate-400 block text-[10px]">Bound Tools</span>
                  <span className="text-slate-200 font-mono mt-1 block">
                    {activeVersion?.tools.join(', ') || 'None'}
                  </span>
                </div>
                <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50 text-xs">
                  <span className="text-slate-400 block text-[10px]">Execution Unit Cost</span>
                  <span className="text-emerald-400 font-bold mt-1 block font-mono">
                    ${activeVersion?.cost_per_execution_usd} USD
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
};
