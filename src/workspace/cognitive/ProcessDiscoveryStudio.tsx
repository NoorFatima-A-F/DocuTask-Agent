import React, { useState, useEffect } from 'react';
import { TrendingUp, RefreshCw, ArrowRight } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { DiscoveredProcess } from '../../types/cognitive';

export const ProcessDiscoveryStudio: React.FC = () => {
  const [processes, setProcesses] = useState<DiscoveredProcess[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.listDiscoveredProcesses();
    setProcesses(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <TrendingUp className="w-7 h-7 text-emerald-400" />
            Autonomous Process Discovery & Mining Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Reconstructs end-to-end workflows from execution traces, measuring cycle times and isolating bottlenecks.
          </p>
        </div>
        <Button variant="outline" onClick={loadData}>
          <span className="flex items-center gap-2">
            <RefreshCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="space-y-4">
        {processes.map((proc) => (
          <Card key={proc.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-lg font-semibold text-slate-200">{proc.process_name}</h3>
                <p className="text-xs text-slate-400">Observed Executions: {proc.observed_executions_count} | Avg Cycle Time: {proc.avg_cycle_time_seconds}s</p>
              </div>
              <Badge variant="success">Opportunity Score: {(proc.automation_opportunity_score * 100).toFixed(0)}%</Badge>
            </div>

            <div>
              <h4 className="text-xs font-semibold text-slate-400 uppercase mb-2">Reconstructed Execution Path</h4>
              <div className="flex flex-wrap gap-2 items-center">
                {proc.reconstructed_steps.map((step, i) => (
                  <React.Fragment key={i}>
                    <span className="px-2.5 py-1.5 rounded bg-slate-800 text-xs font-medium text-slate-200 border border-slate-700">
                      {step}
                    </span>
                    {i < proc.reconstructed_steps.length - 1 && (
                      <ArrowRight className="w-3.5 h-3.5 text-slate-500" />
                    )}
                  </React.Fragment>
                ))}
              </div>
            </div>

            <div className="p-3 rounded-lg bg-amber-950/20 border border-amber-500/30 space-y-1">
              <span className="text-xs font-semibold text-amber-300">Detected Process Bottlenecks:</span>
              {proc.bottlenecks.map((b, idx) => (
                <p key={idx} className="text-xs text-slate-300">{b}</p>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
