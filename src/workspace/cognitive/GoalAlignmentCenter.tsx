import React, { useState, useEffect } from 'react';
import { Target, RefreshCw } from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { cognitiveApiClient } from '../../services/cognitiveApiClient';
import { GoalAlignmentNode } from '../../types/cognitive';

export const GoalAlignmentCenter: React.FC = () => {
  const [goals, setGoals] = useState<GoalAlignmentNode[]>([]);

  const loadData = async () => {
    const data = await cognitiveApiClient.getGoalAlignments();
    setGoals(data);
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-slate-100 flex items-center gap-2">
            <Target className="w-7 h-7 text-indigo-400" />
            Enterprise Goal Alignment & KPI Hierarchy
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Binds every autonomous agent directly to Department Goals, Business Objectives, and Corporate KPIs.
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
        {goals.map((g) => (
          <Card key={g.id} className="p-5 bg-slate-900/60 border-slate-800 space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <Badge variant="outline" className="text-indigo-400 border-indigo-500/30 mb-1">
                  Corporate KPI
                </Badge>
                <h3 className="text-lg font-bold text-slate-100">{g.corporate_kpi}</h3>
              </div>
              <Badge variant="success">Progress: {g.current_progress_pct}%</Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="font-semibold text-slate-400 uppercase">Business Objective:</span>
                <p className="text-slate-200 mt-1">{g.business_goal}</p>
              </div>
              <div className="p-3 bg-slate-800/40 rounded border border-slate-700/50">
                <span className="font-semibold text-slate-400 uppercase">Department Target:</span>
                <p className="text-slate-200 mt-1">{g.department_goal}</p>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800 flex justify-between items-center text-xs text-slate-400">
              <span>Assigned Agents: {g.assigned_agents.join(', ')}</span>
              <span className="text-emerald-400 font-semibold">Health: {g.alignment_health}</span>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
