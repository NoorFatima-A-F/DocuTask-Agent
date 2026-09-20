import React, { useState } from 'react';
import { Badge } from '../../components/ui/Badge';
import { Card } from '../../components/ui/Card';
import { Database, Search, CheckCircle2, AlertTriangle, ArrowUpRight, Hash, Layers } from 'lucide-react';

interface EvidenceItem {
  id: string;
  sourceEventId: string;
  eventType: string;
  dimension: string;
  featureKey: string;
  observedValue: number;
  expectedRange: string;
  statisticalWeight: number;
  provenanceHash: string;
  status: 'VALID' | 'ANOMALOUS' | 'DEGRADED';
  timestamp: string;
}

const mockEvidences: EvidenceItem[] = [
  {
    id: 'ev-901',
    sourceEventId: 'evt_dag_exec_8832',
    eventType: 'worker.step.completed',
    dimension: 'ocr_quality',
    featureKey: 'character_recognition_rate',
    observedValue: 0.994,
    expectedRange: '[0.950, 1.000]',
    statisticalWeight: 0.18,
    provenanceHash: 'sha256:7f9a12c8e3...',
    status: 'VALID',
    timestamp: '2026-09-11T22:45:10Z',
  },
  {
    id: 'ev-902',
    sourceEventId: 'evt_dag_exec_8833',
    eventType: 'worker.schema.validated',
    dimension: 'schema_extraction',
    featureKey: 'field_match_f1',
    observedValue: 0.982,
    expectedRange: '[0.900, 1.000]',
    statisticalWeight: 0.22,
    provenanceHash: 'sha256:4b219cf10a...',
    status: 'VALID',
    timestamp: '2026-09-11T22:45:12Z',
  },
  {
    id: 'ev-903',
    sourceEventId: 'evt_dag_exec_8834',
    eventType: 'truth_ledger.invariant.checked',
    dimension: 'invariant_validation',
    featureKey: 'invariant_violation_count',
    observedValue: 0.0,
    expectedRange: '[0.000, 0.000]',
    statisticalWeight: 0.25,
    provenanceHash: 'sha256:88e09f21ab...',
    status: 'VALID',
    timestamp: '2026-09-11T22:45:15Z',
  },
  {
    id: 'ev-904',
    sourceEventId: 'evt_resilience_probe_102',
    eventType: 'resilience.circuit_breaker.heartbeat',
    dimension: 'worker_reliability',
    featureKey: 'consecutive_error_rate',
    observedValue: 0.012,
    expectedRange: '[0.000, 0.050]',
    statisticalWeight: 0.15,
    provenanceHash: 'sha256:12cba89721...',
    status: 'VALID',
    timestamp: '2026-09-11T22:45:18Z',
  },
  {
    id: 'ev-905',
    sourceEventId: 'evt_planner_mutation_441',
    eventType: 'planner.dag.repartitioned',
    dimension: 'planner_efficiency',
    featureKey: 'dag_schedule_slack_ratio',
    observedValue: 0.068,
    expectedRange: '[0.000, 0.100]',
    statisticalWeight: 0.20,
    provenanceHash: 'sha256:bb18290fa4...',
    status: 'VALID',
    timestamp: '2026-09-11T22:45:22Z',
  },
];

export const RuntimeEvidenceExplorer: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedDimension, setSelectedDimension] = useState<string>('ALL');

  const filtered = mockEvidences.filter((item) => {
    const matchesSearch =
      item.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.sourceEventId.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.featureKey.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.eventType.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesDim = selectedDimension === 'ALL' || item.dimension === selectedDimension;
    return matchesSearch && matchesDim;
  });

  return (
    <div className="p-6 space-y-6 bg-[#0B1120] min-h-screen text-[#F8FAFC]">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-4 border-b border-[#1E293B] pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-br from-emerald-500/20 to-teal-500/20 border border-emerald-500/30 rounded-xl text-emerald-400">
              <Database className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-xl font-bold font-mono tracking-tight text-white flex items-center gap-2">
                Runtime Evidence Explorer
                <Badge variant="success" size="sm">Immutable Ledger</Badge>
              </h1>
              <p className="text-xs text-slate-400">
                Direct projection of domain events into verified statistical features backing confidence scores.
              </p>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="intelligence" size="sm">5 Total Samples</Badge>
          <Badge variant="outline" size="sm">0 Anomalies</Badge>
        </div>
      </div>

      {/* Filter bar */}
      <div className="flex flex-wrap items-center gap-4 bg-[#0F172A] p-4 rounded-xl border border-[#1E293B]">
        <div className="relative flex-1 min-w-[240px]">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Search by Evidence ID, Event ID, Feature..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-[#0B1120] border border-[#1E293B] rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>

        <select
          value={selectedDimension}
          onChange={(e) => setSelectedDimension(e.target.value)}
          className="bg-[#0B1120] border border-[#1E293B] rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-emerald-500"
        >
          <option value="ALL">All Dimensions</option>
          <option value="ocr_quality">OCR Quality</option>
          <option value="schema_extraction">Schema Extraction</option>
          <option value="invariant_validation">Invariant Validation</option>
          <option value="worker_reliability">Worker Reliability</option>
          <option value="planner_efficiency">Planner Efficiency</option>
        </select>
      </div>

      {/* Table */}
      <Card className="bg-[#0F172A] border-[#1E293B] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs font-mono">
            <thead className="bg-[#1E293B]/60 text-slate-400 border-b border-[#1E293B]">
              <tr>
                <th className="p-3">Evidence ID / Timestamp</th>
                <th className="p-3">Source Event</th>
                <th className="p-3">Dimension & Feature</th>
                <th className="p-3">Observed / Range</th>
                <th className="p-3">Weight</th>
                <th className="p-3">Provenance Hash</th>
                <th className="p-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[#1E293B]/40">
              {filtered.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="p-3">
                    <div className="font-semibold text-emerald-400 flex items-center gap-1">
                      <Hash className="w-3.5 h-3.5" />
                      {item.id}
                    </div>
                    <div className="text-[10px] text-slate-500">{item.timestamp}</div>
                  </td>
                  <td className="p-3">
                    <div className="text-slate-200">{item.eventType}</div>
                    <div className="text-[10px] text-slate-500 flex items-center gap-1">
                      <Layers className="w-3 h-3" />
                      {item.sourceEventId}
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="text-slate-300 capitalize">{item.dimension.replace('_', ' ')}</div>
                    <div className="text-[10px] text-slate-400">{item.featureKey}</div>
                  </td>
                  <td className="p-3">
                    <div className="text-slate-200 font-bold">{(item.observedValue * 100).toFixed(1)}%</div>
                    <div className="text-[10px] text-slate-500">{item.expectedRange}</div>
                  </td>
                  <td className="p-3 text-slate-300">
                    {item.statisticalWeight.toFixed(2)}
                  </td>
                  <td className="p-3 text-[10px] text-slate-400">
                    <span className="bg-slate-900/80 px-1.5 py-0.5 rounded border border-slate-700">
                      {item.provenanceHash}
                    </span>
                  </td>
                  <td className="p-3">
                    {item.status === 'VALID' ? (
                      <Badge variant="success" size="sm" className="flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        Valid
                      </Badge>
                    ) : (
                      <Badge variant="warning" size="sm" className="flex items-center gap-1">
                        <AlertTriangle className="w-3 h-3" />
                        {item.status}
                      </Badge>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>

      {/* Footer Info */}
      <div className="flex items-center justify-between text-xs text-slate-500 border-t border-[#1E293B] pt-4">
        <span>Verified against Truth Ledger invariant rule `#INV-CONF-001`</span>
        <a href="#audit" className="text-emerald-400 hover:underline flex items-center gap-1">
          Export Evidence Provenance Chain <ArrowUpRight className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
};
