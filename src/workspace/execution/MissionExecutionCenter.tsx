import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Play,
  RotateCw,
  Clock,
  Send,
  Workflow,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { MissionExecution } from '../../types/executionPlatform';

export const MissionExecutionCenter: React.FC = () => {
  const [missions, setMissions] = useState<MissionExecution[]>([]);
  const [selectedMission, setSelectedMission] = useState<MissionExecution | null>(null);
  const [goalInput, setGoalInput] = useState<string>('Deploy autonomous hotfix to canary and broadcast status');
  const [dryRun, setDryRun] = useState<boolean>(false);
  const [executing, setExecuting] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const loadMissions = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listMissions();
      setMissions(res.missions || []);
      if (res.missions && res.missions.length > 0 && !selectedMission) {
        setSelectedMission(res.missions[0] || null);
      }
    } catch (err) {
      console.error('Failed to load missions:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMissions();
  }, []);

  const handleExecute = async () => {
    if (!goalInput.trim()) return;
    try {
      setExecuting(true);
      const res = await executionPlatformApiClient.executeGoal({
        goal: goalInput,
        dry_run: dryRun,
        initiated_by: 'Mission Execution Control Room',
      });
      await loadMissions();
      setSelectedMission(res.mission);
    } catch (err) {
      console.error('Error executing mission:', err);
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Directive Dispatch Bar */}
      <Card className="bg-slate-900/80 border-purple-800/40 shadow-lg">
        <CardHeader>
          <CardTitle className="text-lg text-white flex items-center gap-2">
            <Send className="w-5 h-5 text-purple-400" />
            Dispatch Real-World Execution Mission
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              className="flex-1 bg-slate-950 border border-slate-700 rounded-lg px-4 py-2.5 text-white text-sm focus:outline-none focus:border-purple-500"
              placeholder="Enter natural language mission goal..."
              value={goalInput}
              onChange={(e) => setGoalInput(e.target.value)}
            />
            <div className="flex items-center gap-4">
              <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={dryRun}
                  onChange={(e) => setDryRun(e.target.checked)}
                  className="rounded bg-slate-950 border-slate-700 text-purple-600 focus:ring-0"
                />
                Dry Run Simulation Only
              </label>
              <Button
                variant="intelligence"
                onClick={handleExecute}
                disabled={executing || !goalInput.trim()}
              >
                <span className="flex items-center gap-2">
                  <Play className="w-4 h-4" />
                  {executing ? 'Executing Mission Pipeline...' : 'Dispatch Mission'}
                </span>
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Main Dual Pane: Mission History List & Detail Stepper */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Mission History */}
        <Card className="lg:col-span-1 bg-slate-900/60 border-slate-800">
          <CardHeader className="flex flex-row items-center justify-between pb-3">
            <CardTitle className="text-sm font-semibold text-white flex items-center gap-2">
              <Clock className="w-4 h-4 text-slate-400" />
              Mission Registry ({missions.length})
            </CardTitle>
            <Button variant="ghost" onClick={loadMissions}>
              <span className="flex items-center gap-1 text-xs text-slate-400 hover:text-white">
                <RotateCw className="w-3.5 h-3.5" />
                Refresh
              </span>
            </Button>
          </CardHeader>
          <CardContent className="space-y-2 max-h-[600px] overflow-y-auto">
            {loading && missions.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">Loading missions...</p>
            ) : missions.length === 0 ? (
              <p className="text-xs text-slate-500 py-4 text-center">No missions registered yet.</p>
            ) : (
              missions.map((m) => (
                <div
                  key={m.mission_id}
                  onClick={() => setSelectedMission(m)}
                  className={`p-3 rounded-lg border cursor-pointer transition-all ${
                    selectedMission?.mission_id === m.mission_id
                      ? 'bg-purple-950/40 border-purple-600'
                      : 'bg-slate-800/40 border-slate-800 hover:border-slate-700'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-medium text-white truncate max-w-[180px]">
                      {m.goal}
                    </span>
                    <Badge
                      variant={
                        m.status === 'completed'
                          ? 'success'
                          : m.status === 'executing'
                          ? 'intelligence'
                          : m.status === 'rolled_back'
                          ? 'warning'
                          : 'error'
                      }
                    >
                      {m.status}
                    </Badge>
                  </div>
                  <div className="flex items-center justify-between mt-2 text-[11px] text-slate-400">
                    <span>{m.steps.length} Steps</span>
                    <span>{m.total_execution_time_ms}ms</span>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>

        {/* Right Column: Active Mission Stepper & Context */}
        <Card className="lg:col-span-2 bg-slate-900/60 border-slate-800">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-base text-white flex items-center gap-2">
                <Workflow className="w-5 h-5 text-purple-400" />
                {selectedMission ? selectedMission.goal : 'Select a Mission'}
              </CardTitle>
              {selectedMission && (
                <Badge variant="outline" className="text-xs">
                  {selectedMission.risk_level.toUpperCase()} RISK
                </Badge>
              )}
            </div>
          </CardHeader>
          <CardContent>
            {!selectedMission ? (
              <p className="text-sm text-slate-500 py-12 text-center">
                Select a mission from the list to view step traces and execution certificates.
              </p>
            ) : (
              <div className="space-y-6">
                {/* Meta Summary Bar */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 p-3 bg-slate-950/60 rounded-lg border border-slate-800 text-xs">
                  <div>
                    <span className="text-slate-500 block">Mission ID</span>
                    <span className="text-slate-300 font-mono">{selectedMission.mission_id}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Initiated By</span>
                    <span className="text-slate-300">{selectedMission.initiated_by}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Status</span>
                    <span className="text-emerald-400 font-semibold">{selectedMission.status}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 block">Execution Latency</span>
                    <span className="text-purple-300">{selectedMission.total_execution_time_ms} ms</span>
                  </div>
                </div>

                {/* Step Trace Timeline */}
                <div className="space-y-4">
                  <h3 className="text-sm font-semibold text-slate-200">Execution Stepper</h3>
                  <div className="space-y-3">
                    {selectedMission.steps.map((step, idx) => (
                      <div
                        key={step.step_id}
                        className="p-3.5 bg-slate-800/40 border border-slate-700/60 rounded-xl space-y-2"
                      >
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-2.5">
                            <span className="w-6 h-6 rounded-full bg-purple-900/60 border border-purple-600 flex items-center justify-center text-xs font-bold text-purple-200">
                              {idx + 1}
                            </span>
                            <span className="text-sm font-medium text-white">{step.name}</span>
                            <span className="text-xs font-mono text-purple-400 bg-purple-950/50 px-2 py-0.5 rounded border border-purple-800/40">
                              {step.tool_id}
                            </span>
                          </div>
                          <Badge
                            variant={
                              step.status === 'success'
                                ? 'success'
                                : step.status === 'running'
                                ? 'intelligence'
                                : 'warning'
                            }
                          >
                            {step.status}
                          </Badge>
                        </div>

                        {/* Step inputs and outputs */}
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs font-mono mt-2">
                          <div className="p-2 bg-slate-950 rounded border border-slate-800">
                            <span className="text-slate-500 block text-[10px]">INPUTS</span>
                            <pre className="text-slate-300 text-[11px] overflow-x-auto whitespace-pre-wrap">
                              {JSON.stringify(step.inputs, null, 2)}
                            </pre>
                          </div>
                          <div className="p-2 bg-slate-950 rounded border border-slate-800">
                            <span className="text-emerald-500 block text-[10px]">OUTPUT</span>
                            <pre className="text-emerald-300 text-[11px] overflow-x-auto whitespace-pre-wrap">
                              {step.output ? JSON.stringify(step.output, null, 2) : '(no output)'}
                            </pre>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};
