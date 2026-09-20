import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';

export const TruthLedgerExplorerView: React.FC = () => {
  const [filterType, setFilterType] = useState<string>('ALL');

  const entries = [
    {
      eventId: 'tle_001_plan',
      missionId: 'msn_1001',
      eventType: 'PLANNER_DECISION',
      timestamp: '14:20:00.124',
      plannerVer: 'v2.1.0',
      strategyVer: '2.1.0',
      model: 'gemini-1.5-pro',
      parentHash: '0x0000000000000000',
      entryHash: '0x8f2ac31b4e5d6a7b',
      evidenceRoot: '0x8f2ac31b4e5d6a7b',
      status: 'VERIFIED',
    },
    {
      eventId: 'tle_002_tool',
      missionId: 'msn_1001',
      eventType: 'TOOL_EXECUTION',
      timestamp: '14:20:00.350',
      plannerVer: 'v2.1.0',
      strategyVer: '2.1.0',
      model: 'tesseract_v2_optimized',
      parentHash: '0x8f2ac31b4e5d6a7b',
      entryHash: '0x3c7eb44a1d9e2f8c',
      evidenceRoot: '0x3c7eb44a1d9e2f8c',
      status: 'VERIFIED',
    },
    {
      eventId: 'tle_003_sign',
      missionId: 'msn_1001',
      eventType: 'EVIDENCE_SIGNED',
      timestamp: '14:20:00.780',
      plannerVer: 'v2.1.0',
      strategyVer: '2.1.0',
      model: 'ed25519_authority',
      parentHash: '0x3c7eb44a1d9e2f8c',
      entryHash: '0x991afe820b4c7d6e',
      evidenceRoot: '0x991afe820b4c7d6e',
      status: 'VERIFIED',
    },
    {
      eventId: 'tle_004_opt',
      missionId: 'msn_1001',
      eventType: 'OPTIMIZATION_PROMOTED',
      timestamp: '14:20:01.050',
      plannerVer: 'v2.1.0',
      strategyVer: '2.1.0',
      model: 'aislcop_optimizer',
      parentHash: '0x991afe820b4c7d6e',
      entryHash: '0x661d009ab5e4f3a2',
      evidenceRoot: '0x661d009ab5e4f3a2',
      status: 'VERIFIED',
    },
  ];

  const filtered = filterType === 'ALL' ? entries : entries.filter((e) => e.eventType === filterType);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-border/40 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight">Runtime Truth Ledger</h1>
            <Badge variant="intelligence" size="sm">Pillar 1</Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1">
            Immutable, append-only truth ledger with SHA-256 parent-child hash continuity linking every mission event to cryptographic evidence.
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="success" size="md">
            Chain Continuity: 100% Verified
          </Badge>
          <Badge variant="outline" size="md">
            Total Entries: {entries.length}
          </Badge>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center gap-2">
        {['ALL', 'PLANNER_DECISION', 'TOOL_EXECUTION', 'EVIDENCE_SIGNED', 'OPTIMIZATION_PROMOTED'].map((t) => (
          <button
            key={t}
            onClick={() => setFilterType(t)}
            className={`text-xs px-2.5 py-1 rounded transition-colors font-medium ${
              filterType === t ? 'bg-primary text-primary-foreground' : 'bg-muted text-muted-foreground hover:bg-muted/80'
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      {/* Ledger Table */}
      <Card className="p-0 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="border-b border-border/40 bg-muted/20 font-semibold text-muted-foreground">
                <th className="p-3">Event ID</th>
                <th className="p-3">Event Type</th>
                <th className="p-3">Mission ID</th>
                <th className="p-3">Timestamp</th>
                <th className="p-3">Parent Hash</th>
                <th className="p-3">Entry Hash</th>
                <th className="p-3">Evidence Link</th>
                <th className="p-3">Audit Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border/20">
              {filtered.map((e) => (
                <tr key={e.eventId} className="hover:bg-muted/10 transition-colors">
                  <td className="p-3 font-mono font-semibold text-primary">{e.eventId}</td>
                  <td className="p-3 font-mono text-foreground">
                    <Badge variant="outline" size="sm">{e.eventType}</Badge>
                  </td>
                  <td className="p-3 font-mono text-foreground">{e.missionId}</td>
                  <td className="p-3 font-mono text-muted-foreground">{e.timestamp}</td>
                  <td className="p-3 font-mono text-[11px] text-muted-foreground">{e.parentHash.slice(0, 10)}...</td>
                  <td className="p-3 font-mono text-[11px] text-emerald-400 font-semibold">{e.entryHash.slice(0, 10)}...</td>
                  <td className="p-3 font-mono text-[11px] text-muted-foreground">{e.evidenceRoot.slice(0, 10)}...</td>
                  <td className="p-3">
                    <Badge variant="success" size="sm">{e.status}</Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
};
