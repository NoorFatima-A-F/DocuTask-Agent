import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const EventGraphView: React.FC = () => {
  const [selectedNodeId, setSelectedNodeId] = useState<string>('node-evt-002');

  const graphNodes = [
    { id: 'node-evt-001', type: 'MissionCreated', category: 'MISSION', connections: 1, latency: '0ms' },
    { id: 'node-evt-002', type: 'PlannerStarted', category: 'PLANNER', connections: 2, latency: '230ms' },
    { id: 'node-evt-003', type: 'PlannerFinished', category: 'PLANNER', connections: 2, latency: '540ms' },
    { id: 'node-evt-004', type: 'TaskAssigned', category: 'WORKER', connections: 1, latency: '210ms' },
    { id: 'node-evt-005', type: 'OCRCompleted', category: 'OCR', connections: 1, latency: '320ms' },
    { id: 'node-evt-006', type: 'ValidationPassed', category: 'VALIDATION', connections: 1, latency: '330ms' },
    { id: 'node-evt-007', type: 'MissionCompleted', category: 'MISSION', connections: 0, latency: '350ms' },
  ];

  const selectedNode = (graphNodes.find(n => n.id === selectedNodeId) || graphNodes[0])!;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Interactive Event Causal Graph</h1>
            <Badge variant="intelligence" size="sm">Topological DAG</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Topological causal dependency network linking events in their true execution order.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            7/7 Causal Edges Acyclic
          </Badge>
        </div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-3">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Causal Event Graph Nodes</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {graphNodes.map(n => (
              <Card
                key={n.id}
                onClick={() => setSelectedNodeId(n.id)}
                className={`p-4 cursor-pointer transition-all border ${
                  selectedNodeId === n.id ? 'border-primary bg-primary/5 shadow-md' : 'border-border/60 hover:border-border'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div>
                    <div className="text-xs font-bold text-foreground">{n.type}</div>
                    <div className="text-[10px] text-muted-foreground font-mono mt-0.5">{n.id}</div>
                  </div>
                  <Badge variant="outline" size="sm">{n.category}</Badge>
                </div>
                <div className="flex items-center justify-between text-[11px] text-muted-foreground mt-3 pt-2 border-t border-border/40 font-mono">
                  <span>Latency: <strong className="text-foreground">{n.latency}</strong></span>
                  <span>Connections: <strong className="text-primary">{n.connections}</strong></span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Node Details */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Node Causal Inspector</h2>
          <Card className="p-5 border-border/60 space-y-4">
            <div>
              <Badge variant="intelligence" size="sm">{selectedNode.category}</Badge>
              <div className="text-base font-bold text-foreground mt-2">{selectedNode.type}</div>
              <div className="text-xs font-mono text-muted-foreground">{selectedNode.id}</div>
            </div>

            <div className="space-y-2 pt-2 border-t border-border/40 text-xs">
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Execution Latency:</span>
                <span className="font-mono font-bold text-foreground">{selectedNode.latency}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-muted-foreground">Downstream Dependencies:</span>
                <span className="font-mono font-bold text-primary">{selectedNode.connections} child events</span>
              </div>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};
