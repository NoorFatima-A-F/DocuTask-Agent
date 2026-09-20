import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../../components/ui/Card';
import { Button } from '../../components/ui/Button';
import { Badge } from '../../components/ui/Badge';
import { SaaSApiClient } from '../../services/saasApiClient';
import type { ConnectorConfig } from '../../types/saasPlatform';
import { Radio, CheckCircle2, Activity, RefreshCw } from 'lucide-react';

export const IntegrationHub: React.FC = () => {
  const [connectors, setConnectors] = useState<ConnectorConfig[]>([]);
  const [testResults, setTestResults] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const load = async () => {
      setLoading(true);
      const list = await SaaSApiClient.listIntegrations('tenant_acme_corp');
      setConnectors(list);
      setLoading(false);
    };
    load();
  }, []);

  const handleTest = async (connectorId: string) => {
    setTestResults((prev) => ({ ...prev, [connectorId]: 'TESTING...' }));
    const res = await SaaSApiClient.testConnector(connectorId);
    setTestResults((prev) => ({ ...prev, [connectorId]: `${res.status} (${res.latency_ms}ms)` }));
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white flex items-center gap-3">
            <Radio className="w-7 h-7 text-indigo-400" />
            Enterprise Integration Hub
          </h1>
          <p className="text-sm text-slate-400 mt-1">
            Connect autonomous agent meshes to Google Drive, Teams, Slack, SAP, Salesforce, Jira, and GitHub.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2" /> Loading Connectors...
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {connectors.map((c) => {
            const testStatus = testResults[c.connector_id];
            return (
              <Card key={c.connector_id} className="bg-slate-900/80 border-slate-800">
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="text-lg text-white">{c.name}</CardTitle>
                      <span className="text-xs font-mono text-slate-400">{c.connector_type}</span>
                    </div>
                    <Badge variant={c.status === 'CONNECTED' ? 'success' : 'error'}>{c.status}</Badge>
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="text-xs text-slate-400 space-y-1 bg-slate-800/40 p-3 rounded">
                    <div>Auth Type: <span className="text-slate-200 font-mono">{c.auth_type}</span></div>
                    <div>Last Synced: <span className="text-slate-200">{new Date(c.last_synced_at).toLocaleTimeString()}</span></div>
                    <div>Connected Workspaces: <span className="text-indigo-400 font-mono">{c.connected_workspaces.join(', ')}</span></div>
                  </div>

                  <div className="flex items-center justify-between pt-2">
                    {testStatus && (
                      <span className="text-xs font-mono text-emerald-400 flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> {testStatus}
                      </span>
                    )}
                    {!testStatus && <span className="text-xs text-slate-500">Ready for ping test</span>}

                    <Button variant="outline" onClick={() => handleTest(c.connector_id)}>
                      <span className="flex items-center gap-1.5 text-xs">
                        <Activity className="w-3.5 h-3.5" /> Test Link
                      </span>
                    </Button>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};
