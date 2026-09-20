import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  GitBranch,
  RotateCw,
  Zap,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { ExecutionPlan } from '../../types/executionPlatform';

export const ExecutionPlannerStudio: React.FC = () => {
  const [plans, setPlans] = useState<ExecutionPlan[]>([]);
  const [selectedPlan, setSelectedPlan] = useState<ExecutionPlan | null>(null);
  const [goalPrompt, setGoalPrompt] = useState<string>('Deploy autonomous hotfix to production kubernetes cluster');
  const [planning, setPlanning] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const loadPlans = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listPlans();
      setPlans(res.plans || []);
      if (res.plans && res.plans.length > 0 && !selectedPlan) {
        setSelectedPlan(res.plans[0] || null);
      }
    } catch (err) {
      console.error('Failed to load plans:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPlans();
  }, []);

  const handleCreatePlan = async () => {
    if (!goalPrompt.trim()) return;
    try {
      setPlanning(true);
      const res = await executionPlatformApiClient.planMission({ mission_goal: goalPrompt });
      await loadPlans();
      setSelectedPlan(res.plan);
    } catch (err) {
      console.error('Error creating plan:', err);
    } finally {
      setPlanning(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Planner Bar */}
      <Card className="bg-slate-900/80 border-purple-800/40">
        <CardHeader>
          <CardTitle className="text-lg text-white flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-purple-400" />
            Critical Path Method (CPM) Planner Studio
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-3">
            <input
              type="text"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-purple-500"
              placeholder="Enter mission goal for CPM Critical Path graph synthesis..."
              value={goalPrompt}
              onChange={(e) => setGoalPrompt(e.target.value)}
            />
            <Button variant="intelligence" onClick={handleCreatePlan} disabled={planning || !goalPrompt.trim()}>
              <span className="flex items-center gap-2">
                <Zap className="w-4 h-4" />
                {planning ? 'Computing Critical Path...' : 'Compile Execution Plan'}
              </span>
            </Button>
          </div>
        </CardContent>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Saved Plans */}
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-sm font-semibold text-white">Generated Plans ({plans.length})</CardTitle>
            <Button variant="ghost" onClick={loadPlans}>
              <span className="flex items-center gap-1 text-xs text-slate-400">
                <RotateCw className="w-3.5 h-3.5" />
                Refresh
              </span>
            </Button>
          </CardHeader>
          <CardContent className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading && plans.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading plans...</p>
            ) : plans.map((p) => (
              <div
                key={p.plan_id}
                onClick={() => setSelectedPlan(p)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  selectedPlan?.plan_id === p.plan_id
                    ? 'bg-purple-950/40 border-purple-600'
                    : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="text-xs font-semibold text-white truncate max-w-[170px]">
                    {p.mission_goal}
                  </span>
                  <Badge variant="outline">{p.overall_risk}</Badge>
                </div>
                <div className="flex items-center justify-between mt-2 text-[11px] text-slate-400 font-mono">
                  <span>{p.nodes.length} Nodes</span>
                  <span>{p.total_estimated_duration_ms}ms total</span>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>

        {/* Right: Critical Path Graph & Slack Calculations */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white">
                {selectedPlan ? selectedPlan.mission_goal : 'Select a Plan'}
              </CardTitle>
              {selectedPlan && (
                <span className="text-xs font-mono text-purple-400">
                  Critical Steps: {selectedPlan.critical_path_steps.length}
                </span>
              )}
            </div>
          </CardHeader>
          <CardContent className="space-y-4">
            {selectedPlan && (
              <>
                <div className="border border-slate-800 rounded-xl overflow-hidden">
                  <table className="w-full text-left text-xs">
                    <thead className="bg-slate-950 text-slate-400 font-mono">
                      <tr>
                        <th className="p-3">Step / Tool</th>
                        <th className="p-3">Est. Duration</th>
                        <th className="p-3">Early (ES/EF)</th>
                        <th className="p-3">Late (LS/LF)</th>
                        <th className="p-3">Slack</th>
                        <th className="p-3">Critical Path</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800 text-slate-300">
                      {selectedPlan.nodes.map((n) => (
                        <tr
                          key={n.step_id}
                          className={n.is_critical_path ? 'bg-purple-950/20' : 'hover:bg-slate-800/30'}
                        >
                          <td className="p-3 font-medium">
                            <span className="text-white block">{n.name}</span>
                            <span className="text-[11px] font-mono text-purple-400">{n.tool_id}</span>
                          </td>
                          <td className="p-3 font-mono">{n.estimated_duration_ms} ms</td>
                          <td className="p-3 font-mono text-slate-400">
                            {n.early_start} / {n.early_finish}
                          </td>
                          <td className="p-3 font-mono text-slate-400">
                            {n.late_start} / {n.late_finish}
                          </td>
                          <td className="p-3 font-mono">
                            <span className={n.slack === 0 ? 'text-amber-400 font-bold' : 'text-slate-400'}>
                              {n.slack} ms
                            </span>
                          </td>
                          <td className="p-3">
                            {n.is_critical_path ? (
                              <Badge variant="intelligence">CRITICAL</Badge>
                            ) : (
                              <Badge variant="outline">Buffer</Badge>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
