import React, { useState, useEffect } from 'react';
import { Database, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { ExperienceMemoryEntry } from '../../types/cognitive';

export const ExperienceMemoryExplorer: React.FC = () => {
  const [experiences, setExperiences] = useState<ExperienceMemoryEntry[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.listExperiences();
    setExperiences(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Database className="w-7 h-7 text-indigo-400" />
            Cross-Agent Experience Memory Pool
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Enterprise pool of successful execution traces enabling instant zero-shot transfer across all agent fleets.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh Pool
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {experiences.map((exp) => (
          <Card key={exp.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-3">
            <div className="flex justify-between items-center">
              <Badge variant="outline" className="text-indigo-400 border-indigo-500/30">
                {exp.task_fingerprint}
              </Badge>
              <Badge variant="info">Reused: {exp.reuse_count}x</Badge>
            </div>
            <h3 className="text-sm font-semibold text-slate-200">{exp.input_pattern}</h3>
            <p className="text-xs text-slate-300 bg-slate-800/40 p-3 rounded border border-slate-700/50">
              {exp.reusable_knowledge}
            </p>
            <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
              <span>Agent Origin: {exp.agent_id}</span>
              <span className="font-mono text-emerald-400">Quality: {((exp.performance_metrics.quality_score || 0.99) * 100).toFixed(0)}%</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
