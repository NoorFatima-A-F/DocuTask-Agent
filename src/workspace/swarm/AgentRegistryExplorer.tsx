import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import {
  Users,
  Search,
  Clock,
  Zap,
  DollarSign,
} from 'lucide-react';

interface AgentItem {
  id: string;
  name: string;
  role: string;
  state: 'AVAILABLE' | 'EXECUTING' | 'NEGOTIATING' | 'VOTING' | 'WAITING' | 'ASSIGNED';
  reputation: number;
  latencyMs: number;
  costPerSec: number;
  capabilities: string[];
  tools: string[];
  tasksCompleted: number;
}

export const AgentRegistryExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedRole, setSelectedRole] = useState<string>('ALL');
  const [selectedAgent, setSelectedAgent] = useState<AgentItem | null>(null);

  const agents: AgentItem[] = [
    {
      id: 'agent-exec-01',
      name: 'Executive Director Alpha',
      role: 'EXECUTIVE',
      state: 'AVAILABLE',
      reputation: 0.992,
      latencyMs: 120,
      costPerSec: 0.08,
      capabilities: ['mission_orchestration', 'goal_alignment', 'strategic_planning'],
      tools: ['mission_decomposer', 'resource_allocator'],
      tasksCompleted: 142,
    },
    {
      id: 'agent-plan-01',
      name: 'Lead DAG Planner',
      role: 'PLANNER',
      state: 'EXECUTING',
      reputation: 0.985,
      latencyMs: 180,
      costPerSec: 0.06,
      capabilities: ['dag_scheduling', 'critical_path_analysis', 'dependency_resolution'],
      tools: ['dag_mutator', 'scheduler_engine'],
      tasksCompleted: 310,
    },
    {
      id: 'agent-coord-01',
      name: 'Swarm Coordinator',
      role: 'COORDINATOR',
      state: 'AVAILABLE',
      reputation: 0.978,
      latencyMs: 150,
      costPerSec: 0.05,
      capabilities: ['task_routing', 'agent_synchronization', 'market_auctioning'],
      tools: ['task_broker', 'auction_manager'],
      tasksCompleted: 480,
    },
    {
      id: 'agent-spec-ocr',
      name: 'Vision & OCR Specialist',
      role: 'SPECIALIST',
      state: 'EXECUTING',
      reputation: 0.988,
      latencyMs: 310,
      costPerSec: 0.04,
      capabilities: ['ocr_extraction', 'table_parsing', 'layout_detection', 'tokenization'],
      tools: ['tesseract_engine', 'vision_transformer'],
      tasksCompleted: 1250,
    },
    {
      id: 'agent-val-sec',
      name: 'Cryptographic Security Validator',
      role: 'VALIDATOR',
      state: 'VOTING',
      reputation: 0.995,
      latencyMs: 90,
      costPerSec: 0.03,
      capabilities: ['security_verification', 'cryptographic_audit', 'schema_validation'],
      tools: ['sha256_verifier', 'policy_evaluator'],
      tasksCompleted: 890,
    },
    {
      id: 'agent-res-opt',
      name: 'Resource & Token Governor',
      role: 'RESOURCE',
      state: 'AVAILABLE',
      reputation: 0.965,
      latencyMs: 80,
      costPerSec: 0.02,
      capabilities: ['budget_management', 'token_quota_control', 'rate_limiting'],
      tools: ['cost_calculator', 'load_balancer'],
      tasksCompleted: 620,
    },
  ];

  const filteredAgents = agents.filter(a => {
    const matchesSearch =
      a.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      a.capabilities.some(c => c.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesRole = selectedRole === 'ALL' || a.role === selectedRole;
    return matchesSearch && matchesRole;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Agent Registry Explorer</h1>
            <Badge variant="intelligence" size="sm">
              {filteredAgents.length} Agents Listed
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Dynamic catalog of autonomous agent profiles, capabilities, permissions, and lifecycle telemetry.
          </p>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="relative flex-1">
          <Search className="w-4 h-4 absolute left-3 top-3 text-muted-foreground" />
          <input
            type="text"
            placeholder="Search by agent name, ID, or semantic capability (e.g. ocr_extraction)..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary"
          />
        </div>
        <select
          value={selectedRole}
          onChange={e => setSelectedRole(e.target.value)}
          className="text-xs px-3 py-2 rounded-md bg-background border border-border/60 focus:outline-none focus:ring-1 focus:ring-primary"
        >
          <option value="ALL">All Roles</option>
          <option value="EXECUTIVE">Executive</option>
          <option value="PLANNER">Planner</option>
          <option value="COORDINATOR">Coordinator</option>
          <option value="SPECIALIST">Specialist</option>
          <option value="VALIDATOR">Validator</option>
          <option value="RESOURCE">Resource</option>
        </select>
      </div>

      {/* Agent Grid & Detail Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Agent List */}
        <div className="lg:col-span-2 space-y-3">
          {filteredAgents.map(a => (
            <Card
              key={a.id}
              onClick={() => setSelectedAgent(a)}
              className={`p-4 cursor-pointer transition-all border ${
                selectedAgent?.id === a.id
                  ? 'border-primary ring-1 ring-primary bg-primary/5'
                  : 'border-border/60 hover:border-border'
              }`}
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="flex items-center gap-2.5">
                  <div className="p-2 rounded-lg bg-muted/40 border border-border/40">
                    <Users className="w-4 h-4 text-primary" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-semibold text-sm">{a.name}</span>
                      <Badge variant="outline" size="sm">{a.role}</Badge>
                    </div>
                    <span className="text-[11px] font-mono text-muted-foreground">{a.id}</span>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <Badge
                    variant={
                      a.state === 'AVAILABLE'
                        ? 'success'
                        : a.state === 'EXECUTING'
                        ? 'info'
                        : a.state === 'VOTING'
                        ? 'warning'
                        : 'default'
                    }
                    size="sm"
                  >
                    {a.state}
                  </Badge>
                  <span className="text-xs font-mono font-bold text-emerald-400">
                    {(a.reputation * 100).toFixed(1)}% Rep
                  </span>
                </div>
              </div>

              {/* Capabilities Chips */}
              <div className="flex flex-wrap gap-1.5 mt-3">
                {a.capabilities.map(cap => (
                  <span
                    key={cap}
                    className="text-[10px] font-mono px-2 py-0.5 rounded bg-muted/30 border border-border/30 text-muted-foreground"
                  >
                    {cap}
                  </span>
                ))}
              </div>
            </Card>
          ))}
        </div>

        {/* Selected Agent Inspector */}
        <div>
          {selectedAgent ? (
            <Card className="p-5 border-border/60 sticky top-4 space-y-4">
              <div className="flex items-center justify-between border-b border-border/40 pb-3">
                <div>
                  <h3 className="font-bold text-sm">{selectedAgent.name}</h3>
                  <span className="text-[11px] font-mono text-muted-foreground">{selectedAgent.id}</span>
                </div>
                <Badge variant="success" size="sm">HEALTHY</Badge>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                  <span className="text-[11px] text-muted-foreground flex items-center gap-1">
                    <Clock className="w-3 h-3 text-blue-400" /> Avg Latency
                  </span>
                  <div className="text-sm font-bold font-mono text-blue-400 mt-1">{selectedAgent.latencyMs} ms</div>
                </div>
                <div className="p-2.5 rounded bg-muted/20 border border-border/30">
                  <span className="text-[11px] text-muted-foreground flex items-center gap-1">
                    <DollarSign className="w-3 h-3 text-emerald-400" /> Compute Cost
                  </span>
                  <div className="text-sm font-bold font-mono text-emerald-400 mt-1">${selectedAgent.costPerSec}/s</div>
                </div>
              </div>

              <div>
                <span className="text-xs font-semibold text-muted-foreground block mb-2">Equipped Tools</span>
                <div className="space-y-1.5">
                  {selectedAgent.tools.map(t => (
                    <div key={t} className="flex items-center gap-2 p-2 rounded bg-muted/10 border border-border/20 text-xs font-mono">
                      <Zap className="w-3 h-3 text-primary" />
                      {t}
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <span className="text-xs font-semibold text-muted-foreground block mb-1">Total Verified Tasks</span>
                <div className="text-lg font-bold font-mono text-primary">{selectedAgent.tasksCompleted} Executions</div>
              </div>

              <Button variant="outline" size="sm" className="w-full">
                Inspect Complete Audit Trace
              </Button>
            </Card>
          ) : (
            <Card className="p-8 border-border/40 text-center text-muted-foreground">
              <Users className="w-8 h-8 mx-auto mb-2 opacity-40" />
              <p className="text-xs">Select an agent profile from the directory to inspect runtime telemetry and tool bindings.</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
