import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Users,
  UserPlus,
  RotateCw,
  Sparkles,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { AgentEmployee, AgentRoleType } from '../../types/organizationPlatform';

export const WorkforceManagementCenter: React.FC = () => {
  const [agents, setAgents] = useState<AgentEmployee[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [rebalancing, setRebalancing] = useState<boolean>(false);
  const [hiring, setHiring] = useState<boolean>(false);
  const [newName, setNewName] = useState<string>('');
  const [newRole, setNewRole] = useState<AgentRoleType>('ENGINEERING_AGENT');

  const loadAgents = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getAgents();
      setAgents(data);
    } catch (err) {
      console.error('Failed to load agents:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAgents();
  }, []);

  const handleRebalance = async () => {
    try {
      setRebalancing(true);
      await organizationPlatformApiClient.optimizeWorkforce();
      await loadAgents();
    } catch (err) {
      console.error('Error rebalancing workforce:', err);
    } finally {
      setRebalancing(false);
    }
  };

  const handleHire = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;
    try {
      setHiring(true);
      await organizationPlatformApiClient.hireAgent(newName, newRole, 'dept_engineering_core', ['pipeline_execution']);
      setNewName('');
      await loadAgents();
    } catch (err) {
      console.error('Error hiring agent:', err);
    } finally {
      setHiring(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Users className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Autonomous Workforce Manager</h1>
            <p className="text-sm text-muted-foreground">
              Agent Employee Registry, Skill Matrix Profiles, Dynamic Workload Balancing & Capability Upgrades
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadAgents} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleRebalance} disabled={rebalancing}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {rebalancing ? 'Rebalancing...' : 'Rebalance Workloads'}
            </span>
          </Button>
        </div>
      </div>

      {/* Provision New Agent Worker Form */}
      <Card className="border-border shadow-sm">
        <CardHeader>
          <CardTitle className="text-base flex items-center gap-2">
            <UserPlus className="w-4 h-4 text-primary" />
            Provision Specialized Agent Worker
          </CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleHire} className="flex flex-col md:flex-row gap-4">
            <input
              type="text"
              value={newName}
              onChange={(e) => setNewName(e.target.value)}
              placeholder="e.g. Smart OCR Normalization Specialist"
              className="flex-1 px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary"
            />
            <select
              value={newRole}
              onChange={(e) => setNewRole(e.target.value as AgentRoleType)}
              className="px-3.5 py-2 text-sm rounded-md border border-input bg-background focus:outline-none focus:ring-1 focus:ring-primary"
            >
              <option value="RESEARCH_AGENT">RESEARCH_AGENT</option>
              <option value="ENGINEERING_AGENT">ENGINEERING_AGENT</option>
              <option value="ANALYST_AGENT">ANALYST_AGENT</option>
              <option value="SECURITY_AGENT">SECURITY_AGENT</option>
              <option value="OPERATIONS_AGENT">OPERATIONS_AGENT</option>
            </select>
            <Button type="submit" variant="primary" disabled={hiring || !newName.trim()}>
              <span className="flex items-center gap-2">
                <UserPlus className="w-4 h-4" />
                {hiring ? 'Provisioning...' : 'Provision Agent'}
              </span>
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Agent Employees Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent) => (
          <Card key={agent.agent_id} className="border-border shadow-sm hover:border-primary/50 transition-colors">
            <CardHeader className="pb-2">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-base">{agent.name}</CardTitle>
                  <span className="text-xs text-muted-foreground font-mono">{agent.agent_id}</span>
                </div>
                <Badge variant={agent.status === 'ACTIVE' ? 'success' : agent.status === 'BUSY' ? 'warning' : 'outline'}>
                  {agent.status}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <Badge variant="intelligence">{agent.role}</Badge>
                <span className="text-muted-foreground">Level {agent.learning_level} Specialist</span>
              </div>

              {/* Workload Progress */}
              <div className="space-y-1">
                <div className="flex justify-between text-xs">
                  <span className="text-muted-foreground">Workload:</span>
                  <span className="font-semibold">{agent.current_workload_percent}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-1.5 overflow-hidden">
                  <div
                    className={`h-full rounded-full ${
                      agent.current_workload_percent > 80
                        ? 'bg-red-500'
                        : agent.current_workload_percent > 50
                        ? 'bg-amber-500'
                        : 'bg-emerald-500'
                    }`}
                    style={{ width: `${Math.min(100, agent.current_workload_percent)}%` }}
                  />
                </div>
              </div>

              {/* Skills */}
              <div className="space-y-1">
                <div className="text-xs font-semibold text-muted-foreground">Verified Skills:</div>
                <div className="flex flex-wrap gap-1">
                  {agent.skills.map((s) => (
                    <span
                      key={s.skill_name}
                      className="px-2 py-0.5 rounded bg-muted/60 text-[11px] font-mono border border-border"
                    >
                      {s.skill_name} ({(s.proficiency_level * 100).toFixed(0)}%)
                    </span>
                  ))}
                </div>
              </div>

              {/* Productivity & Cost Footer */}
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-border/60 text-xs">
                <div>
                  <span className="text-muted-foreground">Productivity:</span>
                  <span className="font-semibold text-emerald-500 ml-1">
                    {(agent.productivity_score * 100).toFixed(0)}%
                  </span>
                </div>
                <div>
                  <span className="text-muted-foreground">Rate:</span>
                  <span className="font-semibold ml-1">${agent.hourly_cost_usd}/hr</span>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
};
