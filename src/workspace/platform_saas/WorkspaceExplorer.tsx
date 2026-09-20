import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { Workspace, Project } from '../../types/saasPlatform';
import { LayoutGrid, FolderGit2, HardDrive, Users, RefreshCw } from 'lucide-react';

export const WorkspaceExplorer: React.FC = () => {
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const [ws, prj] = await Promise.all([
        SaaSApiClient.listWorkspaces('tenant_acme_corp'),
        SaaSApiClient.listProjects('tenant_acme_corp'),
      ]);
      setWorkspaces(ws);
      setProjects(prj);
      setLoading(false);
    };
    load();
  }, []);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <LayoutGrid className="w-7 h-7 text-indigo-400" />
            Workspaces & Project Namespaces
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Scoped team workspaces, agent allocations, storage quotas, and autonomous pipelines.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Workspaces...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {workspaces.map((ws) => {
            const wsProjects = projects.filter((p) => p.workspace_id === ws.workspace_id);
            return (
              <Card key={ws.workspace_id} className="bg-slate-900/80 border-slate-800">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg text-white">{ws.name}</CardTitle>
                      <span className="text-xs font-mono text-slate-400">{ws.workspace_id}</span>
                    </div>
                    <Badge variant="intelligence">{ws.slug}</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid grid-cols-2 gap-3 text-xs bg-slate-800/40 p-3 rounded">
                    <div className="flex items-center gap-2">
                      <Users className="w-4 h-4 text-indigo-400" />
                      <div>
                        <span className="text-slate-400 block text-[10px]">Allocated Agents</span>
                        <span className="font-bold text-white">{ws.allocated_agents_count} Concurrency</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-2">
                      <HardDrive className="w-4 h-4 text-cyan-400" />
                      <div>
                        <span className="text-slate-400 block text-[10px]">Storage Quota</span>
                        <span className="font-bold text-white">{ws.allocated_storage_gb} GB</span>
                      </div>
                    </div>
                  </div>

                  <div>
                    <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-2">
                      Active Projects ({wsProjects.length})
                    </span>
                    <div className="space-y-2">
                      {wsProjects.map((p) => (
                        <div
                          key={p.project_id}
                          className="p-3 bg-slate-800/60 rounded border border-slate-700/60 flex items-center justify-between"
                        >
                          <div className="flex items-center gap-2">
                            <FolderGit2 className="w-4 h-4 text-emerald-400" />
                            <div>
                              <span className="text-sm font-medium text-slate-200 block">{p.name}</span>
                              <span className="text-xs text-slate-400">{p.description}</span>
                            </div>
                          </div>
                          <Badge variant="success" className="text-[10px]">
                            {p.active_workflows_count} Workflows
                          </Badge>
                        </div>
                      ))}
                      {wsProjects.length === 0 && (
                        <p className="text-xs text-slate-500 italic">No projects initialized yet.</p>
                      )}
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
