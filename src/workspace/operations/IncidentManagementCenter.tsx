import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  Clock,
  RefreshCw,
  Zap
} from 'lucide-react';
import { Card } from '../../components/ui/Card';
import { Badge } from '../../components/ui/Badge';

interface IncidentManagementCenterProps {
  missionId?: string;
}

export const IncidentManagementCenter: React.FC<IncidentManagementCenterProps> = ({
  missionId = 'cluster-primary-master',
}) => {
  const [incidents] = useState([
    {
      id: 'inc-9b2f1a',
      title: 'Worker Thread Crash in Local Tesseract Cluster',
      subsystem: 'WORKERS',
      severity: 'MEDIUM',
      detectedAt: '10:14:02 UTC',
      status: 'RESOLVED',
      healingAction: 'WORKER_RESTART',
      mttrMs: 145,
      impactCost: '$0.00',
    },
    {
      id: 'inc-3e7c8d',
      title: 'Model Rate Limit Spike on Gemini 1.5 Pro',
      subsystem: 'API',
      severity: 'HIGH',
      detectedAt: '09:42:15 UTC',
      status: 'RESOLVED',
      healingAction: 'FALLBACK_MODEL_ENGAGE',
      mttrMs: 82,
      impactCost: '$0.00',
    },
    {
      id: 'inc-1a4f0e',
      title: 'Vector Cache Index Eviction Anomaly',
      subsystem: 'MEMORY',
      severity: 'LOW',
      detectedAt: '08:12:30 UTC',
      status: 'RESOLVED',
      healingAction: 'MEMORY_REPAIR',
      mttrMs: 65,
      impactCost: '$0.00',
    },
  ]);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-100 flex items-center gap-2">
            <AlertTriangle className="w-5 h-5 text-amber-400" />
            Autonomous Incident Intelligence & Management Center
          </h2>
          <p className="text-sm text-slate-400">
            Real-time incident detection, correlation clustering, severity classification, and automated healing resolution for: <code className="text-amber-300 font-mono text-xs">{missionId}</code>
          </p>
        </div>
        <div className="flex items-center gap-3">
          <Badge variant="success" size="md">
            Active Incidents: 0
          </Badge>
          <button className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-medium rounded-lg border border-slate-700">
            <RefreshCw className="w-3.5 h-3.5" />
            Sync Incident Stream
          </button>
        </div>
      </div>

      {/* Incident List */}
      <div className="space-y-4 font-mono">
        {incidents.map((inc) => (
          <Card key={inc.id} className="p-5 bg-slate-900 border-slate-800 hover:border-slate-700 transition-all">
            <div className="flex items-start justify-between">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">{inc.id}</span>
                  <Badge variant={inc.severity === 'HIGH' ? 'error' : inc.severity === 'MEDIUM' ? 'warning' : 'default'} size="sm">
                    {inc.severity}
                  </Badge>
                  <span className="text-xs text-indigo-400 font-bold">{inc.subsystem}</span>
                </div>
                <h3 className="text-sm font-bold text-slate-100">{inc.title}</h3>
                <div className="flex items-center gap-4 text-xs text-slate-400 pt-1">
                  <span className="flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                    Detected: {inc.detectedAt}
                  </span>
                  <span className="flex items-center gap-1 text-emerald-400">
                    <Zap className="w-3.5 h-3.5" />
                    Healed: {inc.healingAction} ({inc.mttrMs}ms)
                  </span>
                </div>
              </div>

              <div className="text-right space-y-1">
                <Badge variant="success" size="sm" className="gap-1">
                  <CheckCircle2 className="w-3 h-3" />
                  {inc.status}
                </Badge>
                <span className="text-xs text-slate-400 block font-bold">Loss: {inc.impactCost}</span>
              </div>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};
