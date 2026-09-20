import React, { useState } from 'react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';
import {
  Globe,
  Search,
  History,
  Lock,
  Clock,
} from 'lucide-react';

interface WorldEntityItem {
  id: string;
  type: string;
  name: string;
  healthScore: number;
  status: string;
  attributes: Record<string, any>;
  updatedAt: string;
}

interface StateSnapshotItem {
  id: string;
  sequence: number;
  hash: string;
  timestamp: string;
  entitiesCount: number;
}

export const WorldModelExplorer: React.FC = () => {
  const [selectedType, setSelectedType] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState<string>('');

  const entities: WorldEntityItem[] = [
    {
      id: 'agent-planner-01',
      type: 'AGENT',
      name: 'APDLE Live DAG Planner',
      healthScore: 0.99,
      status: 'OPTIMAL',
      attributes: { role: 'PLANNER', throughput_qps: 45, concurrency: 8 },
      updatedAt: '2026-09-12 10:15:00 UTC',
    },
    {
      id: 'agent-ocr-specialist-01',
      type: 'AGENT',
      name: 'Parallel Table Extraction Specialist',
      healthScore: 0.98,
      status: 'OPTIMAL',
      attributes: { role: 'SPECIALIST', batch_size: 16, accuracy: 0.995 },
      updatedAt: '2026-09-12 10:15:30 UTC',
    },
    {
      id: 'res-gpu-vram-01',
      type: 'RESOURCE',
      name: 'Host VRAM Allocation Pool',
      healthScore: 0.97,
      status: 'OPTIMAL',
      attributes: { total_vram_gb: 24, allocated_vram_gb: 11.6, free_vram_gb: 12.4 },
      updatedAt: '2026-09-12 10:16:00 UTC',
    },
    {
      id: 'infra-eventbus-01',
      type: 'INFRASTRUCTURE',
      name: 'Multicast EventBus Router',
      healthScore: 1.0,
      status: 'OPTIMAL',
      attributes: { events_per_sec: 12500, buffer_capacity_mb: 512, dropped_frames: 0 },
      updatedAt: '2026-09-12 10:16:15 UTC',
    },
    {
      id: 'pol-concurrency-quota-01',
      type: 'POLICY',
      name: 'Dynamic Concurrency Quota Policy',
      healthScore: 1.0,
      status: 'ACTIVE',
      attributes: { max_tasks_per_dag: 16, memory_threshold_pct: 60.0 },
      updatedAt: '2026-09-12 10:16:30 UTC',
    },
  ];

  const snapshots: StateSnapshotItem[] = [
    { id: 'wss-000003', sequence: 3, hash: '0x9e8a7b6c5d...110a', timestamp: '2026-09-12 10:15:00 UTC', entitiesCount: 18 },
    { id: 'wss-000002', sequence: 2, hash: '0x3c4d5e6f7a...882b', timestamp: '2026-09-12 09:45:00 UTC', entitiesCount: 16 },
    { id: 'wss-000001', sequence: 1, hash: '0x7a8b9c0d1e...554c', timestamp: '2026-09-12 09:15:00 UTC', entitiesCount: 14 },
  ];

  const filteredEntities = entities.filter((e) => {
    const matchesType = selectedType === 'ALL' || e.type === selectedType;
    const matchesSearch =
      e.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      e.id.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesType && matchesSearch;
  });

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">World Model Explorer</h1>
            <Badge variant="intelligence" size="sm" hasDot isPulsing>
              GROUND TRUTH STATE
            </Badge>
            <Badge variant="outline" size="sm">
              AWM-PSDTIP Phase 13.10
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Complete enterprise state model across agents, tasks, resources, infrastructure, policies, capabilities, and historical time-travel reconstruction.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <History className="w-3.5 h-3.5 mr-1.5" />
            Time-Travel Query
          </Button>
          <Button variant="intelligence" size="sm">
            <Globe className="w-3.5 h-3.5 mr-1.5" />
            Create State Snapshot
          </Button>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-2 overflow-x-auto pb-1 sm:pb-0">
          {(['ALL', 'AGENT', 'RESOURCE', 'INFRASTRUCTURE', 'POLICY'] as const).map((t) => (
            <Button
              key={t}
              variant={selectedType === t ? 'primary' : 'ghost'}
              size="sm"
              onClick={() => setSelectedType(t)}
            >
              {t}
            </Button>
          ))}
        </div>
        <div className="relative w-full sm:w-64">
          <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-muted-foreground" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search entity or ID..."
            className="w-full bg-secondary/50 text-xs rounded-md pl-8 pr-2 py-1.5 border border-border/40 focus:outline-none focus:border-primary"
          />
        </div>
      </div>

      {/* Main Grid: Entities & Snapshots */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Entities List */}
        <div className="lg:col-span-8 space-y-4">
          {filteredEntities.map((ent) => (
            <Card key={ent.id} className="p-5 border-border/40 space-y-3 hover:border-purple-500/30 transition-colors">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-bold text-foreground">{ent.id}</span>
                    <Badge variant="intelligence" size="sm">{ent.type}</Badge>
                    <Badge variant="success" size="sm">{ent.status}</Badge>
                  </div>
                  <h3 className="text-sm font-semibold text-foreground">{ent.name}</h3>
                </div>
                <span className="text-xs font-mono text-emerald-400 font-bold">
                  Health: {(ent.healthScore * 100).toFixed(1)}%
                </span>
              </div>

              {/* Attributes Matrix */}
              <div className="p-3 rounded bg-secondary/20 border border-border/30 text-xs font-mono text-muted-foreground grid grid-cols-1 sm:grid-cols-3 gap-2">
                {Object.entries(ent.attributes).map(([k, v], idx) => (
                  <div key={idx} className="truncate">
                    <span className="text-foreground">{k}:</span> {String(v)}
                  </div>
                ))}
              </div>

              <div className="flex items-center justify-between text-[11px] text-muted-foreground pt-2 border-t border-border/30 font-mono">
                <span>Updated: {ent.updatedAt}</span>
                <span className="text-purple-400">● Ground-Truth Synchronized</span>
              </div>
            </Card>
          ))}
        </div>

        {/* Snapshot History */}
        <div className="lg:col-span-4 space-y-3">
          <h2 className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
            State Snapshots &amp; Hash Tree
          </h2>
          {snapshots.map((s) => (
            <Card key={s.id} className="p-3.5 border-border/40 bg-secondary/10 space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono font-bold text-foreground">Seq #{s.sequence} ({s.id})</span>
                <Badge variant="outline" size="sm">{s.entitiesCount} Entities</Badge>
              </div>
              <div className="flex items-center gap-1.5 text-[11px] font-mono text-purple-300">
                <Lock className="w-3 h-3 text-purple-400 flex-shrink-0" />
                <span className="truncate">{s.hash}</span>
              </div>
              <div className="text-[10px] text-muted-foreground font-mono flex items-center gap-1">
                <Clock className="w-3 h-3" />
                <span>{s.timestamp}</span>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </div>
  );
};
