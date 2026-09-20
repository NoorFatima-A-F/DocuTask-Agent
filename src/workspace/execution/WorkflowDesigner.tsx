import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Workflow,
  RotateCw,
  ArrowRight,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { WorkflowDefinition } from '../../types/executionPlatform';

export const WorkflowDesigner: React.FC = () => {
  const [workflows, setWorkflows] = useState<WorkflowDefinition[]>([]);
  const [selectedWf, setSelectedWf] = useState<WorkflowDefinition | null>(null);
  const [tiers, setTiers] = useState<string[][]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  const loadWorkflows = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listWorkflows();
      setWorkflows(res.workflows || []);
      if (res.workflows && res.workflows.length > 0 && res.workflows[0]) {
        selectWorkflow(res.workflows[0].workflow_id);
      }
    } catch (err) {
      console.error('Failed to load workflows:', err);
    } finally {
      setLoading(false);
    }
  };

  const selectWorkflow = async (wfId: string) => {
    try {
      const res = await executionPlatformApiClient.getWorkflow(wfId);
      setSelectedWf(res.workflow);
      setTiers(res.tiers || []);
    } catch (err) {
      console.error('Failed to get workflow details:', err);
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
            <Workflow className="w-5 h-5 text-purple-400" />
            Workflow DAG & Saga Designer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Topological tier orchestrator, cycle detection engine, and automated compensation DAG inversion
          </p>
        </div>
        <Button variant="outline" onClick={loadWorkflows}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Workflow Selector */}
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm font-semibold text-white">Registered Pipelines ({workflows.length})</CardTitle>
          </CardHeader>
          <CardContent className="space-y-2">
            {loading && workflows.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading pipelines...</p>
            ) : workflows.map((wf) => (
              <div
                key={wf.workflow_id}
                onClick={() => selectWorkflow(wf.workflow_id)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedWf?.workflow_id === wf.workflow_id
                    ? 'bg-purple-950/40 border-purple-600'
                    : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-white truncate max-w-[180px]">{wf.name}</span>
                  <Badge variant="intelligence">{wf.mode}</Badge>
                </div>
                <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{wf.description}</p>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right: DAG Visualizer & Execution Order */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white">
                {selectedWf ? selectedWf.name : 'Select a Workflow'}
              </CardTitle>
              {selectedWf && (
                <Badge variant="outline" className="text-xs">
                  {selectedWf.steps.length} Steps • {selectedWf.risk_level} Risk
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {selectedWf && (
              <>
                {/* Topological Execution Tiers */}
                <div>
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
                    Topological Parallel Execution Tiers (Kahn's Sort)
                  </h4>
                  <div className="flex flex-wrap items-center gap-3">
                    {tiers.map((tier, idx) => (
                      <div key={idx} className="flex items-center gap-2">
                        <div className="p-3 bg-slate-950 border border-purple-800/50 rounded-lg">
                          <span className="text-[10px] text-purple-400 font-bold block mb-1">TIER {idx + 1}</span>
                          <div className="flex flex-wrap gap-1.5">
                            {tier.map((stepId) => (
                              <span key={stepId} className="px-2 py-0.5 bg-purple-900/40 text-purple-200 text-xs rounded">
                                {stepId}
                              </span>
                            ))}
                          </div>
                        </div>
                        {idx < tiers.length - 1 && <ArrowRight className="w-4 h-4 text-slate-600" />}
                      </div>
                    ))}
                  </div>
                </div>

                {/* Step Node Cards */}
                <div className="space-y-3">
                  <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
                    Workflow Node Specifications
                  </h4>
                  {selectedWf.steps.map((step) => (
                    <div
                      key={step.step_id}
                      className="p-3 bg-slate-800/40 border border-slate-700/60 rounded-xl flex flex-col md:flex-row md:items-center justify-between gap-3"
                    >
                      <div>
                        <div className="flex items-center gap-2">
                          <span className="text-sm font-semibold text-white">{step.name}</span>
                          <span className="text-xs font-mono text-purple-400">({step.step_id})</span>
                        </div>
                        <p className="text-xs text-slate-400 mt-1">
                          Tool: <span className="font-mono text-slate-300">{step.tool_id}</span>
                          {step.depends_on.length > 0 && ` • Depends on: ${step.depends_on.join(', ')}`}
                        </p>
                      </div>
                      <div className="flex items-center gap-2">
                        {step.is_compensable ? (
                          <Badge variant="success">Compensable (Saga)</Badge>
                        ) : (
                          <Badge variant="warning">Non-Compensable</Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
