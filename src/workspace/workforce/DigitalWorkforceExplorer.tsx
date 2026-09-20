import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { workforceApiClient } from '../../services/workforceApiClient';
import { DigitalEmployee } from '../../types/workforce';
import { Search, UserCheck, Award, DollarSign, ShieldAlert, Cpu } from 'lucide-react';

export const DigitalWorkforceExplorer: React.FC = () => {
  const [employees, setEmployees] = useState<DigitalEmployee[]>([]);
  const [search, setSearch] = useState('');
  const [deptFilter, setDeptFilter] = useState<string>('ALL');

  useEffect(() => {
    workforceApiClient.getEmployees().then(setEmployees);
  }, []);

  const filtered = employees.filter(e => {
    const matchesSearch = e.name.toLowerCase().includes(search.toLowerCase()) || e.skills.some(s => s.toLowerCase().includes(search.toLowerCase()));
    const matchesDept = deptFilter === 'ALL' || e.department === deptFilter;
    return matchesSearch && matchesDept;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-5 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <span className="p-2 bg-blue-500/20 text-blue-400 rounded-xl">🤖</span>
            Digital Workforce Explorer
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Enterprise Directory of Autonomous Digital Employees & Career State
          </p>
        </div>
        <div className="flex gap-3 w-full md:w-auto">
          <div className="relative w-64">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              placeholder="Search employee or skill..."
              value={search}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setSearch(e.target.value)}
              className="pl-9 bg-slate-950 border border-slate-800 text-slate-200 rounded-xl px-3 py-2 text-sm w-full"
            />
          </div>
          <select
            value={deptFilter}
            onChange={(e: React.ChangeEvent<HTMLSelectElement>) => setDeptFilter(e.target.value)}
            aria-label="Filter employees by department"
            className="bg-slate-950 border border-slate-800 text-slate-300 rounded-xl px-3 py-2 text-sm"
          >
            <option value="ALL">All Departments</option>
            <option value="EXECUTIVE">Executive</option>
            <option value="ENGINEERING">Engineering</option>
            <option value="OPERATIONS">Operations</option>
            <option value="SECURITY_COMPLIANCE">Security</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map(emp => (
          <Card key={emp.id} className="p-5 bg-slate-900/50 border-slate-800 hover:border-slate-700 transition">
            <div className="flex justify-between items-start mb-3">
              <div>
                <div className="text-base font-bold text-white">{emp.name}</div>
                <div className="text-xs text-indigo-400 font-medium">{emp.role} • Level {emp.level}</div>
              </div>
              <Badge variant={emp.availability_status === 'ACTIVE' ? 'default' : 'outline'}>
                {emp.availability_status}
              </Badge>
            </div>

            <div className="space-y-2 text-xs text-slate-400 my-4 border-y border-slate-800/80 py-3">
              <div className="flex justify-between">
                <span className="flex items-center gap-1.5"><Award className="w-3.5 h-3.5 text-amber-400" /> Trust Score:</span>
                <strong className="text-white">{emp.trust_score}</strong>
              </div>
              <div className="flex justify-between">
                <span className="flex items-center gap-1.5"><UserCheck className="w-3.5 h-3.5 text-emerald-400" /> Success Rate:</span>
                <strong className="text-white">{Math.round(emp.task_success_rate * 100)}%</strong>
              </div>
              <div className="flex justify-between">
                <span className="flex items-center gap-1.5"><DollarSign className="w-3.5 h-3.5 text-blue-400" /> Rate Model:</span>
                <strong className="text-white">${emp.hourly_salary_usd.toFixed(2)}/hr</strong>
              </div>
              <div className="flex justify-between">
                <span className="flex items-center gap-1.5"><ShieldAlert className="w-3.5 h-3.5 text-purple-400" /> Clearance:</span>
                <strong className="text-purple-300">{emp.security_clearance}</strong>
              </div>
            </div>

            <div className="mb-4">
              <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">Certified Skills</div>
              <div className="flex flex-wrap gap-1.5">
                {emp.skills.map((s, idx) => (
                  <span key={idx} className="text-[10px] px-2 py-0.5 bg-slate-800 rounded-md text-slate-300 border border-slate-700">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            <div className="pt-2 flex justify-between items-center text-xs">
              <span className="text-slate-500">Tasks: {emp.lifetime_tasks_completed}</span>
              <Button variant="outline" size="sm">
                <span className="flex items-center gap-1">
                  <Cpu className="w-3 h-3" /> Profile
                </span>
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
