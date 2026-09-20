import React, { useState, useEffect } from 'react';
import {
  Workflow,
  Pause,
  Play,
  RefreshCw,
  ShieldCheck,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { DurableWorkflow } from '../../types/distributedPlatform';

export const DurableWorkflowInspector: React.FC = () => {
  const [workflows, setWorkflows] = useState<DurableWorkflow[]>([]);
  const [selectedWorkflow, setSelectedWorkflow] = useState<DurableWorkflow | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getDurableWorkflows();
      setWorkflows(res);
      if (res.length > 0) {
        setSelectedWorkflow(res[0] || null);
      }
    } catch (err) {
      console.error('Failed to load durable workflows:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, []);

  const handlePause = async (id: string) => {
    try {
      setActionLoading(true);
      const updated = await DistributedApiClient.pauseWorkflow(id);
      setSelectedWorkflow(updated);
      await loadWorkflows();
    } catch (err) {
      console.error('Failed to pause workflow:', err);
    } finally {
      setActionLoading(false);
    }
  };

  const handleResume = async (id: string) => {
    try {
      setActionLoading(true);
      const updated = await DistributedApiClient.resumeWorkflow(id);
      setSelectedWorkflow(updated);
      await loadWorkflows();
    } catch (err) {
      console.error('Failed to resume workflow:', err);
    } finally {
      setActionLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Workflow className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Durable Workflow Inspector</h1>
            <p className="text-sm text-slate-400">
              Temporal-grade stateful saga orchestration with pause, resume, and checkpoint replay
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadWorkflows} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Workflows List */}
        <div className="lg:col-span-1 space-y-3">
          {workflows.map((wf) => {
            const isSelected = selectedWorkflow?.workflow_id === wf.workflow_id;
            return (
              <Card
                key={wf.workflow_id}
                onClick={() => setSelectedWorkflow(wf)}
                className={`p-4 cursor-pointer border transition-all ${
                  isSelected
                    ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <span className="font-bold text-white text-sm truncate">{wf.title}</span>
                  <Badge variant={wf.state === 'RUNNING' ? 'intelligence' : wf.state === 'PAUSED' ? 'warning' : 'success'}>
                    {wf.state}
                  </Badge>
                </div>
                <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
                  <span>{wf.workflow_id}</span>
                  <span className="text-indigo-400">Step {wf.current_step_index + 1} / {wf.total_steps}</span>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Workflow Detail & Step Visualizer */}
        <div className="lg:col-span-2">
          {selectedWorkflow ? (
            <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-6">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <h2 className="text-lg font-bold text-white">{selectedWorkflow.title}</h2>
                  <p className="text-xs text-slate-400 font-mono">ID: {selectedWorkflow.workflow_id} | Tenant: {selectedWorkflow.tenant_id}</p>
                </div>
                <div className="flex items-center gap-2">
                  {selectedWorkflow.state === 'RUNNING' ? (
                    <Button
                      variant="outline"
                      onClick={() => handlePause(selectedWorkflow.workflow_id)}
                      disabled={actionLoading}
                    >
                      <span className="flex items-center gap-2 text-amber-400">
                        <Pause className="w-4 h-4" /> Pause Workflow
                      </span>
                    </Button>
                  ) : (
                    <Button
                      variant="intelligence"
                      onClick={() => handleResume(selectedWorkflow.workflow_id)}
                      disabled={actionLoading}
                    >
                      <span className="flex items-center gap-2">
                        <Play className="w-4 h-4" /> Resume Workflow
                      </span>
                    </Button>
                  )}
                </div>
              </div>

              {/* Step Progress Bar */}
              <div>
                <span className="text-xs text-slate-400 block mb-2">Execution Pipeline Progress</span>
                <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                  <div
                    className="bg-indigo-500 h-full rounded-full transition-all"
                    style={{
                      width: `${((selectedWorkflow.current_step_index + 1) / selectedWorkflow.total_steps) * 100}%`,
                    }}
                  />
                </div>
              </div>

              {/* Checkpoint Timeline */}
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  Durable Checkpoints Recorded ({selectedWorkflow.checkpoints?.length ?? 0})
                </h3>

                {selectedWorkflow.checkpoints?.length ? (
                  selectedWorkflow.checkpoints.map((chk) => (
                    <div
                      key={chk.checkpoint_id}
                      className="p-3 bg-slate-800/40 rounded-xl border border-slate-700 text-xs space-y-2"
                    >
                      <div className="flex justify-between items-center">
                        <span className="font-mono text-indigo-300 font-bold">{chk.checkpoint_id}</span>
                        <span className="text-slate-400">{new Date(chk.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <div className="flex justify-between items-center text-slate-300 font-mono text-[11px]">
                        <span>Fencing Token: #{chk.fencing_token}</span>
                        <span className="text-slate-400 truncate max-w-[200px]">SHA: {chk.state_hash}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 italic">No checkpoints recorded yet.</p>
                )}
              </div>
            </Card>
          ) : (
            <Card className="p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm">
              Select a workflow to inspect durable state details.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
