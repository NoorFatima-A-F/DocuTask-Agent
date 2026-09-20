import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import {
  Server,
  RotateCw,
  Activity,
} from 'lucide-react';
import { executionPlatformApiClient } from '../../services/executionPlatformApiClient';
import type { ConnectorConfig } from '../../types/executionPlatform';

export const ConnectorManagementCenter: React.FC = () => {
  const [connectors, setConnectors] = useState<ConnectorConfig[]>([]);
  const [testingId, setTestingId] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  const loadConnectors = async () => {
    try {
      setLoading(true);
      const res = await executionPlatformApiClient.listConnectors();
      setConnectors(res.connectors || []);
    } catch (err) {
      console.error('Failed to load connectors:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadConnectors();
  }, []);

  const handleTestConnector = async (connectorId: string) => {
    try {
      setTestingId(connectorId);
      await executionPlatformApiClient.testConnector(connectorId);
      await loadConnectors();
    } catch (err) {
      console.error('Error testing connector:', err);
    } finally {
      setTestingId(null);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
        <div>
          <h1 className="text-xl font-bold text-white flex items-center gap-2">
            <Server className="w-5 h-5 text-emerald-400" />
            Universal Connector Framework & Gateway Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">
            Real-time connection pooling, round-trip latency probes, protocol adapters (REST, gRPC, DBs, Cloud SDKs)
          </p>
        </div>
        <Button variant="outline" onClick={loadConnectors}>
          <span className="flex items-center gap-2">
            <RotateCw className="w-4 h-4" />
            Refresh
          </span>
        </Button>
      </div>

      {/* Connectors Grid */}
      {loading && connectors.length === 0 ? (
        <p className="text-xs text-slate-500 py-8 text-center">Loading connectors...</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {connectors.map((c) => (
          <Card key={c.connector_id} className="bg-slate-900/60 border-slate-800 flex flex-col justify-between">
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                <Badge variant="outline" className="text-xs">{c.category}</Badge>
                <Badge
                  variant={c.status === 'connected' ? 'success' : 'error'}
                  className="flex items-center gap-1"
                >
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  {c.status}
                </Badge>
              </div>
              <CardTitle className="text-base text-white mt-2">{c.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="text-xs space-y-1.5 font-mono text-slate-400">
                <p className="truncate">
                  <span className="text-slate-500">Endpoint:</span> {c.endpoint_url}
                </p>
                <p>
                  <span className="text-slate-500">Protocol:</span> {c.protocol}
                </p>
                <p>
                  <span className="text-slate-500">Latency:</span> {c.latency_ms} ms
                </p>
                <p>
                  <span className="text-slate-500">RPM:</span> {c.rpm_used} / {c.rate_limit_rpm}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                <span className="text-[11px] text-emerald-400 font-semibold">
                  Health: {(c.health_score * 100).toFixed(0)}%
                </span>
                <Button
                  variant="outline"
                  className="text-xs"
                  onClick={() => handleTestConnector(c.connector_id)}
                  disabled={testingId === c.connector_id}
                >
                  <span className="flex items-center gap-1.5">
                    <Activity className="w-3.5 h-3.5 text-emerald-400" />
                    {testingId === c.connector_id ? 'Probing...' : 'Probe Health'}
                  </span>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
        </div>
      )}
    </div>
  );
};
