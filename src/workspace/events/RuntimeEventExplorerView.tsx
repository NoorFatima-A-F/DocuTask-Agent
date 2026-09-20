import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Search } from 'lucide-react';

export const RuntimeEventExplorerView: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedSubsystem, setSelectedSubsystem] = useState<string>('ALL');
  const [selectedSeverity, setSelectedSeverity] = useState<string>('ALL');
  const [selectedEventId, setSelectedEventId] = useState<string | null>(null);

  const allEvents = [
    { id: 'evt-001', time: '14:20:00.120', type: 'MissionCreated', subsystem: 'MISSION_CONTROL', actor: 'Operator', severity: 'INFO', payload: { goal: 'Invoice processing' } },
    { id: 'evt-002', time: '14:20:00.350', type: 'PlannerStarted', subsystem: 'PLANNER', actor: 'ChiefPlanner', severity: 'INFO', payload: { strategy: 'DYNAMIC_DAG' } },
    { id: 'evt-003', time: '14:20:00.890', type: 'PlannerFinished', subsystem: 'PLANNER', actor: 'ChiefPlanner', severity: 'INFO', payload: { task_count: 6 } },
    { id: 'evt-004', time: '14:20:01.100', type: 'TaskAssigned', subsystem: 'WORKER_POOL', actor: 'Scheduler', severity: 'INFO', payload: { task_id: 'task-ocr-1' } },
    { id: 'evt-005', time: '14:20:01.420', type: 'OCRCompleted', subsystem: 'OCR_SERVICE', actor: 'worker-ocr-01', severity: 'INFO', payload: { chars: 4520 } },
    { id: 'evt-006', time: '14:20:01.750', type: 'ValidationPassed', subsystem: 'VALIDATION_ENGINE', actor: 'Validator', severity: 'INFO', payload: { valid: true } },
    { id: 'evt-007', time: '14:20:01.890', type: 'TrustUpdated', subsystem: 'TRUTH_LEDGER', actor: 'TrustEngine', severity: 'INFO', payload: { trust_score: 99.4 } },
    { id: 'evt-008', time: '14:20:02.100', type: 'MissionCompleted', subsystem: 'MISSION_CONTROL', actor: 'Commander', severity: 'INFO', payload: { duration: 1.98 } },
  ];

  const filteredEvents = allEvents.filter(e => {
    if (selectedSubsystem !== 'ALL' && e.subsystem !== selectedSubsystem) return false;
    if (selectedSeverity !== 'ALL' && e.severity !== selectedSeverity) return false;
    if (searchTerm) {
      const matchStr = `${e.id} ${e.type} ${e.subsystem} ${e.actor} ${JSON.stringify(e.payload)}`.toLowerCase();
      if (!matchStr.includes(searchTerm.toLowerCase())) return false;
    }
    return true;
  });

  const selectedEvent = allEvents.find(e => e.id === selectedEventId);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Domain Event Explorer</h1>
            <Badge variant="intelligence" size="sm">Search & Audit</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Search, filter, and inspect immutable domain events across all active micro-engines and partitions.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Showing {filteredEvents.length} / {allEvents.length} Events
          </Badge>
        </div>
      </div>

      {/* Filter Toolbar */}
      <Card className="p-4 border-border/60 space-y-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search by event ID, type, payload, actor..."
              value={searchTerm}
              onChange={e => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-3 py-2 bg-muted/40 rounded-lg border border-border/40 text-xs font-mono text-foreground focus:outline-none focus:border-primary"
            />
          </div>

          <div className="flex items-center gap-2">
            <select
              value={selectedSubsystem}
              onChange={e => setSelectedSubsystem(e.target.value)}
              className="px-3 py-2 bg-muted/40 rounded-lg border border-border/40 text-xs font-mono text-foreground focus:outline-none"
            >
              <option value="ALL">All Subsystems</option>
              <option value="MISSION_CONTROL">MISSION_CONTROL</option>
              <option value="PLANNER">PLANNER</option>
              <option value="WORKER_POOL">WORKER_POOL</option>
              <option value="OCR_SERVICE">OCR_SERVICE</option>
              <option value="VALIDATION_ENGINE">VALIDATION_ENGINE</option>
              <option value="TRUTH_LEDGER">TRUTH_LEDGER</option>
            </select>

            <select
              value={selectedSeverity}
              onChange={e => setSelectedSeverity(e.target.value)}
              className="px-3 py-2 bg-muted/40 rounded-lg border border-border/40 text-xs font-mono text-foreground focus:outline-none"
            >
              <option value="ALL">All Severities</option>
              <option value="INFO">INFO</option>
              <option value="WARNING">WARNING</option>
              <option value="ERROR">ERROR</option>
            </select>
          </div>
        </div>
      </Card>

      {/* Events Table */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-3">
          <div className="border border-border/40 rounded-lg overflow-hidden">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-muted/40 text-muted-foreground border-b border-border/40">
                <tr>
                  <th className="p-2.5 font-medium font-sans">Event ID</th>
                  <th className="p-2.5 font-medium font-sans">Timestamp</th>
                  <th className="p-2.5 font-medium font-sans">Type</th>
                  <th className="p-2.5 font-medium font-sans">Subsystem</th>
                  <th className="p-2.5 font-medium font-sans text-center">Severity</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-border/20">
                {filteredEvents.map(e => (
                  <tr
                    key={e.id}
                    onClick={() => setSelectedEventId(e.id)}
                    className={`cursor-pointer transition-colors ${
                      selectedEventId === e.id ? 'bg-primary/10' : 'hover:bg-muted/20'
                    }`}
                  >
                    <td className="p-2.5 text-foreground font-semibold">{e.id}</td>
                    <td className="p-2.5 text-muted-foreground">{e.time}</td>
                    <td className="p-2.5 text-primary font-bold">{e.type}</td>
                    <td className="p-2.5 text-foreground">{e.subsystem}</td>
                    <td className="p-2.5 text-center font-sans">
                      <Badge variant={e.severity === 'ERROR' ? 'error' : 'success'} size="sm">
                        {e.severity}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Selected Event Payload Box */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold tracking-wider text-muted-foreground uppercase">Payload Details</h2>
          {selectedEvent ? (
            <Card className="p-5 border-border/60 space-y-3 font-mono text-xs">
              <div className="flex justify-between items-center">
                <span className="font-bold text-foreground text-sm">{selectedEvent.type}</span>
                <Badge variant="outline" size="sm">{selectedEvent.id}</Badge>
              </div>
              <div className="text-[11px] text-muted-foreground">
                Actor: {selectedEvent.actor} • Subsystem: {selectedEvent.subsystem}
              </div>
              <pre className="p-3 bg-muted/50 rounded text-[11px] text-foreground overflow-x-auto border border-border/30 max-h-60">
                {JSON.stringify(selectedEvent.payload, null, 2)}
              </pre>
            </Card>
          ) : (
            <Card className="p-8 border-border/40 text-center text-xs text-muted-foreground">
              Select an event from the table to inspect its payload.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
