import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { Department } from '../../types/workforce';
import { Layers, RefreshCw } from 'lucide-react';

export const OrganizationChartStudio: React.FC = () => {
  const [departments, setDepartments] = useState<Department[]>([]);
  const [loading, setLoading] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const depts = await workforceApiClient.getDepartments();
      setDepartments(depts);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-xl">🌳</span>
            Organization Chart Studio
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Hierarchical Reporting Trees, Matrix Units, and Reporting Lines
          </p>
        </div>
        <Button variant="outline" onClick={loadData} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh Hierarchy
          </span>
        </Button>
      </div>

      {/* Executive Node */}
      <div className="flex justify-center">
        <Card className="p-6 bg-indigo-950/40 border-indigo-500/50 max-w-md w-full text-center relative shadow-lg shadow-indigo-500/10">
          <Badge variant="default" className="mb-2">CHIEF EXECUTIVE OFFICER</Badge>
          <div className="text-lg font-bold text-white">Astraea Core (CEO)</div>
          <p className="text-xs text-indigo-300 mt-1">Master Autonomous Orchestration & Governance</p>
          <div className="mt-3 text-[11px] text-slate-400">Clearance: TOP_SECRET • Trust: 0.99</div>
        </Card>
      </div>

      <div className="flex justify-center my-2">
        <div className="w-0.5 h-8 bg-slate-700"></div>
      </div>

      {/* Departments Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {departments.map((d) => (
          <Card key={d.id} className="p-5 bg-slate-900/50 border-slate-800">
            <div className="flex justify-between items-start mb-3">
              <div className="text-base font-bold text-white">{d.name}</div>
              <Badge variant="outline">{d.dept_type}</Badge>
            </div>

            <div className="text-xs text-slate-400 space-y-2 mb-4">
              <div className="flex justify-between">
                <span>Headcount:</span>
                <strong className="text-white">{d.headcount} Agents</strong>
              </div>
              <div className="flex justify-between">
                <span>Monthly Budget:</span>
                <strong className="text-emerald-400">${d.monthly_budget_usd.toLocaleString()}</strong>
              </div>
            </div>

            <div className="border-t border-slate-800 pt-3">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Layers className="w-3.5 h-3.5 text-indigo-400" /> Active OKRs
              </div>
              <ul className="space-y-1">
                {d.okrs.map((okr, idx) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                    <span className="text-emerald-400">✓</span> {okr}
                  </li>
                ))}
              </ul>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
