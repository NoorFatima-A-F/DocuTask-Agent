import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Boxes,
  RotateCw,
  Sparkles,
  AlertTriangle,
} from 'lucide-react';
import { organizationPlatformApiClient } from '../../services/organizationPlatformApiClient';
import type { OrganizationSimulationReport } from '../../types/organizationPlatform';

export const OrganizationSimulationStudio: React.FC = () => {
  const [reports, setReports] = useState<OrganizationSimulationReport[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [simulating, setSimulating] = useState<boolean>(false);
  const [selectedReport, setSelectedReport] = useState<OrganizationSimulationReport | null>(null);

  const loadReports = async () => {
    try {
      setLoading(true);
      const data = await organizationPlatformApiClient.getSimulations();
      setReports(data);
      if (data.length > 0 && !selectedReport) {
        setSelectedReport(data[0] || null);
      }
    } catch (err) {
      console.error('Failed to load simulations:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleRunSimulation = async () => {
    try {
      setSimulating(true);
      const rep = await organizationPlatformApiClient.runSimulation(100);
      await loadReports();
      setSelectedReport(rep);
    } catch (err) {
      console.error('Error running organizational simulation:', err);
    } finally {
      setSimulating(false);
    }
  };

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 border-b border-border pb-4">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-primary/10 rounded-lg text-primary">
            <Boxes className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold tracking-tight">Digital Twin Organization Simulator</h1>
            <p className="text-sm text-muted-foreground">
              Synthetic Enterprise Sandbox, Stress Testing, Chaos Fault Injections & Resilience Certification
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="outline" onClick={loadReports} disabled={loading}>
            <span className="flex items-center gap-2">
              <RotateCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </span>
          </Button>
          <Button variant="intelligence" onClick={handleRunSimulation} disabled={simulating}>
            <span className="flex items-center gap-2">
              <Sparkles className="w-4 h-4" />
              {simulating ? 'Simulating 100 Twins...' : 'Run 100-Twin Stress Test'}
            </span>
          </Button>
        </div>
      </div>

      {/* Main Two-Column View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Reports List */}
        <div className="space-y-4">
          <h2 className="text-sm font-semibold">Simulation Runs ({reports.length})</h2>
          <div className="space-y-3">
            {reports.map((r) => (
              <Card
                key={r.report_id}
                onClick={() => setSelectedReport(r)}
                className={`border cursor-pointer transition-all ${
                  selectedReport?.report_id === r.report_id
                    ? 'border-primary bg-primary/5 shadow-sm'
                    : 'border-border hover:bg-muted/30'
                }`}
              >
                <CardContent className="p-4 space-y-2">
                  <div className="flex justify-between items-start">
                    <span className="font-semibold text-sm line-clamp-1">{r.scenario_name}</span>
                    <Badge variant={r.success_rate >= 0.95 ? 'success' : 'warning'}>
                      {(r.success_rate * 100).toFixed(0)}% Pass
                    </Badge>
                  </div>
                  <div className="flex justify-between text-xs text-muted-foreground pt-1">
                    <span>Runs: {r.runs_completed}</span>
                    <span>Resilience: {(r.resilience_score * 100).toFixed(0)}%</span>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

        {/* Selected Simulation Report Deep Dive */}
        <div className="lg:col-span-2 space-y-6">
          {selectedReport ? (
            <Card className="border-border shadow-sm">
              <CardHeader className="flex flex-row items-center justify-between pb-3">
                <div>
                  <CardTitle className="text-lg">{selectedReport.scenario_name}</CardTitle>
                  <p className="text-xs text-muted-foreground font-mono mt-0.5">{selectedReport.report_id}</p>
                </div>
                <Badge variant="success">{selectedReport.simulation_type}</Badge>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Metric Summary */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  <div className="p-3 bg-muted/40 border border-border rounded-lg text-center">
                    <div className="text-xs text-muted-foreground">Success Rate</div>
                    <div className="text-xl font-bold text-emerald-500 mt-0.5">
                      {(selectedReport.success_rate * 100).toFixed(1)}%
                    </div>
                  </div>
                  <div className="p-3 bg-muted/40 border border-border rounded-lg text-center">
                    <div className="text-xs text-muted-foreground">Mean ROI</div>
                    <div className="text-xl font-bold text-primary mt-0.5">{selectedReport.mean_roi_multiplier}x</div>
                  </div>
                  <div className="p-3 bg-muted/40 border border-border rounded-lg text-center">
                    <div className="text-xs text-muted-foreground">p95 Latency</div>
                    <div className="text-xl font-bold mt-0.5">{selectedReport.p95_latency_ms} ms</div>
                  </div>
                  <div className="p-3 bg-muted/40 border border-border rounded-lg text-center">
                    <div className="text-xs text-muted-foreground">Resilience Score</div>
                    <div className="text-xl font-bold text-purple-500 mt-0.5">
                      {(selectedReport.resilience_score * 100).toFixed(0)}%
                    </div>
                  </div>
                </div>

                {/* Injected Fault Scenarios */}
                <div className="space-y-2">
                  <h3 className="text-sm font-semibold flex items-center gap-2">
                    <AlertTriangle className="w-4 h-4 text-amber-500" />
                    Tested Chaos Stress Conditions
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2 text-xs">
                    <div className="p-2.5 bg-card border border-border rounded-lg">
                      <span className="font-semibold text-foreground">GPU Driver Failures</span>
                      <p className="text-muted-foreground mt-0.5">Instant worker failover to CPU backup nodes.</p>
                    </div>
                    <div className="p-2.5 bg-card border border-border rounded-lg">
                      <span className="font-semibold text-foreground">Workload 3x Surge</span>
                      <p className="text-muted-foreground mt-0.5">Dynamic DAG horizontal worker autoscaling.</p>
                    </div>
                    <div className="p-2.5 bg-card border border-border rounded-lg">
                      <span className="font-semibold text-foreground">Agent Deadlock Resolution</span>
                      <p className="text-muted-foreground mt-0.5">Nash arbitration triggers within 120ms.</p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card className="border-border shadow-sm p-8 text-center text-muted-foreground">
              Select a simulation report to inspect digital twin telemetry.
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};
