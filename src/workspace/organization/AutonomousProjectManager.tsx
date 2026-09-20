import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  FolderKanban,
  RotateCw,
  Sparkles,
  Layers,
  Flag,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { VirtualProject } from '../../types/organizationPlatform';

export const AutonomousProjectManager: React.FC = () => {
  const [projects, setProjects] = useState<VirtualProject[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [selectedProject, setSelectedProject] = useState<VirtualProject | null>(null);
  const [replanning, setReplanning] = useState<boolean>(false);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getProjects();
      setProjects(data);
      if (data.length > 0 && !selectedProject) {
        setSelectedProject(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load projects:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleReplan = async (projectId: string) => {
    try {
      setReplanning(true);
      const updated = await organizationPlatformApiClient.replanProject(projectId);
      setSelectedProject(updated);
      await loadProjects();
    } catch (err) {
      console.error('Error replanning project:', err);
    } finally {
      setReplanning(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <FolderKanban className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Autonomous Project Manager</h1>
            <p className="text-sm text-muted-foreground">
              Work Breakdown Structures, Critical Path Method (CPM) Analysis & Autonomous Replanning
            </p>
          </div>
        </div>
        <Button variant="outline" onClick={loadProjects} disabled={loading}>
          <span className="flex items-center gap-2">
            <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            Refresh
          </span>
        </Button>
      </div>

      {/* Main Two-Column View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Project Selector */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold">Active Virtual Projects ({projects.length})</h2>
          <div className="space-y-3">
            {projects.map((p) => (
              <Card
                key={p.project_id}
                onClick={() => setSelectedProject(p)}
                className={`border cursor-pointer transition-all ${
                  selectedProject?.project_id === p.project_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/30'
                }`}
              >
                <CardContent className="p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-sm line-clamp-1">{p.title}</span>
                    <Badge variant={p.status === 'ACTIVE' ? 'success' : 'outline'}>{p.status}</Badge>
                  </div>
                  <p className="text-xs text-muted-foreground line-clamp-2">{p.description}</p>
                  <div className="space-y-1 pt-2">
                    <div className="flex justify-between text-xs text-muted-foreground">
                      <span>Progress:</span>
                      <span className="font-semibold text-foreground">{p.total_progress_percent}%</span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-primary h-full rounded-full transition-all"
                        style={{ width: `${p.total_progress_percent}%` }}
                      />
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Project CPM & Task Breakdown */}
        <div className="lg:col-span-2 space-y-6">
          {selectedProject ? (
            <Card className="border-border shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div>
                  <CardTitle className="text-lg">{selectedProject.title}</CardTitle>
                  <p className="text-xs text-muted-foreground mt-0.5">
                    Lead: <span className="font-mono text-primary">{selectedProject.lead_agent_id}</span>
                  </p>
                </div>
                <Button
                  variant="intelligence"
                  onClick={() => handleReplan(selectedProject.project_id)}
                  disabled={replanning}
                >
                  <span className="flex items-center gap-2">
                    <Sparkles className="w-4 h-4" />
                    {replanning ? 'Replanning...' : 'Autonomous Replan'}
                  </span>
                </Button>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Critical Path Header */}
                <div className="p-3 bg-primary/5 border border-primary/20 rounded-lg flex items-center justify-between text-xs">
                  <div>
                    <span className="font-semibold text-primary">CPM Critical Path Duration: </span>
                    <span className="font-bold">{selectedProject.critical_path_duration_days} Days</span>
                  </div>
                  <Badge variant="success">SCHEDULE ON TRACK</Badge>
                </div>

                {/* Milestones */}
                <div>
                  <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                    <Flag className="w-4 h-4 text-primary" />
                    Milestones ({selectedProject.milestones.length})
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {selectedProject.milestones.map((m) => (
                      <div key={m.milestone_id} className="p-2.5 bg-muted/40 border border-border rounded-lg text-xs">
                        <div className="flex justify-between items-center">
                          <span className="font-medium text-foreground">{m.title}</span>
                          <Badge variant={m.status === 'ACHIEVED' ? 'success' : 'outline'}>{m.status}</Badge>
                        </div>
                        <div className="text-muted-foreground mt-1">Due Week: {m.due_week}</div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Tasks List */}
                <div>
                  <h3 className="text-sm font-semibold mb-2 flex items-center gap-2">
                    <Layers className="w-4 h-4 text-primary" />
                    Work Breakdown Structure Tasks ({selectedProject.tasks.length})
                  </h3>
                  <div className="space-y-2">
                    {selectedProject.tasks.map((task) => (
                      <div
                        key={task.task_id}
                        className={`p-3 rounded-lg border text-xs space-y-1.5 ${
                          task.is_critical_path
                            ? 'border-red-500/40 bg-red-500/5'
                            : 'border-border bg-card'
                        }`}
                      >
                        <div className="flex justify-between items-start">
                          <div className="flex items-center gap-2">
                            <span className="font-semibold text-sm text-foreground">{task.title}</span>
                            {task.is_critical_path && (
                              <Badge variant="error">CRITICAL PATH</Badge>
                            )}
                          </div>
                          <Badge variant={task.status === 'COMPLETED' ? 'success' : 'outline'}>{task.status}</Badge>
                        </div>
                        <p className="text-muted-foreground">{task.description}</p>
                        <div className="flex items-center justify-between text-muted-foreground pt-1">
                          <span>
                            Worker: <strong className="text-foreground">{task.assigned_agent_id}</strong>
                          </span>
                          <span>
                            Est: <strong>{task.estimated_days}d</strong> | Progress: <strong>{task.progress_percent}%</strong>
                          </span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a project to inspect critical path dependencies and task breakdown.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
