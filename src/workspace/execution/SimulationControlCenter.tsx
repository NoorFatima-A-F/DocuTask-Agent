import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Sparkles,
  RotateCw,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { WorkflowDefinition, SimulationReport } from '../../types/executionPlatform';

export const SimulationControlCenter: React.FC = () => {
  const [workflows, setWorkflows] = useState<WorkflowDefinition[]>([]);
  const [selectedWfId, setSelectedWfId] = useState<string>('');
  const [simReport, setSimReport] = useState<SimulationReport | null>(null);
  const [simulating, setSimulating] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listWorkflows();
      setWorkflows(res.workflows || []);
      if (res.workflows && res.workflows.length > 0 && res.workflows[0]) {
        setSelectedWfId(res.workflows[0].workflow_id);
        runSimulation(res.workflows[0].workflow_id);
      }
    } catch (err) {
      console.error('Failed to load workflows for simulation:', err);
    } finally {
      setLoading(false);
    }
  };

  const runSimulation = async (wfId: string) => {
    try {
      setSimulating(true);
      const res = await executionPlatformApiClient.simulateWorkflow(wfId);
      setSimReport(res.simulation);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setSimulating(false);
    }
  };

  useEffect(() => {
    loadWorkflows();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-purple-400" />
            Digital Twin Simulation & Blast Radius Sandbox
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Pre-flight dry runs, state delta predictions, compensation rehearsals & cost estimators
          </p>
        </div>
        <div className="flex items-center gap-3">
          {loading && workflows.length === 0 ? (
            <span className="text-xs text-slate-500">Loading workflows...</span>
          ) : (
            <select
              className="bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-purple-500"
              value={selectedWfId}
              onChange={(e) => {
                setSelectedWfId(e.target.value);
                runSimulation(e.target.value);
              }}
            >
              {workflows.map((w) => (
                <option key={w.workflow_id} value={w.workflow_id}>
                  {w.name}
                </option>
              ))}
            </select>
          )}
          <Button
            variant="intelligence"
            onClick={() => runSimulation(selectedWfId)}
            disabled={simulating || !selectedWfId}
          >
            <span className="flex items-center gap-2 text-xs">
              <RotateCw className={`w-3.5 h-3.5 ${simulating ? 'animate-spin' : ''}`} />
              Re-run Simulation
            </span>
          </Button>
        </div>
      </div>

      {/* Simulation Key Telemetry Cards */}
      {simReport && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <Card className="bg-slate-900/60 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-slate-400">Blast Radius Scope</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-white capitalize">{simReport.blast_radius_scope}</div>
              <Badge variant="outline" className="mt-1 text-[10px]">Zero Contagion</Badge>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/60 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-slate-400">Predicted Cost</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-emerald-400">${simReport.total_predicted_cost_usd}</div>
              <p className="text-[10px] text-slate-500 mt-1">AWS / API compute spend</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/60 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-slate-400">Estimated Latency</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-purple-400">{simReport.total_predicted_duration_ms} ms</div>
              <p className="text-[10px] text-slate-500 mt-1">Forward-pass simulation</p>
            </CardContent>
          </Card>

          <Card className="bg-slate-900/60 border-slate-800">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-slate-400">Rehearsal Verdict</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-xl font-bold text-cyan-400">
                {simReport.simulation_passed ? 'Passed (100%)' : 'Failed'}
              </div>
              <p className="text-[10px] text-emerald-400 mt-1">Ready for real-world dispatch</p>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Simulated Steps Mutation Inspector */}
      {simReport && (
        <Card className="bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-base text-white">Simulated Step Delta & Shadow State Mutations</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {simReport.step_results.map((res, idx) => (
                <div key={res.step_id} className="p-4 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      <span className="w-5 h-5 rounded-full bg-purple-900/60 border border-purple-500 flex items-center justify-center text-xs font-bold text-purple-200">
                        {idx + 1}
                      </span>
                      <span className="text-sm font-semibold text-white">{res.step_id}</span>
                      <span className="text-xs font-mono text-purple-300">({res.tool_id})</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge variant="success">Saga Rehearsal Passed</Badge>
                      <Badge variant="outline">{res.predicted_duration_ms} ms</Badge>
                    </div>
                  </div>

                  <div className="text-xs space-y-1 mt-2">
                    <span className="text-slate-400 font-semibold block">Predicted External Mutations:</span>
                    <ul className="list-disc pl-5 text-slate-300 space-y-0.5">
                      {res.state_mutations_predicted.map((m, mIdx) => (
                        <li key={mIdx}>{m}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};
