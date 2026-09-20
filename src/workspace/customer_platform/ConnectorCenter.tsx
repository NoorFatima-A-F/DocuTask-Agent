import React from 'react';
import { Badge } from '../../components/ui/Badge';
import { Button } from '../../components/ui/Button';

export const ConnectorCenter: React.FC = () => {
  const connectors = [
    { id: 'CONN-GMAIL', name: 'Google Workspace Gmail', category: 'Communication', status: 'Connected', latency: '32ms', calls24h: '1,420' },
    { id: 'CONN-OUTLOOK', name: 'Microsoft 365 Exchange / Outlook', category: 'Communication', status: 'Connected', latency: '28ms', calls24h: '890' },
    { id: 'CONN-SLACK', name: 'Slack Enterprise Grid', category: 'Communication', status: 'Connected', latency: '18ms', calls24h: '3,120' },
    { id: 'CONN-TEAMS', name: 'Microsoft Teams Adaptive Cards', category: 'Communication', status: 'Connected', latency: '22ms', calls24h: '650' },
    { id: 'CONN-GDRIVE', name: 'Google Drive & Cloud Storage', category: 'Storage', status: 'Connected', latency: '45ms', calls24h: '2,400' },
    { id: 'CONN-SHAREPOINT', name: 'Microsoft SharePoint Online', category: 'Storage', status: 'Connected', latency: '52ms', calls24h: '1,100' },
    { id: 'CONN-QUICKBOOKS', name: 'Intuit QuickBooks Online', category: 'Business Systems', status: 'Connected', latency: '64ms', calls24h: '4,200' },
    { id: 'CONN-SALESFORCE', name: 'Salesforce Enterprise CRM', category: 'Business Systems', status: 'Connected', latency: '48ms', calls24h: '1,800' },
    { id: 'CONN-JIRA', name: 'Atlassian Jira Service Management', category: 'Business Systems', status: 'Connected', latency: '38ms', calls24h: '950' },
    { id: 'CONN-WEBHOOK', name: 'Custom REST Webhook Gateway', category: 'API & ERP', status: 'Connected', latency: '12ms', calls24h: '7,800' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-[#0F172A] to-[#1E293B] border border-[#334155]/60 shadow-xl">
        <div>
          <Badge variant="intelligence" size="sm">INTEGRATION HUB</Badge>
          <h1 className="text-2xl font-black text-white mt-1">Enterprise Connector Center</h1>
          <p className="text-sm text-[#94A3B8]">
            Pre-authenticated connectors for seamless document ingestion, communication, and ERP dispatch.
          </p>
        </div>
        <Button variant="primary" size="md">+ Add Custom Webhook</Button>
      </div>

      {/* Connectors Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {connectors.map((conn) => (
          <div key={conn.id} className="p-5 rounded-2xl bg-[#0F172A]/80 border border-[#1E293B] shadow-xl space-y-4 hover:border-[#00D2FF]/40 transition-all">
            <div className="flex items-center justify-between">
              <Badge variant="default" size="sm">{conn.category}</Badge>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-950/40 px-2 py-0.5 rounded border border-emerald-800/40">
                ● {conn.status}
              </span>
            </div>

            <div>
              <h3 className="text-sm font-bold text-white">{conn.name}</h3>
              <span className="text-xs text-[#64748B] font-mono">{conn.id}</span>
            </div>

            <div className="grid grid-cols-2 gap-2 py-2 border-t border-[#1E293B] text-xs">
              <div>
                <span className="text-[#94A3B8] block text-[10px]">Avg Latency</span>
                <span className="font-mono text-cyan-400 font-bold">{conn.latency}</span>
              </div>
              <div>
                <span className="text-[#94A3B8] block text-[10px]">24h Volume</span>
                <span className="font-mono text-white font-bold">{conn.calls24h} calls</span>
              </div>
            </div>

            <div className="flex gap-2">
              <Button variant="secondary" size="sm" className="w-full">Test Ping</Button>
              <Button variant="outline" size="sm" className="w-full">Configure</Button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
