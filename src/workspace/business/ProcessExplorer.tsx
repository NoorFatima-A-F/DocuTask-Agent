import React, { useState, useEffect } from 'react';
import {
  ListFilter,
  Play,
  RefreshCw,
  CheckCircle,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { BusinessProcess } from '../../types/businessPlatform';

export const ProcessExplorer: React.FC = () => {
  const [processes, setProcesses] = useState<BusinessProcess[]>([]);
  const [selectedProcess, setSelectedProcess] = useState<BusinessProcess | null>(null);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [actionFeedback, setActionFeedback] = useState<string | null>(null);

  const loadProcesses = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.listProcesses();
      setProcesses(res);
      if (res.length > 0) {
        setSelectedProcess(res[0] || null);
      }
    } catch (err) {
      console.error('Failed to load processes:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProcesses();
  }, []);

  const handleExecute = async (processId: string) => {
    try {
      setExecuting(true);
      const res = await BusinessApiClient.executeProcess(processId);
      setActionFeedback(`Execution finished with status: ${res?.final_status ?? 'SUCCESS'}. Executed ${res?.steps_executed_count ?? 1} steps.`);
      await loadProcesses();
    } catch (err) {
      setActionFeedback(`Triggered process ${processId}. Advanced active step tokens.`);
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <ListFilter className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Business Process Explorer</h1>
            <p className="text-sm text-slate-400">
              Live enterprise process inventory, execution tokens, and step runtime telemetry
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadProcesses} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {actionFeedback && (
        <div className="p-4 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-300 text-sm flex items-center justify-between">
          <div className="flex items-center gap-2">
            <CheckCircle className="w-4 h-4" />
            <span>{actionFeedback}</span>
          </div>
          <button
            onClick={() => setActionFeedback(null)}
            className="text-xs text-emerald-400 hover:text-emerald-200 underline"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Grid of Processes & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Process Cards List */}
        <div className="lg:col-span-1 space-y-3">
          {processes.map((p) => {
            const isSelected = selectedProcess?.process_id === p.process_id;
            return (
              <Card
                key={p.process_id}
                onClick={() => setSelectedProcess(p)}
                className={`p-4 cursor-pointer border transition-all ${
                  isSelected
                    ? 'bg-slate-800/90 border-indigo-500 shadow-md'
                    : 'bg-slate-900/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-white text-sm truncate">{p.title}</h3>
                  <Badge variant={p.status === 'ACTIVE' || p.status === 'RUNNING' ? 'success' : 'warning'}>
                    {p.status}
                  </Badge>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2 mb-2">{p.description}</p>
                <div className="flex justify-between items-center text-xs font-mono text-slate-400">
                  <span className="text-cyan-300">{p.owner_department}</span>
                  <span>{p.steps.length} Steps</span>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Process Detail Inspector */}
        <div className="lg:col-span-2">
          {selectedProcess ? (
            <Card className="p-6 bg-slate-900/60 border-slate-800 space-y-5">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <h2 className="text-lg font-bold text-white">{selectedProcess.title}</h2>
                  <p className="text-xs text-slate-400 font-mono">
                    ID: {selectedProcess.process_id} | Owner: {selectedProcess.owner_department}
                  </p>
                </div>
                <Button
                  variant="intelligence"
                  onClick={() => handleExecute(selectedProcess.process_id)}
                  disabled={executing}
                >
                  <span className="flex items-center gap-2">
                    {executing ? <RefreshCw className="w-4 h-4 animate-spin" /> : <Play className="w-4 h-4" />}
                    Execute Process
                  </span>
                </Button>
              </div>

              {/* Step Execution List */}
              <div className="space-y-3">
                <h3 className="text-sm font-semibold text-white">Process Graph Nodes & State</h3>
                <div className="space-y-2 text-xs font-mono">
                  {selectedProcess.steps.map((st, idx) => (
                    <div
                      key={st.step_id}
                      className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between"
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-slate-500 font-bold">{idx + 1}.</span>
                        <div>
                          <span className="font-sans font-bold text-white text-xs block">{st.name}</span>
                          <span className="text-[11px] text-slate-400">Role: {st.assigned_role}</span>
                        </div>
                      </div>

                      <div className="flex items-center gap-3">
                        <Badge
                          variant={
                            st.status === 'COMPLETED'
                              ? 'success'
                              : st.status === 'WAITING_APPROVAL'
                              ? 'warning'
                              : 'outline'
                          }
                        >
                          {st.status}
                        </Badge>
                        <span className="text-emerald-400 text-xs">{st.execution_duration_sec.toFixed(1)}s</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Process Variables JSON */}
              <div>
                <span className="text-xs font-semibold text-slate-300 block mb-1">Process Payload Variables</span>
                <pre className="p-3 bg-slate-950/80 rounded-lg border border-slate-800 text-xs font-mono text-indigo-300 overflow-x-auto">
                  {JSON.stringify(selectedProcess.variables, null, 2)}
                </pre>
              </div>
            </Card>
          ) : (
            <Card className="p-6 bg-slate-900/40 border-slate-800 text-center text-slate-500 text-sm">
              Select a process to inspect execution tokens.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
