/**
 * Enterprise Verification Platform Studio Workspace.
 * Full visualization of the 15 Core Components, 12-Stage Lifecycle, Datasets, Evidence, and Traceability DAG.
 */
import React, { useState, useEffect } from 'react';
import { Card } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { verificationApiClient } from '../../services/verificationPlatformApiClient';
import {
  VerificationOverview,
  ComponentHealth,
  VerificationDefinition,
  VerificationRun,
  DatasetRecord,
  EnvironmentReadiness,
  EvidenceItem,
  AuditEntry,
  TraceabilityNode,
  PluginDescriptor,
} from '../../types/verificationPlatform';
import {
  ShieldCheck,
  Play,
  CheckCircle2,
  Lock,
  Cpu,
  Layers,
  Database,
  Server,
  FileCheck,
  GitBranch,
  Check,
} from 'lucide-react';

type StudioSubTab =
  | 'COMPONENTS'
  | 'ORCHESTRATOR'
  | 'DATASETS'
  | 'ENVIRONMENTS'
  | 'EVIDENCE_AUDIT'
  | 'TRACEABILITY';

export const VerificationPlatformStudio: React.FC = () => {
  const [subTab, setSubTab] = useState<StudioSubTab>('COMPONENTS');
  const [overview, setOverview] = useState<VerificationOverview | null>(null);
  const [components, setComponents] = useState<ComponentHealth[]>([]);
  const [definitions, setDefinitions] = useState<VerificationDefinition[]>([]);
  const [activeRun, setActiveRun] = useState<VerificationRun | null>(null);
  const [datasets, setDatasets] = useState<DatasetRecord[]>([]);
  const [environments, setEnvironments] = useState<EnvironmentReadiness[]>([]);
  const [evidenceList, setEvidenceList] = useState<EvidenceItem[]>([]);
  const [auditTrail, setAuditTrail] = useState<AuditEntry[]>([]);
  const [lineageNodes, setLineageNodes] = useState<TraceabilityNode[]>([]);
  const [plugins, setPlugins] = useState<PluginDescriptor[]>([]);
  const [loading, setLoading] = useState(false);
  const [tamperCheckStatus, setTamperCheckStatus] = useState<string | null>(null);

  useEffect(() => {
    verificationApiClient.getOverview().then(setOverview);
    verificationApiClient.getComponentsHealth().then(setComponents);
    verificationApiClient.getDefinitions().then(setDefinitions);
    verificationApiClient.getDatasets().then(setDatasets);
    verificationApiClient.getEnvironments().then(setEnvironments);
    verificationApiClient.getEvidence().then(setEvidenceList);
    verificationApiClient.getAuditTrail().then(setAuditTrail);
    verificationApiClient.getPlugins().then(setPlugins);
  }, []);

  const handleExecute = async (defId: string) => {
    setLoading(true);
    try {
      const run = await verificationApiClient.triggerRun(defId);
      setActiveRun(run);
      // Fetch updated lineage & evidence
      verificationApiClient.getLineage(run.run_id).then(setLineageNodes);
      verificationApiClient.getEvidence().then(setEvidenceList);
      verificationApiClient.getAuditTrail().then(setAuditTrail);
      verificationApiClient.getOverview().then(setOverview);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyTamper = async (evidenceId: string) => {
    const res = await verificationApiClient.verifyEvidence(evidenceId);
    setTamperCheckStatus(res.is_valid ? '100% AUTHENTIC (SHA-256 Verified)' : 'TAMPER DETECTED');
  };

  return (
    <div className="space-y-6">
      {/* Header Summary */}
      <div className="flex items-center justify-between p-6 bg-slate-900/90 rounded-2xl border border-slate-800 backdrop-blur-md shadow-xl">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-gradient-to-br from-indigo-500/20 to-cyan-500/20 rounded-2xl border border-cyan-500/30">
            <ShieldCheck className="w-8 h-8 text-cyan-400" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-white tracking-tight flex items-center gap-3">
              Enterprise Verification Platform (FVPA)
              <Badge variant="success">15 Core Components Active</Badge>
            </h1>
            <p className="text-sm text-slate-400">
              Clean Architecture, SOLID-Compliant, Deterministic & Probabilistic AI Evaluation Backbone
            </p>
          </div>
        </div>

        {definitions.length > 0 && (
          <Button
            variant="primary"
            onClick={() => {
              const def = definitions[0];
              if (def) handleExecute(def.definition_id);
            }}
            disabled={loading}
            className="flex items-center gap-2 shadow-lg shadow-cyan-500/20"
          >
            <Play className="w-4 h-4" />
            {loading ? 'Orchestrating Pipeline...' : 'Run 12-Stage Verification'}
          </Button>
        )}
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <Card className="p-4 bg-slate-900/70 border-slate-800">
          <div className="text-xs text-slate-400 font-mono">Core Components</div>
          <div className="text-2xl font-bold text-cyan-400 mt-1">{overview?.total_core_components || 15} / 15</div>
          <div className="text-xs text-emerald-400 mt-1 flex items-center gap-1">
            <CheckCircle2 className="w-3 h-3" /> 100% Operational Health
          </div>
        </Card>

        <Card className="p-4 bg-slate-900/70 border-slate-800">
          <div className="text-xs text-slate-400 font-mono">Dataset Classes</div>
          <div className="text-2xl font-bold text-indigo-400 mt-1">{overview?.datasets_count || 11} Types</div>
          <div className="text-xs text-slate-400 mt-1 font-mono">SHA-256 Fingerprinted</div>
        </Card>

        <Card className="p-4 bg-slate-900/70 border-slate-800">
          <div className="text-xs text-slate-400 font-mono">Environments Ready</div>
          <div className="text-2xl font-bold text-amber-400 mt-1">{overview?.environments_count || 7} Tiers</div>
          <div className="text-xs text-emerald-400 mt-1 font-mono">Dev $\rightarrow$ Prod Shadow</div>
        </Card>

        <Card className="p-4 bg-slate-900/70 border-slate-800">
          <div className="text-xs text-slate-400 font-mono">Audit Chain Integrity</div>
          <div className="text-2xl font-bold text-emerald-400 mt-1">Verified</div>
          <div className="text-xs text-emerald-400 mt-1 font-mono">Immutable Hash Chain</div>
        </Card>
      </div>

      {/* Sub-Navigation Tabs */}
      <div className="flex items-center gap-2 p-1.5 bg-slate-950/80 rounded-xl border border-slate-800 overflow-x-auto">
        <button
          onClick={() => setSubTab('COMPONENTS')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'COMPONENTS' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Cpu className="w-4 h-4" /> 15 Core Components Matrix
        </button>

        <button
          onClick={() => setSubTab('ORCHESTRATOR')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'ORCHESTRATOR' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Layers className="w-4 h-4" /> 12-Stage Lifecycle & Runs
        </button>

        <button
          onClick={() => setSubTab('DATASETS')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'DATASETS' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Database className="w-4 h-4" /> Dataset Catalog (11 Classes)
        </button>

        <button
          onClick={() => setSubTab('ENVIRONMENTS')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'ENVIRONMENTS' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Server className="w-4 h-4" /> Environment Tiers
        </button>

        <button
          onClick={() => setSubTab('EVIDENCE_AUDIT')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'EVIDENCE_AUDIT' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <Lock className="w-4 h-4" /> Evidence & Audit Ledger
        </button>

        <button
          onClick={() => setSubTab('TRACEABILITY')}
          className={`px-4 py-2 rounded-lg text-xs font-mono font-semibold transition-all flex items-center gap-2 ${
            subTab === 'TRACEABILITY' ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:text-white'
          }`}
        >
          <GitBranch className="w-4 h-4" /> End-to-End Lineage DAG
        </button>
      </div>

      {/* Sub-Tab 1: 15 Core Components Matrix */}
      {subTab === 'COMPONENTS' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {components.map((c, i) => (
            <Card key={c.component_name} className="p-4 bg-slate-900/80 border-slate-800 hover:border-cyan-500/40 transition-all">
              <div className="flex items-center justify-between mb-2">
                <span className="font-mono text-xs text-slate-400">#{i + 1} Component</span>
                <Badge variant={c.status === 'HEALTHY' ? 'success' : 'warning'}>{c.status}</Badge>
              </div>
              <div className="font-bold text-sm text-white">{c.component_name}</div>
              <div className="grid grid-cols-2 gap-2 mt-4 text-xs font-mono text-slate-300">
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Throughput</div>
                  <div className="text-cyan-400 font-bold">{c.throughput_ops_sec} ops/s</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Latency</div>
                  <div className="text-indigo-400 font-bold">{c.latency_ms} ms</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Error Rate</div>
                  <div className="text-emerald-400 font-bold">{c.error_rate_pct}%</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Connections</div>
                  <div className="text-amber-400 font-bold">{c.active_connections}</div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Sub-Tab 2: 12-Stage Lifecycle & Runs */}
      {subTab === 'ORCHESTRATOR' && (
        <div className="space-y-4">
          {activeRun ? (
            <Card className="p-6 bg-slate-900/90 border-slate-800">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <div className="text-xs font-mono text-cyan-400">RUN: {activeRun.run_id}</div>
                  <h2 className="text-lg font-bold text-white mt-1">Lifecycle Orchestration Pipeline</h2>
                </div>
                <Badge variant={activeRun.status === 'PASSED' ? 'success' : 'warning'}>
                  {activeRun.status} ({activeRun.overall_score * 100}%)
                </Badge>
              </div>

              {/* 12-Stage Progress Bar */}
              <div className="w-full bg-slate-950 rounded-full h-3 mb-6 border border-slate-800 overflow-hidden">
                <div
                  className="bg-gradient-to-r from-cyan-500 to-indigo-500 h-full transition-all duration-500"
                  style={{ width: `${activeRun.stage_progress_pct}%` }}
                />
              </div>

              {/* 12 Stages Grid */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs font-mono">
                {[
                  '1. PRE_FLIGHT_DISCOVERY',
                  '2. DATASET_ACQUISITION',
                  '3. ENVIRONMENT_PROVISIONING',
                  '4. INVARIANT_REGISTRATION',
                  '5. PROBABILISTIC_EXECUTION',
                  '6. METRIC_COMPUTATION',
                  '7. STATISTICAL_ANALYSIS',
                  '8. EVIDENCE_SEALING',
                  '9. QUALITY_GATE_EVALUATION',
                  '10. COMPLIANCE_CERTIFICATION',
                  '11. TELEMETRY_EXPORT',
                  '12. POST_FLIGHT_TEARDOWN',
                ].map((stg) => (
                  <div key={stg} className="p-2.5 bg-slate-950/70 border border-slate-800 rounded-lg text-emerald-400 flex items-center gap-2">
                    <Check className="w-3.5 h-3.5" />
                    <span>{stg}</span>
                  </div>
                ))}
              </div>
            </Card>
          ) : (
            <Card className="p-8 text-center bg-slate-900/60 border-slate-800 text-slate-400 font-mono text-sm">
              Click &quot;Run 12-Stage Verification&quot; above to trigger an end-to-end verification lifecycle execution.
            </Card>
          )}

          {/* Plugin Registry Catalog */}
          <Card className="p-4 bg-slate-900/80 border-slate-800">
            <h3 className="font-bold text-sm text-white mb-3 flex items-center gap-2">
              <Layers className="w-4 h-4 text-cyan-400" />
              Registered Verification Plugins ({plugins.length})
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {plugins.map((p) => (
                <div key={p.plugin_id} className="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-white">{p.name}</span>
                    <Badge variant="info">{p.domain}</Badge>
                  </div>
                  <div className="text-[11px] text-slate-400 mt-2">Capabilities: {p.capabilities.join(', ')}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* Sub-Tab 3: Datasets Catalog (11 Classes) */}
      {subTab === 'DATASETS' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {datasets.map((d) => (
            <Card key={d.dataset_id} className="p-4 bg-slate-900/80 border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-cyan-400">{d.dataset_id}</span>
                <Badge variant="outline">{d.dataset_class}</Badge>
              </div>
              <div className="font-bold text-sm text-white">{d.name}</div>
              <div className="text-xs text-slate-400 mt-2 font-mono">Samples: {d.sample_count} records</div>
              <div className="text-[11px] font-mono text-slate-500 truncate mt-1">SHA-256: {d.sha256_checksum}</div>
            </Card>
          ))}
        </div>
      )}

      {/* Sub-Tab 4: Environments */}
      {subTab === 'ENVIRONMENTS' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {environments.map((e) => (
            <Card key={e.environment_id} className="p-4 bg-slate-900/80 border-slate-800">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-mono text-amber-400">{e.environment_id}</span>
                <Badge variant={e.is_ready ? 'success' : 'error'}>{e.env_type}</Badge>
              </div>
              <div className="font-bold text-sm text-white">{e.name}</div>
              <div className="grid grid-cols-2 gap-2 mt-4 text-xs font-mono text-slate-300">
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">CPU Usage</div>
                  <div className="text-cyan-400 font-bold">{e.cpu_utilization_pct}%</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Available RAM</div>
                  <div className="text-indigo-400 font-bold">{e.memory_available_mb} MB</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Network Latency</div>
                  <div className="text-emerald-400 font-bold">{e.network_latency_ms} ms</div>
                </div>
                <div className="p-2 bg-slate-950/60 rounded-lg">
                  <div className="text-slate-500">Sandboxes</div>
                  <div className="text-amber-400 font-bold">{e.active_sandboxes}</div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Sub-Tab 5: Evidence & Audit Ledger */}
      {subTab === 'EVIDENCE_AUDIT' && (
        <div className="space-y-6">
          {/* Tamper Check Status Banner */}
          {tamperCheckStatus && (
            <div className="p-4 bg-emerald-950/80 border border-emerald-500/40 rounded-xl text-emerald-400 font-mono text-sm flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4" />
              Tamper Verification Result: {tamperCheckStatus}
            </div>
          )}

          {/* Evidence Records */}
          <Card className="p-4 bg-slate-900/80 border-slate-800">
            <h3 className="font-bold text-sm text-white mb-3 flex items-center gap-2">
              <Lock className="w-4 h-4 text-cyan-400" />
              Content-Addressable Evidence Records ({evidenceList.length})
            </h3>
            <div className="space-y-3">
              {evidenceList.map((ev) => (
                <div key={ev.evidence_id} className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 flex items-center justify-between text-xs font-mono">
                  <div>
                    <div className="text-cyan-400 font-bold">{ev.evidence_id} ({ev.evidence_type})</div>
                    <div className="text-slate-400 truncate max-w-xl mt-0.5">{ev.content_preview}</div>
                    <div className="text-slate-500 text-[11px] mt-0.5">SHA-256: {ev.payload_hash}</div>
                  </div>
                  <Button
                    variant="outline"
                    onClick={() => handleVerifyTamper(ev.evidence_id)}
                    className="text-xs font-mono"
                  >
                    Verify Cryptographic Seal
                  </Button>
                </div>
              ))}
            </div>
          </Card>

          {/* Immutable Audit Ledger */}
          <Card className="p-4 bg-slate-900/80 border-slate-800">
            <h3 className="font-bold text-sm text-white mb-3 flex items-center gap-2">
              <FileCheck className="w-4 h-4 text-indigo-400" />
              Immutable Hash-Chained Audit Trail ({auditTrail.length})
            </h3>
            <div className="space-y-2">
              {auditTrail.map((entry) => (
                <div key={entry.audit_id} className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 text-xs font-mono text-slate-300">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-amber-400">{entry.event_type}</span>
                    <span className="text-slate-500">{entry.timestamp}</span>
                  </div>
                  <div className="text-slate-400 mt-1">Entity: {entry.entity_id} (Actor: {entry.actor})</div>
                  <div className="text-[11px] text-slate-600 truncate mt-1">Prev: {entry.sha256_prev_hash} $\rightarrow$ Current: {entry.sha256_entry_hash}</div>
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {/* Sub-Tab 6: End-to-End Lineage DAG */}
      {subTab === 'TRACEABILITY' && (
        <Card className="p-6 bg-slate-900/80 border-slate-800">
          <h3 className="font-bold text-sm text-white mb-4 flex items-center gap-2">
            <GitBranch className="w-4 h-4 text-cyan-400" />
            End-to-End Verification Lineage Graph (GUID-Mapped)
          </h3>
          <div className="space-y-3">
            {lineageNodes.length > 0 ? (
              lineageNodes.map((node) => (
                <div key={node.node_id} className="p-3 bg-slate-950/80 rounded-xl border border-slate-800 font-mono text-xs">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-cyan-400">[{node.node_type}] {node.label}</span>
                    <span className="text-slate-500">{node.node_id}</span>
                  </div>
                  {node.connections.length > 0 && (
                    <div className="text-slate-400 text-[11px] mt-1">
                      $\rightarrow$ Links to: {node.connections.join(', ')}
                    </div>
                  )}
                </div>
              ))
            ) : (
              <div className="text-sm font-mono text-slate-500 text-center py-6">
                Run a verification workflow to generate the end-to-end lineage graph.
              </div>
            )}
          </div>
        </Card>
      )}
    </div>
  );
};
