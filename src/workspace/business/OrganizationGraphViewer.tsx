import React, { useState, useEffect } from 'react';
import {
  Users,
  RefreshCw,
  Building,
  Shield,
  Server,
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import { BusinessApiClient } from '../../services/businessApiClient';
import { OrganizationGraph } from '../../types/businessPlatform';

export const OrganizationGraphViewer: React.FC = () => {
  const [org, setOrg] = useState<OrganizationGraph | null>(null);
  const [loading, setLoading] = useState(true);

  const loadOrg = async () => {
    try {
      setLoading(true);
      const res = await BusinessApiClient.getOrganization();
      setOrg(res);
    } catch (err) {
      console.error('Failed to load organization graph:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrg();
  }, []);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 rounded-xl border border-indigo-500/20 text-indigo-400">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Enterprise Knowledge Graph</h1>
            <p className="text-sm text-slate-400">
              Departmental ontology, employee/agent role hierarchies, and approval matrices
            </p>
          </div>
        </div>

        <Button variant="outline" onClick={loadOrg} disabled={loading}>
          <span className="flex items-center gap-2">
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Departments Grid */}
      <div>
        <h2 className="text-base font-semibold text-white mb-3 flex items-center gap-2">
          <Building className="w-4 h-4 text-indigo-400" />
          Enterprise Business Units & Departments
        </h2>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {org?.departments.map((d) => (
            <Card key={d.department_id} className="p-5 bg-slate-900/40 border-slate-800 space-y-3">
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-bold text-white text-sm">{d.name}</h3>
                  <span className="text-xs text-slate-400 font-mono">Head: {d.head_role}</span>
                </div>
                <Badge variant="outline">{d.members_count} Staff</Badge>
              </div>
              <div className="pt-2 border-t border-slate-800/80 text-xs text-slate-300 flex justify-between">
                <span>Active Workflows:</span>
                <span className="font-bold text-indigo-300 font-mono">{d.active_processes_count}</span>
              </div>
            </Card>
          ))}
        </div>
      </div>

      {/* Roles & Systems Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Roles & Agents */}
        <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Shield className="w-4 h-4 text-emerald-400" />
            Roles, Delegations & Approval Limits
          </h2>
          <div className="space-y-3 text-xs">
            {org?.roles.map((r) => (
              <div
                key={r.role_id}
                className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between"
              >
                <div>
                  <div className="flex items-center gap-2">
                    <span className="font-bold text-white text-xs">{r.title}</span>
                    <Badge variant={r.is_autonomous_agent ? 'intelligence' : 'default'}>
                      {r.is_autonomous_agent ? 'AI Agent' : 'Human'}
                    </Badge>
                  </div>
                  <span className="text-slate-400 text-[11px] block mt-0.5">
                    Limit: ${r.approval_limit_amount.toLocaleString()} USD
                  </span>
                </div>
                <span className="text-cyan-300 font-mono text-[11px]">{r.department_id}</span>
              </div>
            ))}
          </div>
        </Card>

        {/* Enterprise Systems */}
        <Card className="p-6 bg-slate-900/40 border-slate-800 space-y-4">
          <h2 className="text-base font-semibold text-white flex items-center gap-2">
            <Server className="w-4 h-4 text-cyan-400" />
            Connected Enterprise IT Systems
          </h2>
          <div className="space-y-3 text-xs">
            {org?.systems.map((s) => (
              <div
                key={s.system_id}
                className="p-3 bg-slate-800/40 rounded-xl border border-slate-700/60 flex items-center justify-between"
              >
                <div>
                  <span className="font-bold text-white text-xs block">{s.name}</span>
                  <span className="text-slate-400 text-[11px]">Type: {s.system_type}</span>
                </div>
                <Badge variant="success">{s.status}</Badge>
              </div>
            ))}
          </div>
        </Card>
      </div>
    </div>
  );
};
