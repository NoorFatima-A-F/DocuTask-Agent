import React, { useState, useEffect } from 'react';
import {
  Shield,
  RefreshCw,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { DistributedApiClient } from '../../services/distributedApiClient';
import { DurableWorkflow, WorkflowCheckpoint } from '../../types/distributedPlatform';

export const CheckpointExplorer: React.FC = () => {
  const [workflows, setWorkflows] = useState<DurableWorkflow[]>([]);
  const [selectedWorkflowId, setSelectedWorkflowId] = useState<string>('');
  const [checkpoints, setCheckpoints] = useState<WorkflowCheckpoint[]>([]);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState<WorkflowCheckpoint | null>(null);
  const [loading, setLoading] = useState(true);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const res = await DistributedApiClient.getDurableWorkflows();
      setWorkflows(res);
      if (res.length > 0) {
        const firstWf = res[0];
        if (firstWf) {
          setSelectedWorkflowId(firstWf.workflow_id);
          const chks = await DistributedApiClient.getCheckpoints(firstWf.workflow_id);
          const fullList = chks.length > 0 ? chks : firstWf.checkpoints || [];
          setCheckpoints(fullList);
          if (fullList.length > 0) {
            setSelectedCheckpoint(fullList[0] || null);
          }
        }
      }
    } catch (err) {
      console.error('Failed to load checkpoints:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, []);

  const handleSelectWorkflow = async (wfId: string) => {
    setSelectedWorkflowId(wfId);
    try {
      const chks = await DistributedApiClient.getCheckpoints(wfId);
      const matched = workflows.find((w) => w.workflow_id === wfId);
      const list = chks.length > 0 ? chks : matched?.checkpoints || [];
      setCheckpoints(list);
      setSelectedCheckpoint(list[0] || null);
    } catch (err) {
      console.error('Failed to load checkpoints for workflow:', err);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Shield className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Checkpoint & State Explorer</h1>
            <p className="text-sm text-slate-400">
              Immutable snapshot verification, monotonic fencing tokens & crash-recovery state audits
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <select
            value={selectedWorkflowId}
            onChange={(e) => handleSelectWorkflow(e.target.value)}
            className="bg-slate-800 border border-slate-700 text-slate-200 text-sm rounded-lg px-3 py-2"
          >
            {workflows.map((w) => (
              <option key={w.workflow_id} value={w.workflow_id}>
                {w.title} ({w.workflow_id})
              </option>
            ))}
          </select>

          <Button variant="outline" onClick={loadWorkflows} disabled={loading}>
            <span className="flex items-center gap-2">
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Checkpoints List */}
        <div className="lg:col-span-1 space-y-3">
          {checkpoints.map((chk) => {
            const isSelected = selectedCheckpoint?.checkpoint_id === chk.checkpoint_id;
            return (
              <Card
                key={chk.checkpoint_id}
                onClick={() => setSelectedCheckpoint(chk)}
                className={`p-4 cursor-pointer border transition-all ${
                  isSelected
                    ? 'bg-slate-800/80 border-indigo-500 shadow-md'
                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono font-bold text-indigo-300 text-xs">{chk.checkpoint_id}</span>
                  <Badge variant="intelligence">Token #{chk.fencing_token}</Badge>
                </div>
                <div className="text-xs text-slate-400 flex justify-between">
                  <span>Step {chk.step_index + 1}</span>
                  <span>{new Date(chk.timestamp).toLocaleTimeString()}</span>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Checkpoint Detail Inspector */}
        <div className="lg:col-span-2">
          {selectedCheckpoint ? (
            <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-5">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <div>
                  <h3 className="text-base font-bold text-white">Snapshot Details</h3>
                  <p className="text-xs font-mono text-slate-400">ID: {selectedCheckpoint.checkpoint_id}</p>
                </div>
                <Badge variant="success">Cryptographically Sealed</Badge>
              </div>

              <div className="grid grid-cols-2 gap-4 text-xs font-mono">
                <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                  <span className="text-slate-500 block">Fencing Token</span>
                  <span className="text-white font-bold text-sm">#{selectedCheckpoint.fencing_token}</span>
                </div>
                <div className="p-3 bg-slate-800/40 rounded-lg border border-slate-700/60">
                  <span className="text-slate-500 block">SHA-256 State Hash</span>
                  <span className="text-emerald-400 text-xs truncate block">{selectedCheckpoint.state_hash}</span>
                </div>
              </div>

              {/* Variables */}
              <div>
                <span className="text-xs font-semibold text-slate-300 block mb-2">Workflow Variables</span>
                <pre className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto">
                  {JSON.stringify(selectedCheckpoint.variables, null, 2)}
                </pre>
              </div>

              {/* Memory Context */}
              <div>
                <span className="text-xs font-semibold text-slate-300 block mb-2">Memory Context</span>
                <pre className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-amber-300 overflow-x-auto">
                  {JSON.stringify(selectedCheckpoint.memory_context, null, 2)}
                </pre>
              </div>
            </Card>
          ) : (
            <Card className="p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm">
              No checkpoint selected.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
